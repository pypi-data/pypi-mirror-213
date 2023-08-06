from collections import defaultdict
from doy.utils import smooth_ema, smooth_conv

# TODO: support logging keys at different timescales (e.g. train_loss, eval_loss)
#       and then match them up again for plotting


class Logger:
    def __init__(self, use_wandb=True):
        self.data = defaultdict(list)
        self.use_wandb = use_wandb

    def __call__(self, step, **kwargs):
        assert kwargs
        for k, v in list(kwargs.items()):
            if v is None:
                del kwargs[k]
                continue
            try:
                self.data[k].append(v.item())
            except AttributeError:
                self.data[k].append(v)
        if self.use_wandb:
            import wandb
            wandb.log(data=kwargs, step=step)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, smooth_method="ema", smoothing_p=0.9):
        if smooth_method is None:
            return self[key]
        elif smooth_method == "ema":
            return smooth_ema(self[key], smoothing_p)
        elif smooth_method == "conv":
            return smooth_conv(self[key], smoothing_p)
        else:
            raise ValueError(f"Unknown smoothing method: {smooth_method}")
