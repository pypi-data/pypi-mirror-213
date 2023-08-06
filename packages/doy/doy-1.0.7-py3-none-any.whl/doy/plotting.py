from typing import Iterable
import numpy as np
from matplotlib import pyplot as plt


def _plot_subplt(ax, d, auto_ylim):
    """ utility function for plot_grid """
    if isinstance(d[-1], str):
        *d, label = d
        ax.plot(*d, label=label)
        ax.legend()
    else:
        ax.plot(*d)
    q = 0.05
    auto_ylim = (
        # we use the previous bounds & the quantile (to discard outliers) & the most recent point (to avoid cutting it off)
        min(auto_ylim[0], np.quantile(d[-1], q), d[-1][-1] - np.std(d[-1]) * 0.08),
        max(auto_ylim[1], np.quantile(d[-1], 1 - q), d[-1][-1] + np.std(d[-1]) * 0.08),
    )
    return auto_ylim


def plot_grid(
    *data,
    nrows=None,
    ncols=None,
    titles=None,
    yscale=None,
    ylimits=None,
    axes_off=False,
    figsize=None,
    sharex=False,
    sharey=False,
    tight_layout=True
):
    """
    call this as plot_grid(d_1, d_2, ...)

    where d_i is a tuple containing 1-3 elements: ([xs], ys, [label])
    - (optional) a list xs of x values
    - a list ys of y values
    - (optional) a string used as legend label

    alternatively, d_i can also be a list of tuples as described above (for multiple plotted lines per subplots)
    """

    if nrows and ncols:
        assert nrows * ncols == len(data)
    elif nrows:
        assert len(data) % nrows == 0
        ncols = len(data) // nrows
    elif ncols:
        assert len(data) % ncols == 0
        nrows = len(data) // ncols
    else:
        nrows = 1
        ncols = len(data)

    if not figsize:
        k = 4
        figsize = (k * ncols, k * nrows)

    figs, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        squeeze=False,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
    )

    for i, (d, ax) in enumerate(zip(data, axes.reshape(-1))):
        auto_ylim = (float("inf"), float("-inf"))
        if d is not None:
            if isinstance(d[0][0], Iterable):
                # if we have multiple plots in a subplot
                for k in d:
                    auto_ylim = _plot_subplt(ax, k, auto_ylim)
            else:
                auto_ylim = _plot_subplt(ax, d, auto_ylim)
        if axes_off:
            ax.axis("off")
        if titles:
            ax.set_title(titles[i])
        if yscale and yscale[i]:
            ax.set_yscale(yscale[i])
        if ylimits and ylimits[i] is not None:
            # ylimits[i] is (s1, s2) or s1 where s_i is either a scalar, or None, or 'auto' (latter one excludes outliers)

            if not isinstance(ylimits[i], tuple):
                ylimits[i] = (ylimits[i], ylimits[i])

            # to prevent: UserWarning: Attempt to set non-positive ylim on a log-scaled axis will be ignored.
            if yscale and yscale[i] == "log":
                auto_ylim = (max(auto_ylim[0], 0), max(auto_ylim[1], 0))

            # to prevent: UserWarning: Attempting to set identical low and high ylims makes transformation singular; automatically expanding.
            if auto_ylim[0] == auto_ylim[1]:
                auto_ylim = (None, None)

            ylimits[i] = list(ylimits[i])
            for j in range(2):
                if ylimits[i][j] == "auto":
                    ylimits[i][j] = auto_ylim[j]

            ax.set_ylim(bottom=ylimits[i][0], top=ylimits[i][1])

    if tight_layout:
        plt.tight_layout()
    plt.show()


def imshow_grid(
    *images, nrows=None, ncols=None, titles=None, axes_off=True, figsize=None
):
    if nrows and ncols:
        assert nrows * ncols == len(images)
    elif nrows:
        assert len(images) % nrows == 0
        ncols = len(images) // nrows
    elif ncols:
        assert len(images) % ncols == 0
        nrows = len(images) // ncols
    else:
        nrows = 1
        ncols = len(images)

    if not figsize:
        k = 12
        ratio = 1  # 0.25 if titles else 0.2
        figsize = (k * nrows, k * ncols)

    figs, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False, figsize=figsize)

    for i, (im, ax) in enumerate(zip(images, axes.reshape(-1))):
        if im is not None:
            ax.imshow(im, interpolation="nearest")
        if axes_off:
            ax.axis("off")
        if titles:
            ax.set_title(titles[i])

    plt.tight_layout()
    plt.show()
