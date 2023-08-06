from .rich_utils import track
import rich, rich.console, rich.progress, rich.status
from tqdm.auto import tqdm, trange
import time
import builtins
from contextlib import contextmanager

_mode = None
_rich_console = None


def config_progress_backend(mode="rich"):  # rich | tqdm | fallback
    assert mode in ("rich", "tqdm", "fallback")
    global _mode
    _mode = mode
    if mode == "rich":
        global _rich_console
        _rich_console = rich.console.Console()


def _init_check():
    if _mode is None:
        config_progress_backend()


def print(*args, **kwargs):
    _init_check()
    if _mode == "rich":
        _rich_console.print(*args, **kwargs)
    else:
        builtins.print(*args, **kwargs)


def log(*args, **kwargs):
    if _mode == "rich":
        _rich_console.log(*args, **kwargs)
    else:
        builtins.print(*args, **kwargs)


def loop(*args, desc=None, desc_align=25):
    _init_check()

    if desc is None:
        desc = ''
    desc = f'{desc:<{desc_align}}'

    if isinstance(args[0], int):
        iterable = range(*args)
    else:
        assert len(args) == 1
        iterable = args[0]

    if _mode == "tqdm":
        yield from tqdm(iterable, desc=desc)
    elif _mode == "fallback":
        if desc is None:
            desc = ""
        if hasattr(iterable, "__len__"):
            l = len(iterable)
            for i, x in enumerate(iterable):
                if i % max(l // 20, 1) == 0:
                    print(f"[{i}/{l} iters] {desc}")
                yield x
        else:
            last_print = 0
            for i, x in enumerate(iterable):
                if time.time() - last_print > 10:
                    print(f"[{i}/? iters] {desc}")
                    last_print = time.time()
                yield x
    elif _mode == "rich":
        yield from track(iterable, description=desc, console=_rich_console)


def status(name="Working..."):
    if _mode is None:
        config_progress_backend()

    if _mode == "rich":
        return rich.status.Status(
            name,
            console=_rich_console,
            spinner="dots",
            spinner_style="status.spinner",
            speed=1,
            refresh_per_second=12.5,
        )
    else:
        print(name)
        return contextmanager(lambda: iter([None]))()
