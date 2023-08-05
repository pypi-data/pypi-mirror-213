import torch


class TensorDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            super().__setitem__(k, v.clone())

    def __repr__(self):
        return f"TensorDict({dict(self)})"

    @staticmethod
    def convert(new):
        if isinstance(next(iter(new.values())), torch.Tensor):
            return TensorDict(new)
        else:
            return new

    def __getitem__(self, item):
        if isinstance(item, str):
            return super().__getitem__(item)
        return TensorDict({k: x.__getitem__(item) for k, x in self.items()})

    def __getattr__(self, name):
        attrs = [getattr(v, name) for v in self.values()]

        if callable(getattr(torch.Tensor, name)):
            def func(*args, **kwargs):
                new = {k: f(*args, **kwargs) for k, f in zip(self.keys(), attrs)}
                return TensorDict.convert(new)
            return func
        else:
            return TensorDict.convert({k: f for k, f in zip(self.keys(), attrs)})

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        if (not all(issubclass(t, TensorDict) for t in types)
                or func not in [torch.cat, torch.stack]):
            return NotImplemented
        td = next(iter(next(iter(args))))
        ttypes = [torch.Tensor] * len(args)
        new = {k: torch.Tensor.__torch_function__(func, ttypes, [[x[k] for x in a] for a in args], kwargs)
               for k in td.keys()}
        return TensorDict.convert(new)
