from progressbar import ProgressBar


class OptionalProgressBar(ProgressBar):
    def __init__(self, *, verbose=True, **kwargs):
        self.verbose = verbose
        super().__init__(**kwargs)

    def start(self, max_value=None, init=True):
        if self.verbose:
            return super().start(max_value, init)
        return self

    def update(self, value=None, force=False, **kwargs):
        if self.verbose:
            return super().update(value, force, **kwargs)
        return self

    def finish(self, end='\n'):
        if self.verbose:
            return super().finish(end)
        return self
