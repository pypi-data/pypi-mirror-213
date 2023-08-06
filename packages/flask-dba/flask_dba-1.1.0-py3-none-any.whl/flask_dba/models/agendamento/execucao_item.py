"""Modelo de item de execução de agendamento."""""
from sqlalchemy import Column, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from ..base import ModelBase

from flask_dba.exceptions.utils import validate_time


class ExecucaoItem(ModelBase):
    """Item de execução de agendamento."""
    __tablename__ = 'ExecucaoItem'

    execucao_uuid = Column(
        String(36),
        ForeignKey('Execucao.uuid'),
        nullable=False
    )
    execucao = declared_attr(
        lambda cls: relationship(
            'Execucao', backref='ExecucaoItem',
        ))

    tempo_de_coleta = Column(Time, nullable=False)

    def insert(self, tempo_de_coleta, **_):
        validate_time(tempo_de_coleta)
        self.tempo_de_coleta = tempo_de_coleta
        return self

    def add_coleta(self, **kwargs):
        Coleta = self._instancia['dba'].Coleta
        coleta = Coleta()
        coleta.insert(**kwargs)
        coleta.execucao_item_uuid = self.uuid
        return coleta.add()
