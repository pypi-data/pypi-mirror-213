import numpy as np
from lspopt import spectrogram_lspopt
from matplotlib.colors import Normalize


def plot_spectrogram(fig, ax, eeg, sf=500, win=15, freq_band=(0.5, 35), cmap="RdBu_r", trim_percentage=5):
    cmap = "Spectral_r"
    assert isinstance(eeg, np.ndarray), "Data must be a 1D NumPy array."
    assert isinstance(sf, (int, float)), "sf must be int or float."
    assert eeg.ndim == 1, "Data must be a 1D (single-channel) NumPy array."
    assert isinstance(win, (int, float)), "win_sec must be int or float."
    assert isinstance(freq_band, tuple) and freq_band.__len__() == 2, "freq_band must be tuple with 2 numbers."
    assert isinstance(freq_band[0], (int, float)), "freq[0] must be int or float."
    assert isinstance(freq_band[1], (int, float)), "freq[1] must be int or float."
    assert freq_band[0] < freq_band[1], "fmin must be strictly inferior to fmax."
    assert freq_band[1] < sf / 2, "fmax must be less than Nyquist (sf / 2)."
    # assert isinstance(vmin, (int, float, type(None))), "vmin must be int, float, or None."
    # assert isinstance(vmax, (int, float, type(None))), "vmax must be int, float, or None."

    nperseg = int(win * sf)
    assert eeg.size > 2 * nperseg, "Data length must be at least 2 * win_sec."
    f, t, Sxx = spectrogram_lspopt(eeg, sf, nperseg=nperseg, noverlap=0)
    Sxx = 10 * np.log10(Sxx)  # Convert uV^2 / Hz --> dB / Hz

    # Select only relevant frequencies (up to 30 Hz)
    good_freqs = np.logical_and(f >= freq_band[0], f <= freq_band[1])
    Sxx = Sxx[good_freqs, :]
    f = f[good_freqs]
    t /= 3600  # Convert t to hours

    vmin, vmax = np.percentile(Sxx, [0 + trim_percentage, 100 - trim_percentage])
    norm = Normalize(vmin=vmin, vmax=vmax)
    im = ax.pcolormesh(t, f, Sxx, norm=norm, cmap=cmap, antialiased=True, shading="auto")
    ax.set_xlim(0, t.max())
    ax.set_ylim([0, 35])
    ax.set_yticks([5, 10, 15, 20, 25, 30, 35])

    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_ylabel("Frequency [Hz]", fontdict={"fontsize": 16})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 16})

    return fig, ax, im


def plot_avg_diff_acc(fig, ax, acc, sf=50, win=15):
    assert acc.shape[0] == 3, "ACC should be a 3-D ndarray"
    assert acc.shape[1] % (win * sf) == 0, "The ACC length should be divisible by the epoch length"

    diff_acc = np.abs(acc[:, 1:] - acc[:, 0:-1])
    diff_acc = np.c_[diff_acc, [0, 0, 0]]

    avg_diff_acc = np.sum(np.reshape(np.sum(diff_acc, axis=0), [-1, sf * win]), axis=1) / (sf * win)
    # set max diff acc to 500
    avg_diff_acc[avg_diff_acc > 500] = 500
    data_length = avg_diff_acc.shape[0]

    t = np.arange(data_length) * win / 3600
    ax.plot(t, avg_diff_acc, lw=1.5, color='r')
    ax.set_xlim(0, t.max())
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_ylabel("Avg Diff ACC", fontdict={"fontsize": 16})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 16})
    return fig, ax


def plot_sleep_staging_result(fig, ax, hypno, sleep_variables, win=15):
    assert len(hypno.shape) == 1, "Hypno should be a 1-D array"

    t = np.arange(hypno.size) * win / 3600
    deep_sleep = np.ma.masked_not_equal(hypno, 0)
    light_sleep = np.ma.masked_not_equal(hypno, 1)
    rem_sleep = np.ma.masked_not_equal(hypno, 2)
    wake = np.ma.masked_not_equal(hypno, 3)
    abnormal = np.ma.masked_not_equal(hypno, 4)
    if sleep_variables is not None:
        sl = sleep_variables["SOL"]
        arousal_time = sleep_variables["ART"]
        if sl > 0:
            ax.axvline(x=sl/3600, color="r", lw=1, linestyle='--')
            ax.text(sl/3600, 4.2, 'SL', fontsize=16, color='r', ha='left', va='bottom')
            ax.axvspan(0, sl/3600, color='gray', alpha=0.5)
        if arousal_time.shape[0] > 0:
            arousal_time = np.asarray(arousal_time)
            b = np.insert(arousal_time, 0, 0)
            diff = b[1:] - b[:-1]
            c = arousal_time[np.where(diff != 1)[0]]
            d = np.append(arousal_time, 0)
            diff = d[1:] - d[:-1]
            e = arousal_time[np.where(diff != 1)[0]]
            boundaries = np.transpose(np.vstack([c, e]))
            for i in range(boundaries.shape[0]):
                # ax.axvline(x=boundaries[i][0]*win/3600, color="r", lw=1, linestyle='--')
                # ax.axvline(x=boundaries[i][1]*win/3600, color="r", lw=1, linestyle='--')
                # ax.text(boundaries[i][1]*win/3600, 4.2, 'Arousal {}'.format(i), fontsize=12, color='r', ha='center', va='bottom')
                ax.axvspan(boundaries[i][0]*win/3600, boundaries[i][1]*win/3600, color='gray', alpha=0.5)
            ax.text(t.max()*0.98, 4.2, "Arousals: {}s in {} times".format(arousal_time.shape[0]*win, boundaries.shape[0]), fontsize=12, color='r', ha='right', va='bottom')
    ax.step(t, hypno, lw=2, color='k')
    ax.step(t, abnormal, lw=2, color='k')
    ax.step(t, wake, lw=2, color='orange')
    ax.step(t, rem_sleep, lw=2, color='lime')
    ax.step(t, light_sleep, lw=2, color='deepskyblue', )
    ax.step(t, deep_sleep, lw=2, color='royalblue')

    ax.set_xlim(0, t.max())
    ax.set_ylim([-0.1, 4.8])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_yticklabels(['Deep Sleep', 'Light Sleep', 'REM Sleep', 'Wake', 'Abnormal'], )
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_ylabel("Sleep Staging Result", fontdict={"fontsize": 16})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 16})


    return fig, ax
