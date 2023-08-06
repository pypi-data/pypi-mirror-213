import os
import re

import sonusai

REQUIRED_CONFIGS = [
    'class_balancing',
    'class_balancing_augmentation',
    'class_labels',
    'class_weights_threshold',
    'feature',
    'impulse_responses',
    'noise_augmentations',
    'noise_mix_mode',
    'noises',
    'num_classes',
    'random_snrs',
    'seed',
    'snrs',
    'spectral_masks',
    'target_augmentations',
    'target_level_type',
    'targets',
    'truth_mode',
    'truth_reduction_function',
    'truth_settings',
]
VALID_CONFIGS = REQUIRED_CONFIGS + ['output']
VALID_TRUTH_SETTINGS = ['function', 'config', 'index']
VALID_AUGMENTATIONS = ['normalize', 'gain', 'pitch', 'tempo', 'eq1', 'eq2', 'eq3', 'lpf', 'ir', 'count', 'mixup']
VALID_NOISE_MIX_MODES = ['exhaustive', 'non-exhaustive', 'non-combinatorial']
RAND_PATTERN = re.compile(r'rand\(([-+]?(\d+(\.\d*)?|\.\d+)),\s*([-+]?(\d+(\.\d*)?|\.\d+))\)')
SAMPLE_RATE = 16000
BIT_DEPTH = 32
ENCODING = 'floating-point'
CHANNEL_COUNT = 1
SAMPLE_BYTES = BIT_DEPTH // 8
FLOAT_BYTES = 4

DEFAULT_NOISE = os.path.join(sonusai.BASEDIR, 'data', 'whitenoise.wav')
DEFAULT_CONFIG = os.path.join(sonusai.BASEDIR, 'data', 'genmixdb.yml')
