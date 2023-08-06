from . import TimeInvalidoException
from datetime import time


def validate_time(_time):
    if _time and not isinstance(_time, time):
        raise TimeInvalidoException(
            'O Tempo deve ser um objeto time.'
        )
