from sonusai.mixture.truth_functions.data import Data
from sonusai.mixture.types import Truth


def sed(data: Data) -> Truth:
    import numpy as np
    from pyaaware import SED

    from sonusai import SonusAIError

    if data.config.config is None:
        raise SonusAIError('Truth function SED missing config')

    parameters = ['thresholds']
    for parameter in parameters:
        if 'thresholds' not in data.config.config:
            raise SonusAIError(f'Truth function SED config missing required parameter: {parameter}')

    thresholds = data.config.config['thresholds']
    if not _strictly_decreasing(thresholds):
        raise SonusAIError(f'Truth function SED thresholds are not strictly decreasing: {thresholds}')

    if len(data.target_audio) % data.frame_size != 0:
        raise SonusAIError(f'Number of samples in audio is not a multiple of {data.frame_size}')

    # SED wants 1-based indices
    s = SED(thresholds=thresholds,
            index=data.config.index,
            frame_size=data.frame_size,
            num_classes=data.config.num_classes,
            mutex=data.config.mutex)

    target_audio = data.target_audio / data.config.target_gain
    for offset in data.offsets:
        indices = slice(offset, offset + data.frame_size)
        new_truth = s.execute(data.target_fft.energy_t(target_audio[indices]))
        data.truth[indices] = np.reshape(new_truth, (1, len(new_truth)))

    return data.truth


def _strictly_decreasing(list_to_check: list) -> bool:
    return all(x > y for x, y in zip(list_to_check, list_to_check[1:]))
