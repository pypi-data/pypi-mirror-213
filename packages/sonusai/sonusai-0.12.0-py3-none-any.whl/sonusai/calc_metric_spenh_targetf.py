"""sonusai calc_metric_spenh_targetf

usage: calc_metric_spenh_targetf [-hvtpws] [-i MIXID] (-d PLOC) [-e WER] INPUT

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture ID(s) to generate. [default: *].
    -d PLOC, --ploc PLOC        Location of SonusAI predict data.
    -e WER, --wer-method WER    Word-Error-Rate method: deepgram, google, or whisper [default: none]
    -t, --truth-est-mode        Calculate extraction using truth and include metrics.
    -p, --plot                  Enable PDF plots file generation per mixture.
    -w, --wav                   Enable WAV file generation per mixture.
    -s, --summary               Enable summary files generation.

Calculate speech enhancement target_f metrics for prediction data in PLOC and SonusAI mixture database in INPUT.

Inputs:
    PLOC    SonusAI prediction data directory.
    INPUT   SonusAI mixture database directory.

Outputs the following to PLOC:
    <id>_metric_spenh_targetf.txt

    If --plot:
        <id>_metric_spenh_targetf.pdf

    If --wav:
        <id>_target.wav
        <id>_target_est.wav
        <id>_noise.wav
        <id>_noise_est.wav
        <id>_mixture.wav

        If --truth-est-mode:
            <id>_target_truth_est.wav
            <id>_noise_truth_est.wav

    If --summary:
        metric_spenh_targetf_summary.txt
        metric_spenh_targetf_summary.csv
        metric_spenh_targetf_list.csv
        metric_spenh_targetf_estats_list.csv

        If --truth-est-mode:
            metric_spenh_targetf_truth_list.csv
            metric_spenh_targetf_estats_truth_list.csv

"""
from dataclasses import dataclass
from typing import Tuple
from typing import Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sonusai import logger
from sonusai.mixture import AudioF
from sonusai.mixture import AudioT
from sonusai.mixture import Feature
from sonusai.mixture import Location
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict

matplotlib.use('SVG')


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    predict_location: Location = None
    truth_est_mode: bool = None
    enable_plot: bool = None
    enable_wav: bool = None
    wer_method: str = None


MP_GLOBAL = MPGlobal()


def mean_square_error(hypothesis: np.ndarray,
                      reference: np.ndarray,
                      squared: bool = False) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate root mean square error or mean square error

    :param hypothesis: [frames, bins]
    :param reference: [frames, bins]
    :param squared: calculate mean square rather than root mean square
    :return: mean, mean per bin, mean per frame
    """
    sq_err = np.square(reference - hypothesis)

    # mean over frames for value per bin
    err_b = np.mean(sq_err, axis=0)
    # mean over bins for value per frame
    err_f = np.mean(sq_err, axis=1)
    # mean over all
    err = np.mean(sq_err)

    if not squared:
        err_b = np.sqrt(err_b)
        err_f = np.sqrt(err_f)
        err = np.sqrt(err)

    return err, err_b, err_f


def mean_abs_percentage_error(hypothesis: np.ndarray, reference: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate mean abs percentage error

    If inputs are complex, calculates average: mape(real)/2 + mape(imag)/2

    :param hypothesis: [frames, bins]
    :param reference: [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    if not np.iscomplexobj(reference) and not np.iscomplexobj(hypothesis):
        abs_err = 100 * np.abs((reference - hypothesis) / (reference + np.finfo(np.float32).eps))
    else:
        reference_r = np.real(reference)
        reference_i = np.imag(reference)
        hypothesis_r = np.real(hypothesis)
        hypothesis_i = np.imag(hypothesis)
        abs_err_r = 100 * np.abs((reference_r - hypothesis_r) / (reference_r + np.finfo(np.float32).eps))
        abs_err_i = 100 * np.abs((reference_i - hypothesis_i) / (reference_i + np.finfo(np.float32).eps))
        abs_err = (abs_err_r / 2) + (abs_err_i / 2)

    # mean over frames for value per bin
    err_b = np.around(np.mean(abs_err, axis=0), 3)
    # mean over bins for value per frame
    err_f = np.around(np.mean(abs_err, axis=1), 3)
    # mean over all
    err = np.around(np.mean(abs_err), 3)

    return err, err_b, err_f


def log_error(reference: np.ndarray, hypothesis: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate log error

    :param reference: complex or real [frames, bins]
    :param hypothesis: complex or real [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    reference_sq = np.real(reference * np.conjugate(reference))
    hypothesis_sq = np.real(hypothesis * np.conjugate(hypothesis))
    log_err = abs(10 * np.log10((reference_sq + np.finfo(np.float32).eps) / (hypothesis_sq + np.finfo(np.float32).eps)))
    # log_err = abs(10 * np.log10(reference_sq / (hypothesis_sq + np.finfo(np.float32).eps) + np.finfo(np.float32).eps))

    # mean over frames for value per bin
    err_b = np.around(np.mean(log_err, axis=0), 3)
    # mean over bins for value per frame
    err_f = np.around(np.mean(log_err, axis=1), 3)
    # mean over all
    err = np.around(np.mean(log_err), 3)

    return err, err_b, err_f


def plot_mixpred(mixture: AudioT,
                 mixture_f: AudioF,
                 target: AudioT = None,
                 feature: Feature = None,
                 predict: Predict = None,
                 tp_title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE

    num_plots = 2
    if feature is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, mixture, label='Mixture', color='mistyrose')
    ax[0].set_ylabel('magnitude', color='tab:blue')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    if target is not None:  # Plot target time-domain waveform on top of mixture
        ax[0].plot(x_axis, target, label='Target', color='tab:blue')
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[p].set_title('Waveform')

    # Plot the mixture spectrogram
    p += 1
    ax[p].imshow(np.transpose(mixture_f), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Mixture')

    if feature is not None:
        p += 1
        ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Feature')

    if predict is not None:
        p += 1
        ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)

    return fig


def plot_pdb_predtruth(predict: np.ndarray,
                       truth_f: Union[np.ndarray, None] = None,
                       metric: Union[np.ndarray, None] = None,
                       tp_title: str = '') -> plt.figure:
    """Plot predict and optionally truth and a metric in power db, e.g. applies 10*log10(predict)"""
    num_plots = 2
    if truth_f is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    tmp = 10 * np.log10(predict.transpose() + np.finfo(np.float32).eps)
    ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')

    if truth_f is not None:
        p += 1
        tmp = 10 * np.log10(truth_f.transpose() + np.finfo(np.float32).eps)
        ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')

    # Plot the predict avg, and optionally truth avg and metric lines
    pred_avg = 10 * np.log10(np.mean(predict, axis=-1) + np.finfo(np.float32).eps)
    p += 1
    x_axis = np.arange(len(pred_avg), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, pred_avg, color='black', linestyle='dashed', label='Predict mean over freq.')
    ax[p].set_ylabel('mean db', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_f is not None:
        truth_avg = 10 * np.log10(np.mean(truth_f, axis=-1) + np.finfo(np.float32).eps)
        ax[p].plot(x_axis, truth_avg, color='green', linestyle='dashed', label='Truth mean over freq.')

    if metric is not None:  # instantiate 2nd y-axis that shares the same x-axis
        ax2 = ax[p].twinx()
        color2 = 'red'
        ax2.plot(x_axis, metric, color=color2, label='sig distortion (mse db)')
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim([0, np.max(metric)])
        ax2.set_ylabel('spectral distortion (mse db)', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        ax[p].set_title('SNR and SNR mse (mean over freq. db)')
    else:
        ax[p].set_title('SNR (mean over freq. db)')
        # ax[0].tick_params(axis='y', labelcolor=color)
    return fig


def plot_epredtruth(predict: np.ndarray,
                    predict_wav: np.ndarray,
                    truth_f: Union[np.ndarray, None] = None,
                    truth_wav: Union[np.ndarray, None] = None,
                    metric: Union[np.ndarray, None] = None,
                    tp_title: str = '') -> plt.figure:
    """Plot predict spectrogram and waveform and optionally truth and a metric)"""
    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if metric is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    ax[p].imshow(predict.transpose(), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')

    if truth_f is not None:
        p += 1
        ax[p].imshow(truth_f.transpose(), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')

    # Plot the predict wav, and optionally truth avg and metric lines
    p += 1
    x_axis = np.arange(len(predict_wav), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, predict_wav, color='black', linestyle='dashed', label='Speech Estimate')
    ax[p].set_ylabel('Amplitude', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_wav is not None:
        ntrim = len(truth_wav) - len(predict_wav)
        if ntrim > 0:
            truth_wav = truth_wav[0:-ntrim]
        ax[p].plot(x_axis, truth_wav, color='green', linestyle='dashed', label='True Target')

    # Plot the metric lines
    if metric is not None:
        p += 1
        x_axis = np.arange(len(metric), dtype=np.float32)  # / SAMPLE_RATE
        ax[p].plot(x_axis, metric, color='red', label='Target LogErr')
        ax[p].set_ylabel('log error db', color='red')
        ax[p].set_xlim(x_axis[0], x_axis[-1])
        ax[p].set_ylim([-0.01, np.max(metric) + .01])

    return fig


def _process_mixture(mixid: int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py

    from sonusai import SonusAIError
    from sonusai.metrics import calc_pcm
    from sonusai.metrics import calc_pesq
    from sonusai.metrics import calc_sa_sdr
    from sonusai.metrics import calc_wer
    from sonusai.utils import calc_asr
    from sonusai.utils import float_to_int16
    from sonusai.utils import unstack_complex
    from sonusai.utils import write_wav

    mixdb = MP_GLOBAL.mixdb
    predict_location = MP_GLOBAL.predict_location
    truth_est_mode = MP_GLOBAL.truth_est_mode
    enable_plot = MP_GLOBAL.enable_plot
    enable_wav = MP_GLOBAL.enable_wav
    wer_method = MP_GLOBAL.wer_method

    # 1) Collect true target, noise, mixture data
    target = mixdb.mixture_target(mixid)
    target_f = mixdb.mixture_target_f(mixid, target=target)

    noise = mixdb.mixture_noise(mixid)
    noise_f = mixdb.mixture_noise_f(mixid, noise=noise)

    mixture = mixdb.mixture_mixture(mixid, target=target, noise=noise)
    mixture_f = mixdb.mixture_mixture_f(mixid, mixture=mixture)

    feature, truth_f = mixdb.mixture_ft(mixid, mixture=mixture)

    # need to use inv-tf to match size & tf properties
    targetfi = mixdb.inverse_transform(target_f)
    noisefi = mixdb.inverse_transform(noise_f)

    # Test code for tf-based aaware inv transform
    # mcf = np.concatenate([np.expand_dims(target_f,0), np.expand_dims(noise_f,0)],axis=0)
    # ttf = tf_istft_olsa_hanns(mcf, N=mixdb.it_config.N,
    #                           R=mixdb.it_config.R,
    #                           BinStart=mixdb.fg.bin_start,
    #                           BinEnd=mixdb.fg.bin_end)
    # write_wav('tf_target.wav', audio=float_to_int16(ttf[0,:]))
    # write_wav('tf_noise.wav', audio=float_to_int16(ttf[1, :]))
    # to = tf_istft_olsa_hanns(target_f, N=mixdb.it_config.N,
    #                           R=mixdb.it_config.R,
    #                           BinStart=mixdb.fg.bin_start,
    #                           BinEnd=mixdb.fg.bin_end)
    # write_wav('tf_target_only.wav', audio=float_to_int16(to))

    # 2)  Read predict data
    output_name = join(predict_location, mixdb.mixtures[mixid].name)
    base_name = splitext(output_name)[0]
    try:
        with h5py.File(output_name, 'r') as f:
            predict = np.array(f['predict'])
    except Exception as e:
        raise SonusAIError(f'Error reading {output_name}: {e}')

    # 3) Extraction - for target_f truth, simply unstack as predict is estimating the target
    predict_complex = unstack_complex(predict)
    truth_f_complex = unstack_complex(truth_f)
    noise_est_complex = mixture_f - predict_complex
    target_est_wav = mixdb.inverse_transform(predict_complex)
    noise_est_wav = mixdb.inverse_transform(noise_est_complex)

    target_truth_est_complex = None
    target_truth_est_audio = None

    noise_truth_est_complex = None
    noise_truth_est_audio = None

    if truth_est_mode:
        # estimates using truth instead of prediction
        target_truth_est_complex = truth_f_complex
        target_truth_est_audio = mixdb.inverse_transform(target_truth_est_complex)

        noise_truth_est_complex = mixture_f - target_truth_est_complex
        noise_truth_est_audio = mixdb.inverse_transform(noise_truth_est_complex)

    # 4) Metrics
    # Mean absolute percentage error (real and imag)
    # cmape_tg, cmape_tg_bin, cmape_tg_frame = mean_abs_percentage_error(hypothesis=predict_complex,
    #                                                                    reference=truth_f_complex)

    # Target/Speech logerr - PSD estimation accuracy symmetric mean log-spectral distortion
    lerr_tg, lerr_tg_bin, lerr_tg_frame = log_error(truth_f_complex, predict_complex)
    # Noise logerr - PSD estimation accuracy
    lerr_n, lerr_n_bin, lerr_n_frame = log_error(noise_f, noise_est_complex)
    # PCM loss metric
    ytrue_f = np.concatenate((truth_f_complex[:, np.newaxis, :], noise_f[:, np.newaxis, :]), axis=1)
    ypred_f = np.concatenate((predict_complex[:, np.newaxis, :], noise_est_complex[:, np.newaxis, :]), axis=1)
    pcm, pcm_bin, pcm_frame = calc_pcm(hypothesis=ypred_f, reference=ytrue_f, with_log=True)

    # Noise td logerr
    # lerr_nt, lerr_nt_bin, lerr_nt_frame = log_error(noisefi, noise_truth_est_audio)

    # SA-SDR (time-domain source-aggragated SDR)
    ytrue = np.concatenate((targetfi[:, np.newaxis], noisefi[:, np.newaxis]), axis=1)
    ypred = np.concatenate((target_est_wav[:, np.newaxis], noise_est_wav[:, np.newaxis]), axis=1)
    # note: w/o scale is more pessimistic number
    sa_sdr, _ = calc_sa_sdr(hypothesis=ypred, reference=ytrue)

    # Speech intelligibility measure - PESQ
    if int(mixdb.mixtures[mixid].snr) > -99:
        pesq_speech = calc_pesq(hypothesis=target_est_wav, reference=target)
        pesq_mixture = calc_pesq(hypothesis=mixture, reference=target)
        # pesq improvement
        pesq_impr = pesq_speech - pesq_mixture
        # pesq improvement %
        pesq_impr_pc = pesq_impr / (pesq_mixture + np.finfo(np.float32).eps) * 100
    else:
        pesq_speech = 0
        pesq_mixture = 0
        pesq_impr_pc = 0

    # Calc WER
    if wer_method == 'none':
        wer_mx = float('nan')
        wer_tge = float('nan')
        wer_pi = float('nan')
    else:
        # i.e., wer_method ='google'
        asr_tt = calc_asr(target, engine=wer_method)  # target truth
        asr_mx = calc_asr(mixture, engine=wer_method)
        asr_tge = calc_asr(target_est_wav, engine=wer_method)

        tmp = calc_wer(asr_mx.text, asr_tt.text)  # mixture wer
        wer_mx = tmp.wer * 100
        tmp = calc_wer(asr_tge.text, asr_tt.text)  # target estimate wer
        wer_tge = tmp.wer * 100
        wer_pi = (wer_mx - wer_tge) / (wer_mx + 0.1) * 100

    # 5) Save per mixture metric results
    # Single row in table of scalar metrics per mixture
    mtable1_col = ['MXSNR', 'MXPESQ', 'MXWER', 'PESQ', 'PESQi%', 'WER', 'WERi%', 'SASDR', 'PCM', 'SPLERR', 'NLERR',
                   'SPFILE', 'NFILE']
    ti = mixdb.mixtures[mixid].target_file_index[0]
    ni = mixdb.mixtures[mixid].noise_file_index
    metr1 = [mixdb.mixtures[mixid].snr, pesq_mixture, wer_mx, pesq_speech, pesq_impr_pc, wer_tge, wer_pi,
             sa_sdr, pcm, lerr_tg, lerr_n, basename(mixdb.targets[ti].name), basename(mixdb.noises[ni].name)]
    mtab1 = pd.DataFrame([metr1], columns=mtable1_col, index=[mixid])

    # Stats of per frame estimation metrics
    efs_table2_col = ['Max', 'Min', 'Avg', 'Median']
    efs_table2_row = ['PCM', 'SPLERR', 'NLERR']
    metr2 = [[np.max(pcm_frame), np.min(pcm_frame), np.mean(pcm_frame), np.median(pcm_frame)],
             [np.max(lerr_tg_frame), np.min(lerr_tg_frame), np.mean(lerr_tg_frame), np.median(lerr_tg_frame)],
             [np.max(lerr_n_frame), np.min(lerr_n_frame), np.mean(lerr_n_frame), np.median(lerr_n_frame)]]
    mtab2 = pd.DataFrame(metr2, columns=efs_table2_col, index=efs_table2_row)
    mtab2flat_col = ['MXSNR', 'PCM Max', 'PCM Min', 'PCM Avg', 'PCM Median',
                     'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                     'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
    tmp = np.insert(np.array(metr2), 0, mixdb.mixtures[mixid].snr).reshape(1, 13)
    mtab2_flat = pd.DataFrame(tmp, columns=mtab2flat_col, index=[mixid])

    all_metrics_table_1 = mtab1
    all_metrics_table_2 = mtab2_flat

    metric_name = base_name + '_metric_spenh_targetf.txt'
    with open(metric_name, 'w') as f:
        print('Speech enhancement metrics:', file=f)
        print(mtab1.round(2).to_string(), file=f)
        print('', file=f)
        print(f'Extraction statistics over {mixture_f.shape[0]} frames:', file=f)
        print(mtab2.round(2).to_string(), file=f)
        print('', file=f)
        print(f'Target path: {mixdb.targets[ti].name}', file=f)
        print(f'Noise path: {mixdb.noises[ni].name}', file=f)
        # print(f'PESQ improvement: {pesq_impr:0.2f}, {pesq_impr_pc:0.1f}%', file=f)

    lerr_tgtr_frame = None
    lerr_ntr_frame = None
    all_metrics_table_3 = None
    all_metrics_table_4 = None

    if truth_est_mode:
        # cmape_tgtr, cmape_tgtr_bin, cmape_tgtr_frame = mean_abs_percentage_error(hypothesis=target_truth_est_complex,
        #                                                                          reference=truth_f_complex)

        # metrics of estimates using truth instead of prediction
        lerr_tgtr, lerr_tgtr_bin, lerr_tgtr_frame = log_error(truth_f_complex, target_truth_est_complex)
        lerr_ntr, lerr_ntr_bin, lerr_ntr_frame = log_error(noise_f, noise_truth_est_complex)
        ypred_tr_f = np.concatenate((target_truth_est_complex[:, np.newaxis, :],
                                     noise_truth_est_complex[:, np.newaxis, :]), axis=1)
        pcm_tr, pcm_tr_bin, pcm_tr_frame = calc_pcm(hypothesis=ypred_tr_f, reference=ytrue_f, with_log=True)

        # ytrue = np.concatenate((targetfi[:, np.newaxis], noisefi[:, np.newaxis]), axis=1)
        ypred = np.concatenate((target_truth_est_audio[:, np.newaxis], noise_truth_est_audio[:, np.newaxis]), axis=1)
        # scale should be ones
        sa_sdr_tr, opt_scale_tr = calc_sa_sdr(hypothesis=ypred, reference=ytrue, with_scale=True)

        if int(mixdb.mixtures[mixid].snr) > -99:
            pesq_speechtr = calc_pesq(hypothesis=target_truth_est_audio, reference=target)
            # pesq improvement
            pesq_impr_sptr = pesq_speechtr - pesq_mixture
            # pesq improvement %
            pesq_impr_pctr = pesq_impr_sptr / (pesq_mixture + np.finfo(np.float32).eps) * 100
        else:
            pesq_speechtr = 0
            pesq_impr_pctr = 0

        if wer_method == 'none':
            wer_ttge = float('nan')
            wer_tip = float('nan')
        else:
            asr_ttge = calc_asr(target_truth_est_audio, engine=wer_method)
            tmp = calc_wer(asr_ttge.text, asr_tt.text)  # target estimate wer
            wer_ttge = tmp.wer * 100
            wer_tip = (wer_mx - wer_ttge) / (wer_mx + 0.1) * 100

        mtable3_col = ['MXSNR', 'MXPESQ', 'MXWER', 'PESQ', 'PESQi%', 'WER', 'WERi%', 'SASDR', 'PCM', 'SPLERR', 'NLERR']
        metr3 = [mixdb.mixtures[mixid].snr, pesq_mixture, wer_mx, pesq_speechtr, pesq_impr_pctr, wer_ttge,
                 wer_tip, sa_sdr_tr, pcm_tr, lerr_tgtr, lerr_ntr]
        mtab3 = pd.DataFrame([metr3], columns=mtable3_col, index=[mixid])

        # Stats of per frame estimation metrics
        efs_table4_col = ['Max', 'Min', 'Avg', 'Median']
        efs_table4_row = ['PCM', 'SPLERR', 'NLERR']
        metr4 = [[np.max(pcm_tr_frame), np.min(pcm_tr_frame), np.mean(pcm_tr_frame),
                  np.median(pcm_tr_frame)],
                 [np.max(lerr_tgtr_frame), np.min(lerr_tgtr_frame), np.mean(lerr_tgtr_frame),
                  np.median(lerr_tgtr_frame)],
                 [np.max(lerr_ntr_frame), np.min(lerr_ntr_frame), np.mean(lerr_ntr_frame),
                  np.median(lerr_ntr_frame)]]
        mtab4 = pd.DataFrame(metr4, columns=efs_table4_col, index=efs_table4_row)

        # Append extraction metrics to metrics file:
        with open(metric_name, 'a') as f:
            print('', file=f)
            print('Speech enhancement metrics of extraction method using truth:', file=f)
            print(mtab3.round(2).to_string(), file=f)
            print('', file=f)
            print('Extraction (using Truth) statistics over frames:', file=f)
            print(mtab4.round(2).to_string(), file=f)

        # Append to all mixture table
        # mtab4flat_col = ['MXSNR', 'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
        #                  'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
        mtab4flat_col = ['MXSNR', 'PCM Max', 'PCM Min', 'PCM Avg', 'PCM Median',
                         'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                         'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
        # Insert MXSNR
        tmp = np.insert(np.array(metr4), 0, mixdb.mixtures[mixid].snr).reshape(1, 13)
        mtab4_flat = pd.DataFrame(tmp, columns=mtab4flat_col, index=[mixid])

        all_metrics_table_3 = mtab3
        all_metrics_table_4 = mtab4_flat

    # 7) write wav files
    if enable_wav:
        write_wav(name=base_name + '_mixture.wav', audio=float_to_int16(mixture))
        write_wav(name=base_name + '_target_est.wav', audio=float_to_int16(target_est_wav))
        write_wav(name=base_name + '_noise_est.wav', audio=float_to_int16(noise_est_wav))
        write_wav(name=base_name + '_target.wav', audio=float_to_int16(target))
        # write_wav(name=base_name + '_tf_target.wav', audio=float_to_int16(ttf))
        write_wav(name=base_name + '_noise.wav', audio=float_to_int16(noise))
        # debug code to test for perfect reconstruction of the extraction method
        # note both 75% olsa-hanns and 50% olsa-hann modes checked to have perfect reconstruction
        # target_r = mixdb.inverse_transform(target_f)
        # noise_r = mixdb.inverse_transform(noise_f)
        # _write_wav(name=base_name + '_target_r.wav', audio=float_to_int16(target_r))
        # _write_wav(name=base_name + '_noise_r.wav', audio=float_to_int16(noise_r)) # chk perfect rec
        if truth_est_mode:
            write_wav(name=base_name + '_target_truth_est.wav', audio=float_to_int16(target_truth_est_audio))
            write_wav(name=base_name + '_noise_truth_est.wav', audio=float_to_int16(noise_truth_est_audio))

    # 8) Write out plot file
    if enable_plot:
        from matplotlib.backends.backend_pdf import PdfPages
        plot_fname = base_name + '_metric_spenh_targetf.pdf'

        # Reshape feature to eliminate overlap redundancy for easier to understand spectrogram view
        # Original size (frames, stride, num_bands), decimates in stride dimension only if step is > 1
        # Reshape to get frames*decimated_stride, num_bands
        step = int(mixdb.feature_samples / mixdb.feature_step_samples)
        if feature.ndim != 3:
            raise SonusAIError(f'feature does not have 3 dimensions: frames, stride, num_bands')

        # for feature cn*00n**
        feat_sgram = unstack_complex(feature)
        feat_sgram = 20 * np.log10(abs(feat_sgram) + np.finfo(np.float32).eps)
        feat_sgram = feat_sgram[:, -step:, :]  # decimate,  Fx1xB
        feat_sgram = np.reshape(feat_sgram, (feat_sgram.shape[0] * feat_sgram.shape[1], feat_sgram.shape[2]))

        with PdfPages(plot_fname) as pdf:
            # page1 we always have a mixture and prediction, target optional if truth provided
            tfunc_name = mixdb.targets[0].truth_settings[0].function  # first target, assumes all have same
            if tfunc_name == 'mapped_snr_f':
                # leave as unmapped snr
                predplot = predict
                tfunc_name = mixdb.targets[0].truth_settings[0].function
            elif tfunc_name == 'target_f':
                predplot = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            else:
                # use dB scale
                predplot = 10 * np.log10(predict + np.finfo(np.float32).eps)
                tfunc_name = tfunc_name + ' (db)'

            mixspec = 20 * np.log10(abs(mixture_f) + np.finfo(np.float32).eps)
            pdf.savefig(plot_mixpred(mixture=mixture,
                                     mixture_f=mixspec,
                                     target=target,
                                     feature=feat_sgram,
                                     predict=predplot,
                                     tp_title=tfunc_name))

            # ----- page 2, plot unmapped predict, opt truth reconstructed and line plots of mean-over-f
            # pdf.savefig(plot_pdb_predtruth(predict=pred_snr_f, tp_title='predict snr_f (db)'))

            # page 3 speech extraction
            tg_spec = 20 * np.log10(abs(target_f) + np.finfo(np.float32).eps)
            tg_est_spec = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            # n_spec = np.reshape(n_spec,(n_spec.shape[0] * n_spec.shape[1], n_spec.shape[2]))
            pdf.savefig(plot_epredtruth(predict=tg_est_spec,
                                        predict_wav=target_est_wav,
                                        truth_f=tg_spec,
                                        truth_wav=target,
                                        metric=lerr_tg_frame,
                                        tp_title='speech estimate'))

            # page 4 noise extraction
            n_spec = 20 * np.log10(abs(noise_f) + np.finfo(np.float32).eps)
            n_est_spec = 20 * np.log10(abs(noise_est_complex) + np.finfo(np.float32).eps)
            pdf.savefig(plot_epredtruth(predict=n_est_spec,
                                        predict_wav=noise_est_wav,
                                        truth_f=n_spec,
                                        truth_wav=noisefi,
                                        metric=lerr_n_frame,
                                        tp_title='noise estimate'))

            if truth_est_mode:
                # page 5 truth-based speech extraction
                tg_trest_spec = 20 * np.log10(abs(target_truth_est_complex) + np.finfo(np.float32).eps)
                pdf.savefig(plot_epredtruth(predict=tg_trest_spec,
                                            predict_wav=target_truth_est_audio,
                                            truth_f=tg_spec,
                                            truth_wav=target,
                                            metric=lerr_tgtr_frame,
                                            tp_title='truth-based speech estimate'))

                # page 6 truth-based noise extraction
                n_trest_spec = 20 * np.log10(abs(noise_truth_est_complex) + np.finfo(np.float32).eps)
                pdf.savefig(plot_epredtruth(predict=n_trest_spec,
                                            predict_wav=noise_truth_est_audio,
                                            truth_f=n_spec,
                                            truth_wav=noisefi,
                                            metric=lerr_ntr_frame,
                                            tp_title='truth-based noise estimate'))

        plt.close('all')

    return all_metrics_table_1, all_metrics_table_2, all_metrics_table_3, all_metrics_table_4


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    predict_location = args['--ploc']
    wer_method = args['--wer-method'].lower()
    truth_est_mode = args['--truth-est-mode']
    enable_plot = args['--plot']
    enable_wav = args['--wav']
    enable_summary = args['--summary']
    input_name = args['INPUT']

    from os.path import join

    from tqdm import tqdm

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import p_tqdm_map

    # Setup logging file
    create_file_handler(join(predict_location, 'calc_metric_spenh_targetf.log'))
    update_console_handler(verbose)
    initial_log_messages('calc_metric_spenh_targetf')

    mixdb = MixtureDatabase(config=input_name, show_progress=True)
    mixids = mixdb.mixids_to_list(mixids)
    logger.info(f'Found {len(mixids)} mixtures with {mixdb.num_classes} classes from {input_name}')

    mtab_snr_summary_tr = None
    mtab_snr_summary_emtr = None

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.predict_location = predict_location
    MP_GLOBAL.truth_est_mode = truth_est_mode
    MP_GLOBAL.enable_plot = enable_plot
    MP_GLOBAL.enable_wav = enable_wav
    MP_GLOBAL.wer_method = wer_method

    progress = tqdm(total=len(mixids), desc='calc_metric_spenh_targetf')
    all_metrics_tables = p_tqdm_map(_process_mixture, mixids, progress=progress)
    progress.close()

    all_metrics_table_1 = pd.concat([item[0] for item in all_metrics_tables])
    all_metrics_table_2 = pd.concat([item[1] for item in all_metrics_tables])
    if truth_est_mode:
        all_metrics_table_3 = pd.concat([item[2] for item in all_metrics_tables])
        all_metrics_table_4 = pd.concat([item[3] for item in all_metrics_tables])

    if not enable_summary:
        return

    # 9) Done with mixtures, write out summary metrics
    # Calculate SNR summary avg of each non-random snr
    all_mtab1_sorted = all_metrics_table_1.sort_values(by=['MXSNR', 'SPFILE'])
    all_mtab2_sorted = all_metrics_table_2.sort_values(by=['MXSNR'])
    mtab_snr_summary = None
    mtab_snr_summary_em = None
    for snri in range(0, len(mixdb.snrs)):
        tmp = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(numeric_only=True).to_frame().T
        # avoid nan when subset of mixids specified
        if ~np.isnan(tmp.iloc[0].to_numpy()[0]).any():
            mtab_snr_summary = pd.concat([mtab_snr_summary, tmp])

        tmp = all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(numeric_only=True).to_frame().T
        # avoid nan when subset of mixids specified
        if ~np.isnan(tmp.iloc[0].to_numpy()[0]).any():
            mtab_snr_summary_em = pd.concat([mtab_snr_summary_em, tmp])

    # Calculate avg metrics over all mixtures except -99
    all_mtab1_sorted_nom99 = all_mtab1_sorted[all_mtab1_sorted.MXSNR != -99]
    all_nom99_mean = all_mtab1_sorted_nom99.mean(numeric_only=True)

    if truth_est_mode:
        all_mtab3_sorted = all_metrics_table_3.sort_values(by=['MXSNR'])
        all_mtab4_sorted = all_metrics_table_4.sort_values(by=['MXSNR'])
        mtab_snr_summary_tr = all_mtab3_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        mtab_snr_summary_emtr = all_mtab4_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        for snri in range(1, len(mixdb.snrs)):
            mtab_snr_summary_tr = pd.concat([mtab_snr_summary_tr,
                                             all_mtab3_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                 numeric_only=True).to_frame().T])
            mtab_snr_summary_emtr = pd.concat([mtab_snr_summary_emtr,
                                               all_mtab4_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                   numeric_only=True).to_frame().T])

    num_mix = len(mixids)
    if num_mix > 1:
        with open(join(predict_location, 'metric_spenh_targetf_summary.txt'), 'w') as f:
            print(f'Speech enhancement metrics avg over all {len(all_mtab1_sorted_nom99)} non -99 SNR mixtures:',
                  file=f)
            print(all_nom99_mean.to_frame().T.round(2).to_string(), file=f)
            print(f'\nSpeech enhancement metrics avg over each SNR:', file=f)
            print(mtab_snr_summary.round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats avg over each SNR:', file=f)
            print(mtab_snr_summary_em.round(2).to_string(), file=f)
            print('', file=f)

            print(f'Speech enhancement metrics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_1.describe().round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_2.describe().round(2).to_string(), file=f)
            print('', file=f)

            if truth_est_mode:
                print(f'Truth-based speech enhancement metrics avg over each SNR:', file=f)
                print(mtab_snr_summary_tr.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistics stats avg over each SNR:', file=f)
                print(mtab_snr_summary_emtr.round(2).to_string(), file=f)
                print('', file=f)

                print(f'Truth-based speech enhancement metrics stats over all {num_mix} mixtures:', file=f)
                print(all_metrics_table_3.describe().round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistic stats over all {num_mix} mixtures:', file=f)
                print(all_metrics_table_4.describe().round(2).to_string(), file=f)
                print('', file=f)

            print('Speech enhancement metrics all-mixtures list:', file=f)
            print(all_metrics_table_1.round(2).to_string(), file=f)
            print('', file=f)
            print('Extraction statistics all-mixtures list:', file=f)
            print(all_metrics_table_2.round(2).to_string(), file=f)

            # Write summary to .csv file
            csv_name = join(predict_location, 'metric_spenh_targetf_summary.csv')
            header_args = {
                'mode': 'a',
                'encoding': 'utf-8',
                'index': False,
                'header': False,
            }
            table_args = {
                'mode': 'a',
                'encoding': 'utf-8',
            }
            label = f'Speech enhancement metrics stats over {num_mix} mixtures:'
            pd.DataFrame([label]).to_csv(csv_name, **header_args)
            all_metrics_table_1.describe().round(2).to_csv(csv_name, encoding='utf-8')
            pd.DataFrame(['']).to_csv(csv_name, **header_args)

            label = f'Extraction statistics stats over {num_mix} mixtures:'
            pd.DataFrame([label]).to_csv(csv_name, **header_args)
            all_metrics_table_2.describe().round(2).to_csv(csv_name, **table_args)
            pd.DataFrame(['']).to_csv(csv_name, **header_args)

            if truth_est_mode:
                label = 'Speech enhancement metrics of extraction method using truth, stats:'
                pd.DataFrame([label]).to_csv(csv_name, **header_args)
                all_metrics_table_3.describe().round(2).to_csv(csv_name, **table_args)
                pd.DataFrame(['']).to_csv(csv_name, **header_args)

                label = 'Truth extraction statistics stats:'
                pd.DataFrame([label]).to_csv(csv_name, **header_args)
                all_metrics_table_4.describe().round(2).to_csv(csv_name, **table_args)
                pd.DataFrame(['']).to_csv(csv_name, **header_args)

            csv_name = join(predict_location, 'metric_spenh_targetf_list.csv')
            pd.DataFrame(['Speech enhancement metrics list:']).to_csv(csv_name, **header_args)
            all_metrics_table_1.round(2).to_csv(csv_name, **table_args)

            csv_name = join(predict_location, 'metric_spenh_targetf_estats_list.csv')
            pd.DataFrame(['Extraction statistics list:']).to_csv(csv_name, **header_args)
            all_metrics_table_2.round(2).to_csv(csv_name, **table_args)

            if truth_est_mode:
                csv_name = join(predict_location, 'metric_spenh_targetf_truth_list.csv')
                pd.DataFrame(['Speech enhancement metrics list:']).to_csv(csv_name, **header_args)
                all_metrics_table_3.round(2).to_csv(csv_name, **table_args)

                csv_name = join(predict_location, 'metric_spenh_targetf_truth_list.csv')
                pd.DataFrame(['Extraction statistics list:']).to_csv(csv_name, **header_args)
                all_metrics_table_4.round(2).to_csv(csv_name, **table_args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
