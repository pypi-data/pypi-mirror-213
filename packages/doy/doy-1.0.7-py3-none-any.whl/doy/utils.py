import numpy as np


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def mappend(lists, values):
    for l, v in zip(lists, values):
        l.append(v)


def lerp(a, b, alpha=0.9):
    return alpha * a + (1 - alpha) * b


def smooth_ema(X, alpha=0.9):
    assert 0 <= alpha < 1
    if len(X) == 0:
        return X
    res = []
    z = X[0]
    for x in X:
        z = lerp(z, x, alpha)
        res.append(z)
    return np.array(res)


def smooth_conv(X, box_pts, mode="valid"):
    assert isinstance(box_pts, int)
    if len(X) == 0:
        return X
    box = np.ones(box_pts) / box_pts
    X_smooth = np.convolve(X, box, mode=mode)
    return X_smooth


def bchw_to_bhwc(x):
    assert len(x.shape) == 4
    if isinstance(x, np.ndarray):
        return x.transpose(0, 2, 3, 1)
    else:
        return x.permute(0, 2, 3, 1)


def bhwc_to_bchw(x):
    assert len(x.shape) == 4
    if isinstance(x, np.ndarray):
        return x.transpose(0, 3, 1, 2)
    else:
        return x.permute(0, 3, 1, 2)


def count_parameters(model, requires_grad_only=True):
    return sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad or not requires_grad_only
    )
