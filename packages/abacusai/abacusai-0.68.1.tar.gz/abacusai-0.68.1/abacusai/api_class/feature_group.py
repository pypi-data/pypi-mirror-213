import dataclasses
from typing import List

from . import enums
from .abstract import ApiClass, _ApiClassFactory


@dataclasses.dataclass
class SamplingConfig(ApiClass):
    """
    An abstract class for the sampling config of a feature group
    """
    def __post_init__(self):
        if self.__class__ == SamplingConfig:
            raise TypeError('Cannot instantiate abstract SamplingConfig class.')


@dataclasses.dataclass
class NSamplingConfig(SamplingConfig):
    """
    The number of distinct values of the key columns to include in the sample, or number of rows if key columns not specified.

    Args:
        sampling_method (SamplingMethodType): N_SAMPLING
        sample_count (int): The number of rows to include in the sample
        key_columns (list[str]): The feature(s) to use as the key(s) when sampling
    """
    sample_count: int
    key_columns: List[str] = dataclasses.field(default_factory=list)
    sampling_method: enums.SamplingMethodType = enums.SamplingMethodType.N_SAMPLING


@dataclasses.dataclass
class PercentSamplingConfig(SamplingConfig):
    """
    The fraction of distinct values of the feature group to include in the sample.

    Args:
        sampling_method (SamplingMethodType): PERCENT_SAMPLING
        sample_percent (float): The percentage of the rows to sample
        key_columns (list[str]): The feature(s) to use as the key(s) when sampling
    """
    sample_percent: float
    key_columns: List[str] = dataclasses.field(default_factory=list)
    sampling_method: enums.SamplingMethodType = enums.SamplingMethodType.PERCENT_SAMPLING


@dataclasses.dataclass
class _SamplingConfigFactory(_ApiClassFactory):
    config_class_key = 'sampling_method'
    config_class_map = {
        enums.SamplingMethodType.N_SAMPLING: NSamplingConfig,
        enums.SamplingMethodType.PERCENT_SAMPLING: PercentSamplingConfig,
    }
