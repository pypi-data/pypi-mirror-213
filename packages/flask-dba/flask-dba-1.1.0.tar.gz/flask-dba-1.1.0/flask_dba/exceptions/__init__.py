class AgendamentoException(Exception):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class DiaInvalidoException(AgendamentoException):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class MinutoInvalidoException(AgendamentoException):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class HoraInvalidoException(AgendamentoException):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class TimeInvalidoException(AgendamentoException):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
