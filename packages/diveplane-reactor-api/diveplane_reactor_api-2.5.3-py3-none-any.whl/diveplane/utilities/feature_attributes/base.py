from abc import ABC, abstractmethod
from collections.abc import Container
from copy import deepcopy
import json
import logging
import numbers
from typing import (
    Any, Collection, Dict, Iterable, List, Mapping, Optional, Tuple, Union
)
import warnings

from diveplane.utilities.features import FeatureType
from diveplane.utilities.internals import serialize_openapi_models
import numpy as np


logger = logging.getLogger(__name__)


class FeatureAttributesBase(dict):
    """Provides accessor methods for and dict-like access to inferred feature attributes."""

    def __init__(self, feature_attributes, params):
        """Instantiate this FeatureAttributesBase object."""
        self.params = params
        self.update(feature_attributes)

    def __copy__(self) -> "FeatureAttributesBase":
        """Return a (deep)copy of this instance of FeatureAttributesBase."""
        cls = self.__class__
        obj_copy = cls.__new__(cls)
        obj_copy.update(deepcopy(self))
        obj_copy.params = self.params
        return obj_copy

    def get_parameters(self) -> dict:
        """
        Get the keyword arguments used with the initial call to infer_feature_attributes.

        Returns
        -------
        Dict
            A dictionary containing the kwargs used in the call to `infer_feature_attributes`.

        """
        return self.params

    def to_json(self) -> str:
        """
        Get a JSON string representation of this FeatureAttributes object.

        Returns
        -------
        String
            A JSON representation of the inferred feature attributes.
        """
        return json.dumps(self)

    def get_names(self, *, types: Union[str, Container] = None,
                  without: Iterable[str] = None
                  ) -> List[str]:
        """
        Get feature names associated with this FeatureAttributes object.

        Parameters
        ----------
        types : String, Container (of String), default None
            (Optional) A feature type as a string (E.g., 'continuous') or a
            list of feature types to limit the output feature names.
        without : Iterable of String
            (Optional) An Iterable of feature names to exclude from the return object.

        Returns
        -------
        List of String
            A list of feature names.
        """
        if without:
            for feature in without:
                if feature not in self.keys():
                    raise ValueError(f'Feature {feature} does not exist in this FeatureAttributes '
                                     'object')
        names = self.keys()

        if types:
            if isinstance(types, str):
                types = [types, ]
            names = [
                name for name in names
                if self[name].get('type') in types
            ]

        return [
            key for key in names
            if without is None or key not in without
        ]


class MultiTableFeatureAttributes(FeatureAttributesBase):
    """A dict-like object containing feature attributes for multiple tables."""

    pass


class SingleTableFeatureAttributes(FeatureAttributesBase):
    """A dict-like object containing feature attributes for a single table or DataFrame."""

    pass


class InferFeatureAttributesBase(ABC):
    """
    This is an abstract Feature Attributes inferrer base class.

    It is agnostic to the type of data being inspected.
    """

    def _process(self,  # noqa: C901
                 features: Optional[Dict[str, Dict]] = None,
                 infer_bounds: bool = True,
                 dropna: bool = False,
                 tight_bounds: bool = False,
                 tight_bound_features: Optional[Iterable[str]] = None,
                 mode_bound_features: Optional[Iterable[str]] = None,
                 id_feature_name: Optional[Union[str, Iterable[str]]] = None,
                 attempt_infer_extended_nominals: bool = False,
                 nominal_substitution_config: Optional[Dict[str, Dict]] = None,
                 include_extended_nominal_probabilities: Optional[bool] = False,
                 datetime_feature_formats: Optional[Dict] = None,
                 ordinal_feature_values: Optional[Dict[str, List[str]]] = None,
                 dependent_features: Optional[Dict[str, List[str]]] = None,
                 ) -> Dict:
        """
        Get inferred feature attributes for the parameters.

        See `infer_feature_attributes` for full docstring.
        """
        if features and not isinstance(features, dict):
            raise ValueError(
                f"The parameter `features` needs to be a `dict` and not of "
                f"type {type(features)}."
            )

        if features:
            feature_attributes: Dict = serialize_openapi_models(features)
        else:
            feature_attributes = dict()

        if datetime_feature_formats is None:
            datetime_feature_formats = dict()

        if ordinal_feature_values is None:
            ordinal_feature_values = dict()

        if dependent_features is None:
            dependent_features = dict()

        feature_names_list = self._get_feature_names()
        for feature_name in feature_names_list:
            # What type is this feature?
            feature_type, typing_info = self._get_feature_type(feature_name)

            # EXPLICITLY DECLARED ORDINALS
            if feature_name in ordinal_feature_values:
                feature_attributes[feature_name] = {
                    'type': 'ordinal',
                    'bounds': {'allowed': ordinal_feature_values[feature_name]}
                }

            # EXPLICITLY DECLARED DATETIME FEATURES
            elif datetime_feature_formats.get(feature_name, None):
                # datetime_feature_formats is expected to either be only a
                # single string (format) or a tuple of strings (format, locale)
                user_dt_format = datetime_feature_formats[feature_name]
                if features and 'date_time_format' in features.get(feature_name, {}):
                    warnings.warn(f'Warning: date_time_format for {feature_name} '
                                  'provided in both `features` (ignored) and '
                                  '`datetime_feature_formats`.')
                    del features[feature_name]['date_time_format']

                if feature_type == FeatureType.DATETIME:
                    # When feature is a datetime instance, we won't need to
                    # parse the datetime from a string using a custom format.
                    feature_attributes[feature_name] = (
                        self._infer_datetime_attributes(feature_name))
                    warnings.warn(
                        'Providing a datetime feature format for the feature '
                        f'"{feature_name}" is not necessary because the data '
                        'is already formatted as a datetime object. This '
                        'custom format will be ignored.')
                elif feature_type == FeatureType.DATE:
                    # When feature is a date instance, we won't need to
                    # parse the datetime from a string using a custom format.
                    feature_attributes[feature_name] = (
                        self._infer_date_attributes(feature_name))
                    warnings.warn(
                        'Providing a datetime feature format for the feature '
                        f'"{feature_name}" is not necessary because the data '
                        'is already formatted as a date object. This custom '
                        'format will be ignored.')
                elif feature_type == FeatureType.TIME:
                    # When feature is a time instance, we won't need to
                    # parse the datetime from a string using a custom format.
                    feature_attributes[feature_name] = (
                        self._infer_datetime_attributes(feature_name))
                    warnings.warn(
                        'Time only features with a datetime feature format '
                        'will be treated as a datetime using the date '
                        '1970-1-1.', UserWarning)
                elif isinstance(user_dt_format, str):
                    # User passed only the format string
                    feature_attributes[feature_name] = {
                        'type': 'continuous',
                        'date_time_format': user_dt_format,
                    }
                elif (
                    isinstance(user_dt_format, Collection) and
                    len(user_dt_format) == 2
                ):
                    # User passed format string and a locale string
                    dt_format, dt_locale = user_dt_format
                    feature_attributes[feature_name] = {
                        'type': 'continuous',
                        'date_time_format': dt_format,
                        'locale': dt_locale,
                    }
                else:
                    # Not really sure what they passed.
                    raise TypeError(
                        f'The value passed (`{user_dt_format}`) to '
                        f'`datetime_feature_formats` for feature "{feature_name}"'
                        f'is invalid. It should be either a single string '
                        f'(format), or a tuple of 2 strings (format, locale).')

            # FLOATING POINT FEATURES
            elif feature_type == FeatureType.NUMERIC:
                feature_attributes[feature_name] = (
                    self._infer_floating_point_attributes(feature_name))

            # IMPLICITLY DEFINED DATETIME FEATURES
            elif feature_type == FeatureType.DATETIME:
                feature_attributes[feature_name] = (
                    self._infer_datetime_attributes(feature_name))

            # DATE ONLY FEATURES
            elif feature_type == FeatureType.DATE:
                feature_attributes[feature_name] = (
                    self._infer_date_attributes(feature_name))

            # TIME ONLY FEATURES
            elif feature_type == FeatureType.TIME:
                feature_attributes[feature_name] = (
                    self._infer_time_attributes(feature_name))

            # TIMEDELTA FEATURES
            elif feature_type == FeatureType.TIMEDELTA:
                feature_attributes[feature_name] = (
                    self._infer_timedelta_attributes(feature_name))

            # INTEGER FEATURES
            elif feature_type == FeatureType.INTEGER:
                feature_attributes[feature_name] = (
                    self._infer_integer_attributes(feature_name))

            # BOOLEAN FEATURES
            elif feature_type == FeatureType.BOOLEAN:
                feature_attributes[feature_name] = (
                    self._infer_boolean_attributes(feature_name))

            # ALL OTHER FEATURES
            else:
                feature_attributes[feature_name] = (
                    self._infer_string_attributes(feature_name))

            # Is column constrained to be unique?
            if self._has_unique_constraint(feature_name):
                feature_attributes[feature_name]['unique'] = True

            # Add original type to feature
            if feature_type is not None:
                feature_attributes[feature_name]['original_type'] = {
                    'data_type': str(feature_type),
                    **typing_info
                }

            # DECLARED DEPENDENTS
            # First determine if there are any dependent features in the partial features dict
            partial_dependent_features = []
            if features and 'dependent_features' in features.get(feature_name, {}):
                partial_dependent_features = features[feature_name]['dependent_features']
            # Set dependent features: `dependent_features` + partial features dict, if provided
            if feature_name in dependent_features:
                feature_attributes[feature_name]['dependent_features'] = list(
                    set(partial_dependent_features + dependent_features[feature_name])
                )

        if isinstance(id_feature_name, str):
            self._add_id_attribute(feature_attributes, id_feature_name)
        elif isinstance(id_feature_name, Iterable):
            for id_feature in id_feature_name:
                self._add_id_attribute(feature_attributes, id_feature)
        elif id_feature_name is not None:
            raise ValueError('ID feature must be of type `str` or `list[str], '
                             f'not {type(id_feature_name)}.')

        if infer_bounds:
            for feature_name in feature_attributes:
                bounds = self._infer_feature_bounds(
                    feature_attributes, feature_name,
                    tight_bounds=tight_bounds,
                    tight_bound_features=tight_bound_features,
                    mode_bound_features=mode_bound_features,
                )
                if bounds:
                    feature_attributes[feature_name]['bounds'] = bounds  # noqa

        if dropna:
            for feature_name in feature_attributes:
                if 'dropna' in feature_attributes[feature_name]:
                    # Don't override user's preference
                    continue
                feature_attributes[feature_name]['dropna'] = True  # noqa

        # If requested, infer extended nominals.
        if attempt_infer_extended_nominals:
            # Attempt to import the NominalDetectionEngine.
            try:
                from diveplane.nominal_substitution import (
                    NominalDetectionEngine,
                )
                # Grab whether the user wants the probabilities saved in the feature
                # metadata.
                include_meta = include_extended_nominal_probabilities

                # Get the assigned extended nominal probabilities (aenp) and all
                # probabilities.
                nde = NominalDetectionEngine(nominal_substitution_config)
                aenp, all_probs = nde.detect(self.data)

                nominal_default_subtype = 'int-id'
                # Apply them if they are above the threshold value.
                for feature_name in feature_names_list:
                    if feature_name in aenp:
                        if len(aenp[feature_name]) > 0:
                            feature_attributes[feature_name]['subtype'] = (max(
                                aenp[feature_name], key=aenp[feature_name].get))

                        if include_meta:
                            feature_attributes[feature_name].update({
                                'extended_nominal_probabilities':
                                    all_probs[feature_name]
                            })

                    # If `subtype` is a nominal feature, assign it to 'int-id'
                    if (
                        feature_attributes[feature_name]['type'] == 'nominal' and
                        not feature_attributes[feature_name].get('subtype', None)
                    ):
                        feature_attributes[feature_name]['subtype'] = (
                            nominal_default_subtype)
            except ImportError:
                warnings.warn('Cannot infer extended nominals: not supported')

        # Re-insert any partial features provided as an argument
        if features:
            for feature in features.keys():
                for attribute, value in features[feature].items():
                    feature_attributes[feature][attribute] = value

        return feature_attributes

    @abstractmethod
    def __call__(self) -> FeatureAttributesBase:
        """Process and return the feature attributes."""

    @abstractmethod
    def _infer_floating_point_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given floating-point column."""

    @abstractmethod
    def _infer_datetime_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given date-time column."""

    @abstractmethod
    def _infer_date_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given date only column."""

    @abstractmethod
    def _infer_time_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given time column."""

    @abstractmethod
    def _infer_timedelta_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given timedelta column."""

    @abstractmethod
    def _infer_boolean_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given boolean column."""

    @abstractmethod
    def _infer_integer_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given integer column."""

    @abstractmethod
    def _infer_string_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given string column."""

    @abstractmethod
    def _infer_unknown_attributes(self, feature_name: str) -> Dict:
        """Get inferred attributes for the given unknown-type column."""

    @abstractmethod
    def _infer_feature_bounds(
        self,
        feature_attributes: Mapping[str, Mapping],
        feature_name: str,
        tight_bounds: bool = False,
        tight_bound_features: Optional[Iterable[str]] = None,
        mode_bound_features: Optional[Iterable[str]] = None,
    ) -> Optional[Dict]:
        """
        Return inferred bounds for the given column.

        Features with datetimes are converted to seconds since epoch and their
        bounds are calculated accordingly. Features with timedeltas are
        converted to total seconds.

        Parameters
        ----------
        data : Any
            Input data
        feature_attributes : dict
            A dictionary of feature names to a dictionary of parameters.
        feature_name : str
            The name of feature to infer bounds for.
        tight_bounds: bool, default False
            If True, will set tight min and max bounds on all continuous
            features.
        tight_bound_features : list of str, optional
            Explicit list of feature names that should have tight bounds.
        mode_bound_features : list of str, optional
            Explicit list of feature names that should use mode bounds. When
            None, uses all features.

        Returns
        -------
        dict or None
            Dictionary of bounds for the specified feature, or None if no
            bounds.
        """

    @staticmethod
    def infer_loose_feature_bounds(min_bound: Union[int, float],
                                   max_bound: Union[int, float]
                                   ) -> Tuple[float, float]:
        """
        Infer the loose bound values given a tight min and max bound value.

        Parameters
        ----------
        min_bound : int or float
            The minimum value in a dataset for a feature, must be equal to or less
            than the max value
        max_bound : int or float
            The maximum value in a dataset for a feature, must be equal to or more
            than the min value

        Returns
        -------
        Tuple of (min_bound, max_bound) of loose bounds around the provided tight
        min and max_bound bounds
        """
        # NOTE: It was considered to use a smoother bounds-expansion function that
        #       looked like max_loose_bounds = exp(ln(max_bounds) + 0.5), but this
        #       could leak privacy since the actual bounds would be
        #       reverse-engineer-able.
        assert min_bound <= max_bound, \
            "Feature min_bound cannot be larger than max_bound"

        if min_bound < 0:
            # for negative min_bound boundary values:  e^ceil(ln(num))
            min_bound = -np.exp(np.ceil(np.log(-min_bound)))
        elif min_bound > 0:
            # for positive min_bound boundary values:  e^floor(ln(num))
            min_bound = np.exp(np.floor(np.log(min_bound)))

        if max_bound < 0:
            # for negative max_bound boundary values: e^floor(ln(num))
            max_bound = -np.exp(np.floor(np.log(-max_bound)))
        elif max_bound > 0:
            # for positive max_bound boundary values: e^ceil(ln(num))
            max_bound = np.exp(np.ceil(np.log(max_bound)))

        return min_bound, max_bound

    @staticmethod
    def _add_id_attribute(feature_attributes: Mapping,
                          id_feature_name: str
                          ) -> None:
        """Update the given feature_attributes in-place for id_features."""
        if id_feature_name in feature_attributes:
            feature_attributes[id_feature_name]['id_feature'] = True
            # If id feature was inferred to be continuous, change it to nominal
            # with 'data_type':number attribute to prevent string conversion.
            if feature_attributes[id_feature_name]['type'] == 'continuous':
                feature_attributes[id_feature_name]['type'] = 'nominal'
                feature_attributes[id_feature_name]['data_type'] = 'number'
                if 'decimal_places' in feature_attributes[id_feature_name]:
                    del feature_attributes[id_feature_name]['decimal_places']

    @classmethod
    def _get_min_max_number_size_bounds(
        cls, feature_attributes: Mapping,
        feature_name: str
    ) -> Tuple[Optional[numbers.Number], Optional[numbers.Number]]:
        """
        Get the minimum and maximum size bounds for a numeric feature.

        The minimum and maximum value is based on the storage size of the
        number obtained from the "original_type" feature attribute, i.e. for a
        8bit integer: min=-128, max=127.

        .. NOTE::
            Bounds will not be returned for 64bit floats since this is the
            maximum supported numeric size, so no bounds are necessary.

        Parameters
        ----------
        feature_attributes : dict
            A dictionary of feature names to a dictionary of parameters.
        feature_name : str
            The name of feature.

        Returns
        -------
        Number or None
            The minimum size.
        Number or None
            The maximum size.
        """
        try:
            original_type = feature_attributes[feature_name]['original_type']
        except (TypeError, KeyError):
            # Feature not found or original typing info not defined
            return None, None

        min_value = None
        max_value = None
        if original_type and original_type.get('size'):
            size = original_type.get('size')
            data_type = original_type.get('data_type')

            if size in [1, 2, 4, 8]:
                if data_type == FeatureType.INTEGER.value:
                    if original_type.get('unsigned'):
                        dtype_info = np.iinfo(f'uint{size * 8}')
                    else:
                        dtype_info = np.iinfo(f'int{size * 8}')
                elif data_type == FeatureType.NUMERIC.value and size < 8:
                    dtype_info = np.finfo(f'float{size * 8}')
                else:
                    # Not a numeric feature or is 64bit float
                    return None, None

                min_value = dtype_info.min
                max_value = dtype_info.max
            elif size == 3 and data_type == FeatureType.INTEGER.value:
                # Some database dialects support 24bit integers
                if original_type.get('unsigned'):
                    min_value = 0
                    max_value = 16777215
                else:
                    min_value = -8388608
                    max_value = 8388607

        return min_value, max_value

    @abstractmethod
    def _get_feature_type(self, feature_name: str
                          ) -> Tuple[Optional[FeatureType], Optional[Dict]]:
        """
        Return the type information for a given feature.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get the type of

        Returns
        -------
        FeatureType or None
            The feature type or None if the column could not be found.
        Dict or None
            Additional typing information about the feature or None if the
            column could not be found.
        """

    @abstractmethod
    def _has_unique_constraint(self, feature_name: str) -> bool:
        """Return whether this feature has a unique constraint."""

    @abstractmethod
    def _get_first_non_null(self, feature_name: str) -> Optional[Any]:
        """
        Get the first non-null value in the given column.

        NOTE: "first" means arbitrarily the first one that the DataFrame or database
              returned; there is no implication of ordering.
        """

    @abstractmethod
    def _get_num_features(self) -> int:
        """Get the number of features/columns in the data."""

    @abstractmethod
    def _get_num_cases(self) -> int:
        """Get the number of cases/rows in the data."""

    @abstractmethod
    def _get_feature_names(self) -> List[str]:
        """Get the names of the features/columns of the data."""
