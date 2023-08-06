import logging
from pathlib import Path
import platform
from typing import (
    Any,
    List,
    Optional,
    Union,
)
import uuid
import warnings

from amalgam.api import Amalgam
from diveplane.client.exceptions import DiveplaneError, DiveplaneWarning
from diveplane.utilities.internals import sanitize_for_json
import diveplane.utilities.json_wrapper as json
from pkg_resources import resource_filename
import six

_logger = logging.getLogger('diveplane.direct')

# Position under home directory of downloaded amalgam files
core_lib_dirname = ".diveplane/lib/core/"
amlg_lib_dirname = ".diveplane/lib/amlg/"


class DiveplaneCore:
    """
    Diveplane Core API.

    This class is used in conjunction with the Amalgam python interface to
    interact with the Diveplane Core and Amalgam binaries.

    Parameters
    ----------
    handle : str
        Handle for the Diveplane entity. If none is provided a random 6 digit
        alphanumeric handle will be assigned.
    library_path : str, optional
        Path to Amalgam library.
    gc_interval : int, default 100
        Number of Amalgam operations to perform before forcing garbage collection.
        Lower is better at memory management but compromises performance.
        Higher is better performance but may result in higher memory usage.
    diveplane_path : str, default "~/.diveplane/lib/dev/core/"
        Directory path to the Diveplane caml files.
    trainee_template_path : str, default "~/.diveplane/lib/dev/core/"
        Directory path to the trainee_template caml files.
    diveplane_fname : str, default "diveplane.caml"
        Name of the Diveplane caml file with extension.
    trainee_template_fname : str, default "trainee_template.caml"
        Name of the trainee template file with extension.
    write_log : str, optional
        Absolute path to write log file.
    print_log : str, optional
        Absolute path to print log file.
    amlg_debug : bool, default False
        Deprecated, use "trace" parameter instead.
    trace: bool, default False
        If true, sets debug flag for amlg operations. This will generate an
        execution trace useful in debugging with the standard name of
        [HANDLE]_execution.trace.
    sbf_datastore_enabled : bool, default True
        If true, sbf tree structures are enabled.
    max_num_threads : int, default 0
        If a multithreaded Amalgam binary is used, sets the maximum number of
        threads to the value specified. If 0, will use the number of visible
        logical cores.
    license_file : str, optional
        The path to a license file.
    """

    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types

    def __init__(  # noqa: C901
        self,
        handle: Optional[str] = None,
        library_path: Optional[str] = None,
        gc_interval: int = 100,
        diveplane_path: str = str(Path(Path.home(), '.diveplane', 'lib', 'dev', 'core')),
        trainee_template_path: str = str(Path(Path.home(), '.diveplane', 'lib', 'dev', 'core')),
        diveplane_fname: str = "diveplane.caml",
        trainee_template_fname: str = "trainee_template.caml",
        write_log: Optional[str] = None,
        print_log: Optional[str] = None,
        trace: bool = False,
        sbf_datastore_enabled: bool = True,
        max_num_threads: int = 0,
        license_file: Optional[str] = None,
        **kwargs
    ):
        self.handle = handle if handle is not None else self.random_handle()
        if kwargs.get("amlg_debug", None) is not None:
            if trace is None:
                trace = kwargs["amlg_debug"]
            _logger.warning(
                'The "amlg_debug" parameter is deprecated use "trace" instead.')

        self.trace = bool(trace)

        if write_log is not None:
            self.write_log = Path(write_log).expanduser()
        else:
            self.write_log = ''

        if print_log is not None:
            self.print_log = Path(print_log).expanduser()
        else:
            self.print_log = ''

        # The parameters to pass to the Amalgam object - compiled here, so that
        # they can be merged with config file params.
        amlg_params = {
            'library_path': library_path,
            'gc_interval': gc_interval,
            'sbf_datastore_enabled': sbf_datastore_enabled,
            'max_num_threads': max_num_threads,
            'trace': self.trace,
            'execution_trace_file': self.handle + "_execution.trace",
        }

        # Check if there is a file present at the given location.
        self.license_file = None
        if license_file:
            license_file = Path(license_file).expanduser()
            if Path(license_file).is_file():
                self.license_file = Path(license_file).resolve()

        try:
            # merge parameters from config.yml - favoring the configured params
            amlg_params_intersection = amlg_params.keys(
            ) & kwargs['amalgam'].keys()
            # Warn that there are conflicts
            if amlg_params_intersection:
                _logger.warning(
                    "The following parameters from configuration file will "
                    "override the Amalgam parameters set in the code: " +
                    str(amlg_params_intersection)
                )
            amlg_params = {**amlg_params, **kwargs['amalgam']}

        except KeyError:
            # No issue, if there is no amalgam key
            pass

        # Infer the os/arch from the running platform, unless set in config
        operating_system = amlg_params.setdefault('os', platform.system().lower())
        if operating_system == 'windows':
            library_file_extension = "dll"
        elif operating_system == 'darwin':
            library_file_extension = "dylib"
        else:
            library_file_extension = "so"

        # Assemble the library file name - use multithreaded library by default
        library_postfix = amlg_params.get('library_postfix', '-mt')
        library_filename = f'amalgam{library_postfix}.{library_file_extension}'

        # Infer the architecture unless set, and normalize
        architecture = amlg_params.setdefault('arch', platform.machine().lower())
        if architecture in ['x86_64', 'amd64']:
            architecture = 'amd64'
        elif architecture in ['aarch64_be', 'aarch64', 'armv8b', 'armv8l']:
            # see: https://stackoverflow.com/questions/45125516/possible-values-for-uname-m
            architecture = 'arm64'

        # If embedded set, its value is a package path to the amalgam library files or True
        if 'embedded' in amlg_params:
            if amlg_params.get('download'):
                _logger.warning('Incompatible amalgam params \'embedded\' and \'download\' set. '
                                'Disregarding download configuration')

            # Calculate the full path to the library file
            if amlg_params['embedded'] is True:
                embedded_amlg_location = 'diveplane.local.lib.amlg'
                warnings.warn(f'The use of a boolean for "embedded" is deprecated. '
                              f'Please update your diveplane.yml to use the package path instead.'
                              f'Defaulting to {embedded_amlg_location}')
            else:
                embedded_amlg_location = amlg_params['embedded']

            embedded_path = f'{embedded_amlg_location}.{operating_system}.{architecture}'
            embedded_resource_filename = resource_filename(embedded_path, library_filename)
            embedded_amlg_location = Path(embedded_resource_filename)

            if embedded_amlg_location.exists():
                amlg_params['library_path'] = str(embedded_amlg_location)
                _logger.debug(f'Using embedded amalgam location: {embedded_amlg_location}')
            else:
                raise DiveplaneError(f'No amalgam library found at {embedded_amlg_location}')

        # If download set (but not embedded), try and download the specified version using diveplane-build-artifacts
        elif amlg_params.get('download'):
            # Download amalgam (unless already there) - and get the path
            amalgam_download_dir = self.download_amlg(amlg_params)
            amlg_params['library_path'] = str(Path(
                amalgam_download_dir, 'lib',
                f"amalgam{library_postfix}.{library_file_extension}"
            ))
            _logger.debug(f'Using downloaded amalgam location: {amlg_params["library_path"]}')

        # If version is set, but download not, use the default download location
        elif amlg_params.get('version'):
            versioned_amlg_location = Path(Path.home(), amlg_lib_dirname, operating_system,
                                           architecture, amlg_params.get('version'), 'lib',
                                           f"amalgam{library_postfix}.{library_file_extension}")
            if versioned_amlg_location.exists():
                amlg_params['library_path'] = str(versioned_amlg_location)
                _logger.debug(f'Using amalgam version located at: {amlg_params["library_path"]}')
            else:
                raise DiveplaneError(f'No amalgam library found at {versioned_amlg_location}')

        # Using the defaults
        else:
            _logger.debug(f'Using default amalgam location: {amlg_params["library_path"]}')

        # Filter out invalid amlg_params, and instantiate.
        amlg_params = {
            k: v for k, v in amlg_params.items()
            if k in ['library_path', 'gc_interval', 'sbf_datastore_enabled',
                     'max_num_threads', 'debug', 'trace', 'execution_trace_file',
                     'execution_trace_dir', 'library_postfix']
        }
        self.amlg = Amalgam(**amlg_params)

        core_params = kwargs.get('core', {})

        # If 'embedded' set, its value is a package path to the core library files or True
        if 'embedded' in core_params:
            if core_params.get('download'):
                _logger.warn('Incompatible params "embedded" and "download" set. '
                             'Disregarding download configuration')

            # Append filenames to the embedded path
            if core_params['embedded'] is True:
                diveplane_location = 'diveplane.local.lib.core'
                warnings.warn('The use of a boolean for "embedded" is deprecated. '
                              'Please update your diveplane.yml to use a package path instead.'
                              f'Using default path: {diveplane_location}')
            else:
                diveplane_location = core_params['embedded']

            diveplane_python_path = f'{diveplane_location}'
            diveplane_embedded_filepath = resource_filename(diveplane_python_path, 'diveplane.caml')
            trainee_template_embedded_filepath = resource_filename(diveplane_python_path, 'trainee_template.caml')

            diveplane_embedded_filepath = Path(diveplane_embedded_filepath)
            trainee_template_embedded_filepath = Path(trainee_template_embedded_filepath)

            _logger.debug(f'Using diveplane embedded filepath {diveplane_embedded_filepath}')
            _logger.debug(f'Using trainee template embedded filepath {trainee_template_embedded_filepath}')

            if not (diveplane_embedded_filepath.exists() and trainee_template_embedded_filepath.exists()):
                raise DiveplaneError(f'Core files diveplane.caml and/or trainee_template.caml '
                                     f'not found at {diveplane_embedded_filepath} '
                                     f'and/or {trainee_template_embedded_filepath}')

            diveplane_embedded_dir = diveplane_embedded_filepath.parent.expanduser()
            self.diveplane_path = self.trainee_template_path = diveplane_embedded_dir
            _logger.debug(f'Using diveplane location: {self.diveplane_path}')
            _logger.debug(f'Using trainee_template location: {self.trainee_template_path}')
            self.default_save_path = Path(Path.home(), '.diveplane', 'saved_trainees')

        # If download (and not embedded), then retrieve using diveplane-build-artifacts
        elif core_params.get('download', False):
            self.diveplane_path = Path(self.download_core(core_params)).expanduser()
            self.trainee_template_path = self.diveplane_path
            self.default_save_path = Path(self.diveplane_path, 'trainee')

        # If version is set, but download not, use the default download location
        elif core_params.get('version'):
            # Set paths, ensuring tailing slash
            self.diveplane_path = Path(Path.home(), core_lib_dirname,
                                       core_params.get('version'))
            self.trainee_template_path = self.diveplane_path
            self.default_save_path = Path(self.diveplane_path, "trainee")

        # .... otherwise use default locations
        else:
            # Set paths, ensuring tailing slash
            self.diveplane_path = Path(diveplane_path).expanduser()
            self.trainee_template_path = Path(trainee_template_path).expanduser()
            self.default_save_path = Path(self.diveplane_path, "trainee")

        # Allow for trainee save directory to be overridden
        if core_params.get('persisted_trainees_dir'):
            self.default_save_path = Path(core_params.get("persisted_trainees_dir")).expanduser()
            _logger.debug(f'Trainee save directory has been overridden to {self.default_save_path}')
        # make save dir if doesn't exist
        if not self.default_save_path.exists():
            self.default_save_path.mkdir(parents=True)
        # make log dir(s) if they do not exist
        if self.write_log and not self.write_log.parent.exists():
            self.write_log.mkdir()
        if self.print_log and not self.print_log.parent.exists():
            self.print_log.mkdir()

        self.diveplane_fname = diveplane_fname
        self.trainee_template_fname = trainee_template_fname
        self.ext = trainee_template_fname[trainee_template_fname.rindex('.'):]

        self.diveplane_fully_qualified_path = Path(self.diveplane_path, self.diveplane_fname)
        if not self.diveplane_fully_qualified_path.exists():
            raise DiveplaneError(f'Diveplane core file {self.diveplane_fully_qualified_path} does not exist')
        _logger.debug(f'Using diveplane-core location: {self.diveplane_fully_qualified_path}')

        self.trainee_template_fully_qualified_path = Path(self.trainee_template_path, self.trainee_template_fname)
        if not self.trainee_template_fully_qualified_path.exists():
            raise DiveplaneError(f'Diveplane core file {self.trainee_template_fully_qualified_path} does not exist')
        _logger.debug('Using diveplane-core trainee template location: '
                      f'{self.trainee_template_fully_qualified_path}')

        if self.handle in self.get_entities():
            self.loaded = True
        else:
            self.loaded = self.amlg.load_entity(
                handle=self.handle,
                amlg_path=str(self.diveplane_fully_qualified_path),
                write_log=str(self.write_log),
                print_log=str(self.print_log)
            )

        # If a license is provided, enable the license_checks and add license.
        if self.license_file:
            # The following line could be removed when licensing is released.
            self.amlg.set_number_value(self.handle, "disable_license_checks", 0)
            result = self._execute("add_license", {"full_path": str(self.license_file)})
            print(result.get('message'))

    @staticmethod
    def random_handle() -> str:
        """
        Generate a random 6 byte hexadecimal handle.

        Returns
        -------
        str
            A random 6 byte hex.
        """
        try:
            # Use of secrets/uuid must be used instead of the "random" package
            # as they will not be affected by setting random.seed which could
            # cause duplicate handles to be generated.
            import secrets
            return secrets.token_hex(6)
        except (ImportError, NotImplementedError):
            # Fallback to uuid if operating system does not support secrets
            return uuid.uuid4().hex[-12:]

    def __str__(self) -> str:
        """Return a string representation of the DiveplaneCore object."""
        return "Trainee template:\t %s%s\n Diveplane Path:\t\t %s%s\n Save Path:\t\t %s\n " \
               "Write Log:\t\t %s\n Print Log:\t\t %s\n Handle:\t\t\t %s\n %s" % (
                   self.trainee_template_path, self.trainee_template_fname, self.diveplane_path, self.diveplane_fname,
                   self.default_save_path, self.write_log, self.print_log, self.handle, str(self.amlg))

    def version(self) -> str:
        """Return the version of the Diveplane Core."""
        if self.trainee_template_fname.split('.')[1] == 'amlg':
            version = "9.9.9"
        else:
            version = self._execute("version", {})
        return version

    def get_trainee_version(self, trainee, version=None) -> str:
        """Return the version of the Trainee Template."""
        return self._execute("get_trainee_version", {"trainee": trainee, "version": version})

    def create_trainee(self, trainee):
        """
        Create a Trainee using the Trainee Template.

        Parameters
        ----------
        trainee : str
            The name of the Trainee to create.
        """
        return self._execute("create_trainee",
                             {
                                 "trainee": trainee,
                                 "filepath": f"{self.trainee_template_path}/",
                                 "trainee_template_filename": self.trainee_template_fname.split('.')[0],
                                 "file_extension": self.trainee_template_fname.split('.')[1]
                             })

    def get_loaded_trainees(self) -> List[str]:
        """Get loaded Trainees."""
        return self._execute("get_loaded_trainees", {})

    def get_entities(self) -> List[str]:
        """Get loaded entities."""
        return self.amlg.get_entities()

    def load(
        self,
        trainee: str,
        filename: Optional[str] = None,
        filepath: Optional[str] = None,
    ) -> Union[Any, None]:
        """
        Load a persisted Trainee from disk.

        Parameters
        ----------
        trainee : str
            The ID or name of the Trainee to load.
        filename : str, optional
            The filename to load.
        filepath : str, optional
            The path containing the filename to load.
        """
        filename = trainee if filename is None else filename
        filepath = f"{self.default_save_path}/" if filepath is None else filepath
        ret = self._execute("load", {
            "trainee": trainee,
            "filename": filename,
            "filepath": filepath
        })

        return ret

    def persist(
        self,
        trainee: str,
        filename: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        """
        Save a Trainee to disk.

        Parameters
        ----------
        trainee : str
            The name or ID of the Trainee to save.
        filename : str, optional
            The name of the file to save the Trainee to.
        filepath : str, optional
            The path of the file to save the Trainee to.
        """
        filename = trainee if filename is None else filename
        filepath = f"{self.default_save_path}/" if filepath is None else filepath
        return self._execute("save",
                             {
                                 "trainee": trainee,
                                 "filename": filename,
                                 "filepath": filepath
                             })

    def delete(self, trainee: str):
        """
        Delete a Trainee.

        Parameters
        ----------
        trainee : str
            The name or ID of the Trainee to delete.
        """
        return self._execute("delete", {"trainee": trainee})

    def copy(self, trainee: str, target_trainee: str):
        """
        Copy the contents of one Trainee into another.

        Parameters
        ----------
        trainee : str
            The name or ID of the Trainee to copy from.
        target_trainee : str
            The name or ID of the Trainee to copy into.
        """
        return self._execute("copy",
                             {
                                 "trainee": trainee,
                                 "target_trainee": target_trainee
                             })

    def remove_series_store(self, trainee_id: str, series: Optional[str] = None):
        """
        Delete part or all of the series store from a Trainee.

        Parameters
        ----------
        trainee_id : str
            The ID of the Trainee to delete the series store from.
        series : str, optional
            The ID of the series to remove from the series store.

            If None, the entire series store will be deleted.
        """
        return self._execute("remove_series_store", {
            "trainee": trainee_id,
            "series": series
        })

    def clean_data(self, trainee, context_features, action_features, remove_duplicates=None):
        return self._execute("clean_data",
                             {
                                 "trainee": trainee,
                                 "context_features": context_features,
                                 "action_features": action_features,
                                 "remove_duplicates": remove_duplicates
                             })

    def set_substitute_feature_values(self, trainee, substitution_value_map):
        return self._execute("set_substitute_feature_values",
                             {
                                 "trainee": trainee,
                                 "substitution_value_map": substitution_value_map
                             })

    def get_substitute_feature_values(self, trainee):
        return self._execute("get_substitute_feature_values",
                             {
                                 "trainee": trainee
                             })

    def set_session_metadata(self, trainee, session, metadata):
        return self._execute("set_session_metadata", {
            "trainee": trainee,
            "session": session,
            "metadata": metadata
        })

    def get_session_metadata(self, trainee, session):
        return self._execute("get_session_metadata", {
            "trainee": trainee,
            "session": session
        })

    def get_sessions(self, trainee, attributes):
        return self._execute("get_sessions",
                             {
                                 "trainee": trainee,
                                 "attributes": attributes
                             })

    def remove_session(self, trainee, session):
        return self._execute("remove_session",
                             {
                                 "trainee": trainee,
                                 "session": session
                             })

    def remove_feature(self, trainee, feature, *, condition=None,
                       condition_session=None, session=None):
        return self._execute("remove_feature",
                             {
                                 "trainee": trainee,
                                 "feature": feature,
                                 "condition": condition,
                                 "session": session,
                                 "condition_session": condition_session
                             })

    def add_feature(
        self, trainee, feature, feature_value=None, *,
        condition=None, condition_session=None,
        feature_attributes=None, overwrite=False,
        session=None,
    ):
        return self._execute("add_feature",
                             {
                                 "trainee": trainee,
                                 "feature": feature,
                                 "feature_value": feature_value,
                                 "overwrite": overwrite,
                                 "condition": condition,
                                 "feature_attributes": feature_attributes,
                                 "session": session,
                                 "condition_session": condition_session
                             })

    def get_num_training_cases(self, trainee):
        return self._execute("get_num_training_cases",
                             {
                                 "trainee": trainee
                             })

    def auto_optimize_params(self, trainee,
                             auto_optimize_enabled=False,
                             optimize_threshold=None,
                             optimize_growth_factor=None,
                             auto_optimize_limit_size=None, **kwargs):
        params = {
            "trainee": trainee,
            "auto_optimize_enabled": auto_optimize_enabled,
            "optimize_threshold": optimize_threshold,
            "optimize_growth_factor": optimize_growth_factor,
            "auto_optimize_limit_size": auto_optimize_limit_size
        }
        return self._execute("set_auto_optimize", {**kwargs, **params})

    def auto_optimize(self, trainee):
        return self._execute("auto_optimize",
                             {
                                 "trainee": trainee
                             })

    def compute_feature_weights(self, trainee, action_feature, context_features,
                                robust, weight_feature, use_case_weights):
        return self._execute("compute_feature_weights",
                             {
                                 "trainee": trainee,
                                 "action_feature": action_feature,
                                 "context_features": context_features,
                                 "robust": robust,
                                 "weight_feature": weight_feature,
                                 "use_case_weights": use_case_weights
                             })

    def set_feature_weights(self, trainee, feature_weights=None, action_feature=None, use_feature_weights=True):
        return self._execute("set_feature_weights",
                             {
                                 "trainee": trainee,
                                 "action_feature": action_feature,
                                 "feature_weights_map": feature_weights,
                                 "use_feature_weights": use_feature_weights
                             })

    def set_feature_weights_matrix(self, trainee, feature_weights_matrix, use_feature_weights=True):
        return self._execute("set_feature_weights_matrix",
                             {
                                 "trainee": trainee,
                                 "feature_weights_matrix": feature_weights_matrix,
                                 "use_feature_weights": use_feature_weights
                             })

    def get_feature_weights_matrix(self, trainee):
        return self._execute("get_feature_weights_matrix",
                             {
                                 "trainee": trainee
                             })

    def clear_conviction_thresholds(self, trainee):
        return self._execute("clear_conviction_thresholds",
                             {
                                 "trainee": trainee
                             })

    def set_conviction_lower_threshold(self, trainee, conviction_lower_threshold):
        return self._execute("set_conviction_lower_threshold",
                             {
                                 "trainee": trainee,
                                 "conviction_lower_threshold": conviction_lower_threshold
                             })

    def set_conviction_upper_threshold(self, trainee, conviction_upper_threshold):
        return self._execute("set_conviction_upper_threshold",
                             {
                                 "trainee": trainee,
                                 "conviction_upper_threshold": conviction_upper_threshold
                             })

    def set_metadata(self, trainee, metadata):
        return self._execute("set_metadata",
                             {
                                 "trainee": trainee,
                                 "metadata": metadata
                             })

    def get_metadata(self, trainee):
        return self._execute("get_metadata",
                             {
                                 "trainee": trainee,
                             })

    def retrieve_extreme_cases_for_feature(self, trainee, features, sort_feature, num):
        return self._execute("retrieve_extreme_cases_for_feature",
                             {
                                 "trainee": trainee,
                                 "features": features,
                                 "sort_feature": sort_feature,
                                 "num": num
                             })

    def train(self, trainee, *, input_cases, features, derived_features,
              session, ablatement_params, series, input_is_substituted,
              accumulate_weight_feature, train_weights_only):
        return self._execute("train",
                             {
                                 "trainee": trainee,
                                 "input_cases": input_cases,
                                 "features": features,
                                 "derived_features": derived_features,
                                 "session": session,
                                 "ablatement_params": ablatement_params,
                                 "series": series,
                                 "input_is_substituted": input_is_substituted,
                                 "accumulate_weight_feature": accumulate_weight_feature,
                                 "train_weights_only": train_weights_only
                             })

    def impute(self, trainee, *, features, features_to_impute, session, batch_size=1):
        return self._execute("impute",
                             {
                                 "trainee": trainee,
                                 "features": features,
                                 "features_to_impute": features_to_impute,
                                 "session": session,
                                 "batch_size": batch_size
                             })

    def clear_imputed_session(self, trainee, session, impute_session):
        return self._execute("clear_imputed_session",
                             {
                                 "trainee": trainee,
                                 "session": session,
                                 "impute_session": impute_session
                             })

    def get_cases(self, trainee, features=None, session=None,
                  case_indices=None, indicate_imputed=0, condition=None,
                  num_cases=None, precision=None):
        return self._execute("get_cases",
                             {
                                 "trainee": trainee,
                                 "features": features,
                                 "session": session,
                                 "case_indices": case_indices,
                                 "indicate_imputed": indicate_imputed,
                                 "condition": condition,
                                 "num_cases": num_cases,
                                 "precision": precision
                             })

    def append_to_series_store(self, trainee, context_features,
                               contexts, series):
        return self._execute("append_to_series_store",
                             {
                                 "trainee": trainee,
                                 "context_features": context_features,
                                 "context_values": contexts,
                                 "series": series
                             })

    def react(self, trainee, context_features, context_values,
              action_features, action_values=None,
              case_access_count_label=None, extra_audit_features=None,
              case_indices=None, details=None,
              allow_nulls=False, new_case_threshold="min",
              use_regional_model_residuals=None,
              desired_conviction=None, feature_bounds_map=None,
              generate_new_cases="no", ordered_by_specified_features=False,
              preserve_feature_values=None, into_series_store=None,
              input_is_substituted=False, substitute_output=True,
              weight_feature=None, use_case_weights=False):
        return self._execute(
            "react",
            {
                "trainee": trainee,
                "context_features": context_features,
                "context_values": context_values,
                "action_features": action_features,
                "action_values": action_values,
                "details": details,
                "case_access_count_label": case_access_count_label,
                "extra_audit_features": extra_audit_features,
                "case_indices": case_indices,
                "allow_nulls": allow_nulls,
                "input_is_substituted": input_is_substituted,
                "substitute_output": substitute_output,
                "weight_feature": weight_feature,
                "use_case_weights": use_case_weights,
                "use_regional_model_residuals": use_regional_model_residuals,
                "desired_conviction": desired_conviction,
                "feature_bounds_map": feature_bounds_map,
                "generate_new_cases": generate_new_cases,
                "ordered_by_specified_features": ordered_by_specified_features,
                "preserve_feature_values": preserve_feature_values,
                "new_case_threshold": new_case_threshold,
                "into_series_store": into_series_store
            }
        )

    def batch_react(self, trainee, context_features, context_values,
                    action_features, action_values=None,
                    derived_context_features=None,
                    derived_action_features=None,
                    case_access_count_label=None,
                    extra_audit_features=None,
                    case_indices=None, details=None,
                    allow_nulls=False,
                    use_regional_model_residuals=None,
                    desired_conviction=None,
                    feature_bounds_map=None, generate_new_cases="no",
                    ordered_by_specified_features=False, preserve_feature_values=None,
                    into_series_store=None, input_is_substituted=False,
                    substitute_output=True, weight_feature=None,
                    use_case_weights=False, leave_case_out=None,
                    num_cases_to_generate=None,
                    new_case_threshold="min"):
        return self._execute(
            "batch_react",
            {
                "trainee": trainee,
                "context_features": context_features,
                "context_values": context_values,
                "action_features": action_features,
                "action_values": action_values,
                "derived_context_features": derived_context_features,
                "derived_action_features": derived_action_features,
                "details": details,
                "case_access_count_label": case_access_count_label,
                "extra_audit_features": extra_audit_features,
                "case_indices": case_indices,
                "allow_nulls": allow_nulls,
                "input_is_substituted": input_is_substituted,
                "substitute_output": substitute_output,
                "weight_feature": weight_feature,
                "use_case_weights": use_case_weights,
                "leave_case_out": leave_case_out,
                "num_cases_to_generate": num_cases_to_generate,
                "use_regional_model_residuals": use_regional_model_residuals,
                "desired_conviction": desired_conviction,
                "feature_bounds_map": feature_bounds_map,
                "generate_new_cases": generate_new_cases,
                "ordered_by_specified_features": ordered_by_specified_features,
                "preserve_feature_values": preserve_feature_values,
                "new_case_threshold": new_case_threshold,
                "into_series_store": into_series_store
            }
        )

    def batch_react_series(self, trainee, context_features, context_values,
                           action_features, action_values=None,
                           final_time_steps=None,
                           init_time_steps=None,
                           initial_features=None,
                           initial_values=None,
                           series_stop_maps=None,
                           max_series_lengths=None,
                           output_new_series_ids=True,
                           derived_context_features=None,
                           derived_action_features=None,
                           series_context_features=None,
                           series_context_values=None,
                           series_id_tracking="fixed",
                           case_access_count_label=None,
                           extra_audit_features=None,
                           case_indices=None,
                           preserve_feature_values=None,
                           new_case_threshold="min",
                           details=None,
                           use_regional_model_residuals=None,
                           desired_conviction=None,
                           feature_bounds_map=None, generate_new_cases="no",
                           ordered_by_specified_features=False,
                           input_is_substituted=False,
                           substitute_output=True, weight_feature=None,
                           use_case_weights=False, leave_case_out=None,
                           num_series_to_generate=None):
        return self._execute(
            "batch_react_series",
            {
                "trainee": trainee,
                "context_features": context_features,
                "context_values": context_values,
                "action_features": action_features,
                "action_values": action_values,
                "final_time_steps": final_time_steps,
                "init_time_steps": init_time_steps,
                "initial_features": initial_features,
                "initial_values": initial_values,
                "series_stop_maps": series_stop_maps,
                "max_series_lengths": max_series_lengths,
                "derived_context_features": derived_context_features,
                "derived_action_features": derived_action_features,
                "series_context_features": series_context_features,
                "series_context_values": series_context_values,
                "series_id_tracking": series_id_tracking,
                "output_new_series_ids": output_new_series_ids,
                "details": details,
                "case_access_count_label": case_access_count_label,
                "extra_audit_features": extra_audit_features,
                "case_indices": case_indices,
                "input_is_substituted": input_is_substituted,
                "substitute_output": substitute_output,
                "weight_feature": weight_feature,
                "use_case_weights": use_case_weights,
                "leave_case_out": leave_case_out,
                "num_series_to_generate": num_series_to_generate,
                "preserve_feature_values": preserve_feature_values,
                "new_case_threshold": new_case_threshold,
                "use_regional_model_residuals": use_regional_model_residuals,
                "desired_conviction": desired_conviction,
                "feature_bounds_map": feature_bounds_map,
                "generate_new_cases": generate_new_cases,
                "ordered_by_specified_features": ordered_by_specified_features
            }
        )

    def react_into_features(self, trainee, features=None,
                            familiarity_conviction_addition=False,
                            familiarity_conviction_removal=False,
                            p_value_of_addition=False,
                            p_value_of_removal=False,
                            distance_contribution=False,
                            high_distance_accuracy=True,
                            weight_feature=None,
                            use_case_weights=False):
        return self._execute("react_into_features",
                             {
                                 "trainee": trainee,
                                 "features": features,
                                 "familiarity_conviction_addition": familiarity_conviction_addition,
                                 "familiarity_conviction_removal": familiarity_conviction_removal,
                                 "p_value_of_addition": p_value_of_addition,
                                 "p_value_of_removal": p_value_of_removal,
                                 "distance_contribution": distance_contribution,
                                 "high_distance_accuracy": high_distance_accuracy,
                                 "weight_feature": weight_feature,
                                 "use_case_weights": use_case_weights
                             })

    def batch_react_group(self, trainee, *,
                          new_cases=None,
                          features=None,
                          trainees_to_compare=None,
                          distance_contributions=False,
                          familiarity_conviction_addition=True,
                          familiarity_conviction_removal=False,
                          kl_divergence_addition=False,
                          kl_divergence_removal=False,
                          p_value_of_addition=False,
                          p_value_of_removal=False,
                          high_distance_accuracy=True,
                          weight_feature=None,
                          use_case_weights=False):
        return self._execute("batch_react_group",
                             {
                                 "trainee": trainee,
                                 "features": features,
                                 "new_cases": new_cases,
                                 "trainees_to_compare": trainees_to_compare,
                                 "distance_contributions": distance_contributions,
                                 "familiarity_conviction_addition": familiarity_conviction_addition,
                                 "familiarity_conviction_removal": familiarity_conviction_removal,
                                 "kl_divergence_addition": kl_divergence_addition,
                                 "kl_divergence_removal": kl_divergence_removal,
                                 "p_value_of_addition": p_value_of_addition,
                                 "p_value_of_removal": p_value_of_removal,
                                 "high_distance_accuracy": high_distance_accuracy,
                                 "weight_feature": weight_feature,
                                 "use_case_weights": use_case_weights
                             })

    def compute_conviction_of_features(self, trainee, *,
                                       features=None,
                                       action_features=None,
                                       familiarity_conviction_addition=True,
                                       familiarity_conviction_removal=False,
                                       high_distance_accuracy=True,
                                       weight_feature=None,
                                       use_case_weights=False):
        return self._execute("compute_conviction_of_features",
                             {
                                 "trainee": trainee,
                                 "features": features,
                                 "action_features": action_features,
                                 "familiarity_conviction_addition": familiarity_conviction_addition,
                                 "familiarity_conviction_removal": familiarity_conviction_removal,
                                 "high_distance_accuracy": high_distance_accuracy,
                                 "weight_feature": weight_feature,
                                 "use_case_weights": use_case_weights
                             })

    def simplify_model(self, trainee, num_cases_to_remove, distribute_weight_feature):
        return self._execute("simplify_model",
                             {
                                 "trainee": trainee,
                                 "num_cases_to_remove": num_cases_to_remove,
                                 "distribute_weight_feature": distribute_weight_feature
                             })

    def forget_irrelevant_data(self, trainee, num_cases_to_remove, case_access_count_label, distribute_weight_feature):
        return self._execute("forget_irrelevant_data",
                             {
                                 "trainee": trainee,
                                 "num_cases_to_remove": num_cases_to_remove,
                                 "case_access_count_label": case_access_count_label,
                                 "distribute_weight_feature": distribute_weight_feature
                             })

    def get_session_indices(self, trainee, session):
        return self._execute("get_session_indices",
                             {
                                 "trainee": trainee,
                                 "session": session
                             })

    def get_session_training_indices(self, trainee, session):
        return self._execute("get_session_training_indices",
                             {
                                 "trainee": trainee,
                                 "session": session
                             })

    def set_distance_weight_exponent(self, trainee, distance_weight_exponent):
        return self._execute("set_distance_weight_exponent",
                             {
                                 "trainee": trainee,
                                 "distance_weight_exponent": distance_weight_exponent
                             })

    def set_internal_parameters(self, trainee, hyperparameter_map):
        params = {**{"trainee": trainee}, **hyperparameter_map}
        return self._execute("set_internal_parameters", params)

    def set_feature_attributes(self, trainee, feature_attributes):
        return self._execute("set_feature_attributes",
                             {
                                 "trainee": trainee,
                                 "features": feature_attributes
                             })

    def get_feature_attributes(self, trainee):
        return self._execute("get_feature_attributes", {"trainee": trainee})

    def export_trainee(self, trainee_id,
                       path_to_trainee=None,
                       decode_cases=False,
                       separate_files=False):
        if path_to_trainee is None:
            path_to_trainee = self.default_save_path

        return self._execute("export_trainee",
                             {
                                 "trainee": trainee_id,
                                 "trainee_filepath": f"{path_to_trainee}/",
                                 "root_filepath": f"{self.diveplane_path}/",
                                 "decode_cases": decode_cases,
                                 "separate_files": separate_files
                             })

    def upgrade_trainee(self, trainee_id,
                        path_to_trainee=None,
                        separate_files=False):
        if path_to_trainee is None:
            path_to_trainee = self.default_save_path

        return self._execute("upgrade_trainee",
                             {
                                 "trainee": trainee_id,
                                 "trainee_filepath": f"{path_to_trainee}/",
                                 "root_filepath": f"{self.diveplane_path}/",
                                 "separate_files": separate_files
                             })

    def optimize(self, trainee, **kwargs):
        params = {**kwargs, "trainee": trainee}
        return self._execute("optimize", params)

    def get_feature_residuals(self, trainee_id,
                              action_feature=None,
                              robust=None,
                              robust_hyperparameters=None,
                              weight_feature=None):
        return self._execute("get_feature_residuals",
                             {
                                 "trainee": trainee_id,
                                 "robust": robust,
                                 "action_feature": action_feature,
                                 "robust_hyperparameters": robust_hyperparameters,
                                 "weight_feature": weight_feature,
                             })

    def get_feature_mda(self, trainee_id, action_feature,
                        permutation=None,
                        robust=None,
                        weight_feature=None):
        return self._execute("get_feature_mda",
                             {
                                 "trainee": trainee_id,
                                 "robust": robust,
                                 "action_feature": action_feature,
                                 "permutation": permutation,
                                 "weight_feature": weight_feature,
                             })

    def get_feature_contributions(self, trainee_id, action_feature,
                                  robust=None,
                                  weight_feature=None):
        return self._execute("get_feature_contributions",
                             {
                                 "trainee": trainee_id,
                                 "robust": robust,
                                 "action_feature": action_feature,
                                 "weight_feature": weight_feature,
                             })

    def get_prediction_stats(
        self, trainee_id, *,
        action_feature=None,
        robust=None,
        robust_hyperparameters=None,
        stats=None,
        weight_feature=None
    ):
        return self._execute("get_prediction_stats",
                             {
                                 "trainee": trainee_id,
                                 "robust": robust,
                                 "action_feature": action_feature,
                                 "robust_hyperparameters": robust_hyperparameters,
                                 "stats": stats,
                                 "weight_feature": weight_feature,
                             })

    def get_marginal_stats(self, trainee_id, *, weight_feature=None):
        return self._execute("get_marginal_stats",
                             {
                                 "trainee": trainee_id,
                                 "weight_feature": weight_feature,
                             })

    def react_into_trainee(self, trainee_id,
                           action_feature=None,
                           context_features=None,
                           contributions=None,
                           contributions_robust=None,
                           hyperparameter_param_path=None,
                           mda=None,
                           mda_permutation=None,
                           mda_robust=None,
                           mda_robust_permutation=None,
                           num_samples=None,
                           residuals=None,
                           residuals_robust=None,
                           sample_model_fraction=None,
                           sub_model_size=None,
                           use_case_weights=False,
                           weight_feature=None):
        self._execute("react_into_trainee",
                      {
                          "trainee": trainee_id,
                          "context_features": context_features,
                          "use_case_weights": use_case_weights,
                          "weight_feature": weight_feature,
                          "num_samples": num_samples,
                          "residuals": residuals,
                          "residuals_robust": residuals_robust,
                          "contributions": contributions,
                          "contributions_robust": contributions_robust,
                          "mda": mda,
                          "mda_permutation": mda_permutation,
                          "mda_robust": mda_robust,
                          "mda_robust_permutation": mda_robust_permutation,
                          "hyperparameter_param_path": hyperparameter_param_path,
                          "sample_model_fraction": sample_model_fraction,
                          "sub_model_size": sub_model_size,
                          "action_feature": action_feature
                      })

    def set_random_seed(self, trainee, seed):
        return self._execute("set_random_seed",
                             {
                                 "trainee": trainee,
                                 "seed": seed
                             })

    def get_internal_parameters(self, trainee):
        return self._execute("get_internal_parameters", {"trainee": trainee})

    def move_cases(self, trainee, target_trainee, num_cases=1, *,
                   condition=None, condition_session=None, precision=None,
                   preserve_session_data=False, session=None,
                   distribute_weight_feature=None):
        result = self._execute(
            "move_cases",
            {
                "trainee": trainee,
                "target_trainee": target_trainee,
                "condition": condition,
                "condition_session": condition_session,
                "precision": precision,
                "num_cases": num_cases,
                "preserve_session_data": preserve_session_data,
                "session": session,
                "distribute_weight_feature": distribute_weight_feature
            }
        )
        if not result:
            return {'count': 0}
        return result

    def remove_cases(
        self, trainee, num_cases=1, *, condition=None,
        condition_session=None, precision=None, preserve_session_data=None,
        session=None, distribute_weight_feature=None
    ):
        return self.move_cases(
            trainee,
            target_trainee=None,
            condition=condition,
            condition_session=condition_session,
            num_cases=num_cases,
            precision=precision,
            preserve_session_data=preserve_session_data,
            session=session,
            distribute_weight_feature=distribute_weight_feature
        )

    def edit_cases(
        self, trainee, *, case_indices=None, condition=None,
        condition_session=None, features=None, feature_values=None,
        num_cases=None, precision=None, session=None,
    ):
        result = self._execute(
            "edit_cases",
            {
                "trainee": trainee,
                "case_indices": case_indices,
                "condition": condition,
                "condition_session": condition_session,
                "features": features,
                "feature_values": feature_values,
                "precision": precision,
                "num_cases": num_cases,
                "session": session,
            }
        )
        if not result:
            return {'count': 0}
        return result

    def pairwise_distances(self, trainee_id, *, features=None,
                           action_feature=None, from_case_indices=None,
                           from_values=None, to_case_indices=None,
                           to_values=None, use_case_weights=False,
                           weight_feature=None):
        return self._execute(
            "pairwise_distances",
            {
                "trainee": trainee_id,
                "features": features,
                "action_feature": action_feature,
                "from_case_indices": from_case_indices,
                "from_values": from_values,
                "to_case_indices": to_case_indices,
                "to_values": to_values,
                "weight_feature": weight_feature,
                "use_case_weights": use_case_weights
            })

    def distances(self, trainee_id, *, features=None,
                  action_feature=None, case_indices=None,
                  feature_values=None, weight_feature=None,
                  use_case_weights=False, row_offset=0,
                  row_count=None, column_offset=0,
                  column_count=None):
        return self._execute(
            "distances",
            {
                "trainee": trainee_id,
                "features": features,
                "action_feature": action_feature,
                "case_indices": case_indices,
                "feature_values": feature_values,
                "weight_feature": weight_feature,
                "use_case_weights": use_case_weights,
                "row_offset": row_offset,
                "row_count": row_count,
                "column_offset": column_offset,
                "column_count": column_count,
            })

    def evaluate(self, trainee_id, features_to_code_map, *,
                 aggregation_code=None):
        return self._execute(
            "evaluate",
            {
                "trainee": trainee_id,
                "features_to_code_map": features_to_code_map,
                "aggregation_code": aggregation_code
            })

    def reset_parameter_defaults(self, trainee):
        return self._execute("reset_parameter_defaults", {"trainee": trainee})

    @classmethod
    def _deserialize(cls, payload):
        """Deserialize core response."""
        try:
            deserialized_payload = json.loads(payload)
            if isinstance(deserialized_payload, dict):
                if deserialized_payload.get('status') != 'ok':
                    # If result is an error, raise it
                    errors = deserialized_payload.get('errors') or []
                    if errors:
                        # Raise first error
                        raise DiveplaneError(errors[0].get('detail'))
                    else:
                        # Unknown error occurred
                        raise DiveplaneError('An unknown error occurred while '
                                             'processing the core operation.')

                warning_list = deserialized_payload.get('warnings') or []
                for w in warning_list:
                    warnings.warn(w.get('detail'), category=DiveplaneWarning)

                return deserialized_payload.get('payload')
            return deserialized_payload
        except DiveplaneError:
            raise
        except Exception:  # noqa: Deliberately broad
            raise DiveplaneError('Failed to deserialize the core response.')

    def _get_label(self, label):
        result = self.amlg.get_json_from_label(self.handle, label)
        return result

    def _set_label(self, label, payload):
        payload = sanitize_for_json(payload)
        payload = self._remove_null_entries(payload)
        self.amlg.set_json_to_label(
            self.handle, label, json.dumps(payload))

    def _execute(self, label, payload):
        payload = sanitize_for_json(payload)
        payload = self._remove_null_entries(payload)
        try:
            result = self.amlg.execute_entity_json(
                self.handle, label, json.dumps(payload))
        except ValueError as err:
            raise DiveplaneError(f'Invalid payload - please check for infinity or NaN values: {err}')

        if result is None or len(result) == 0:
            return None
        return self._deserialize(result)

    @staticmethod
    def _remove_null_entries(payload):
        """Remove keys from dict whose value is None."""
        return dict((k, v) for k, v in payload.items() if v is not None)

    @classmethod
    def escape_filename(cls, s):
        escaped = ""
        i = 0
        for i in range(len(s)):
            if cls._is_char_safe(ord(s[i])):
                escaped += s[i]
            else:
                escaped += cls._escape_char(s[i])

        return escaped

    @classmethod
    def unescape_filename(cls, s):
        unescaped = ""
        i = 0
        while i < len(s):
            if s[i] == '_' and (i + 2) < len(s):
                unescaped += cls._char_value_from_escape_hex(
                    s[i + 1], s[i + 2])
                i += 3
            else:
                unescaped += s[i]
                i += 1
        return unescaped

    @staticmethod
    def _is_char_safe(c):
        # UTF-8 chars below zero (U+0030) are unsafe
        if c < 0x30:
            return False
        # Chars between 0 and 9 are ok
        if c <= 0x39:
            return True
        # Chars above 9 (U+0039) and below A (U+0041) are unsafe
        if c < 0x41:
            return False
        # Chars between A and Z are ok
        if c <= 0x5A:
            return True
        # Chars between Z and a (exclusive) are unsafe
        if c < 0x61:
            return False
        # Chars between a and z are ok
        if c <= 0x7A:
            return True

        # Any other char is unsafe
        return False

    @classmethod
    def _escape_char(cls, c):
        low = cls._decimal_to_hex(15 & ord(c))
        high = cls._decimal_to_hex(15 & (ord(c) >> 4))
        return '_' + high + low

    @staticmethod
    def _decimal_to_hex(c):
        if c >= 10:
            return chr(c - 10 + ord('a'))
        return chr(c + ord('0'))

    @classmethod
    def _char_value_from_escape_hex(cls, high, low):
        chr_int_value = cls._hex_to_decimal(low) + (
            (cls._hex_to_decimal(high) << 4) & 240)
        return chr(chr_int_value)

    @staticmethod
    def _hex_to_decimal(c):
        if c >= '0':
            if c <= '9':
                return ord(c) - ord('0')
            if 'a' <= c <= 'f':
                return ord(c) - ord('a') + 10
            if 'A' <= c <= 'F':
                return ord(c) - ord('A') + 10

        # Invalid and possibly unsafe char is not a hex value, return 0 as
        # having no value
        return 0

    @classmethod
    def download_amlg(cls, config):
        """
        Download amalgam binaries.

        Requires the diveplane-build-artifacts dependency.

        Parameters
        ----------
        config : dict
            The amalgam configuration options.

        Returns
        -------
        Path
            The path to the downloaded amalgam directory. Or None if nothing
            was downloaded.
        """
        # Since direct client may be distributed without build downloads ..
        try:
            from diveplane.build.artifacts.repo import DpArtifactService
        except ImportError as err:
            raise ImportError(
                "Amalgam Download functionality only available "
                "if diveplane-build-artifacts is installed"
            ) from err

        if config is None:
            raise ValueError("config may not be None")

        version = config.get('version', 'latest')
        api_key = config.get('download_apikey')
        repo = config.get('repo')

        service_config = {}
        if api_key:
            service_config['DP_ARTIFACTORY_APIKEY'] = api_key
        if repo:
            repo_path = f'{repo}/amalgam/'
            service_config['DP_AMALGAM_DOWNLOAD_PATH'] = repo_path

        service = DpArtifactService(service_config)
        download_dir = service.download_amalgam(
            version=version,
            operating_system=config.get('os'),
            architecture=config.get('arch')
        )

        _logger.info(f'Downloaded amalgam version: {version}')
        return download_dir

    @classmethod
    def download_core(cls, config):
        """
        Download core binaries.

        Requires the diveplane-build-artifacts dependency.

        Parameters
        ----------
        config : dict
            The core configuration options.

        Returns
        -------
        Path
            The path to the downloaded core directory. Or None if nothing
            was downloaded.
        """
        # Since direct client may be distributed without build downloads ..
        try:
            from diveplane.build.artifacts.repo import DpArtifactService
        except ImportError as err:
            raise ImportError(
                "Amalgam Download functionality only available "
                "if diveplane-build-artifacts is installed"
            ) from err

        version = config.pop('version', 'latest')
        api_key = config.pop('download_apikey', None)
        repo = config.get('repo')

        service_config = {}
        if api_key:
            service_config['DP_ARTIFACTORY_APIKEY'] = api_key
        if repo:
            repo_path = f'{repo}/diveplane-core/'
            service_config['DP_CORE_DOWNLOAD_PATH'] = repo_path

        service = DpArtifactService(service_config)
        download_dir = service.download_core(version=version)

        _logger.info(f'Downloaded core version: {version}')
        return download_dir

    @staticmethod
    def default_library_ext():
        """Returns the default library extension based on runtime os."""
        if platform.system().lower() == 'windows':
            return ".dll"
        elif platform.system().lower() == 'darwin':
            return ".dylib"
        else:
            return ".so"
