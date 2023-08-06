"""Modelo de execução de agendamento."""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from ..base import ModelBase
from loguru import logger


class Execucao(ModelBase):
    """Execução de agendamento."""
    __tablename__ = 'Execucao'

    agendamento_uuid = Column(
        String(36),
        ForeignKey("Agendamento.uuid"),
        nullable=False
    )
    agendamento = declared_attr(
        lambda cls: relationship(
            'Agendamento', backref='Execucao',
        ))

    def insert(self, **kwargs):
        logger.debug(f'Execucao.insert({kwargs})')
        return self

    def add_item(self, **kwargs):
        ExeItem = self._instancia['dba'].ExecucaoItem
        item = ExeItem()
        item.insert(**kwargs)
        item.execucao_uuid = self.uuid
        return item.add()
