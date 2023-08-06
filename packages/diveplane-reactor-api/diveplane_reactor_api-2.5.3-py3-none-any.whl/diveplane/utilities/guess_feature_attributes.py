# Deprecation warning
# This file can be removed after 6.24.2023
# Keeping this here in case someone uses 'from diveplane.utilities.guess_feature_attributes ...'
import warnings

from diveplane.utilities.feature_attributes import infer_feature_attributes


def guess_feature_attributes(*args, **kwargs):
    """Shim the deprecated `guess_feature_attributes` to raise a warning."""
    warnings.warn(
        'guess_feature_attributes is deprecated. Please use '
        'diveplane.utilities.infer_feature_attributes instead. This '
        'compatibility shim will be removed in a future release.',
        DeprecationWarning)

    return infer_feature_attributes(*args, **kwargs)
