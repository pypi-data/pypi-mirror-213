"""Modelo de agendamento para o scheduler."""
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from ..base import ModelBase
from flask_dba.exceptions import (
    DiaInvalidoException,
    HoraInvalidoException,
    MinutoInvalidoException
)
from flask_dba.exceptions.utils import validate_time
from datetime import time


class Agendamento(ModelBase):
    """Agendamento para o scheduler."""
    __tablename__ = 'Agendamento'

    dia = Column(Integer, nullable=False)
    hora = Column(Integer, nullable=False)
    minuto = Column(Integer, nullable=False)

    credencial_uuid = Column(
        String(36),
        ForeignKey("Credencial.uuid"),
        nullable=True
    )
    credencial = declared_attr(
        lambda cls: relationship(
            'Credencial', backref='Agendamento',
        ))

    def _validate_dia(self, dia):
        if dia > 31:
            raise DiaInvalidoException(
                'O dia não pode ser maior que 31.'
            )
        elif dia <= 0:
            raise DiaInvalidoException(
                'O dia não pode ser menor ou igual a 0.'
            )

    def _validate_hora(self, hora):
        if hora > 23:
            raise HoraInvalidoException(
                'A hora não pode ser maior que 23.'
            )
        elif hora < 0:
            raise HoraInvalidoException(
                'A hora não pode ser menor que 0.'
            )

    def _validate_minuto(self, minuto):
        if minuto > 59:
            raise MinutoInvalidoException(
                'O minuto não pode ser maior que 59.'
            )
        elif minuto < 0:
            raise MinutoInvalidoException(
                'O minuto não pode ser menor que 0.'
            )

    def insert_time(self, _time: time):
        validate_time(_time)
        self.dia = _time.day
        self.hora = _time.hour
        self.minuto = _time.minute

    def insert_numbers_time(self, dia: int, hora: int, minuto: int):
        self._validate_dia(dia)
        self._validate_hora(hora)
        self._validate_minuto(minuto)
        self.dia = dia
        self.hora = hora
        self.minuto = minuto

    def insert(
        self,
        dia: int = None,
        hora: int = None,
        minuto: int = None,
        _time: time = None
    ):

        if _time:
            self.insert_time(_time)
        else:
            self.insert_numbers_time(dia, hora, minuto)

        return self

    def insert_credencial(self, credencial_uuid: str):
        self.credencial_uuid = str(credencial_uuid)

        return self

    def add_execucao(self, **kw):
        Exe = self._instancia['dba'].Execucao
        exe = Exe().insert(**kw)
        exe.agendamento_uuid = self.uuid
        return exe.add()
