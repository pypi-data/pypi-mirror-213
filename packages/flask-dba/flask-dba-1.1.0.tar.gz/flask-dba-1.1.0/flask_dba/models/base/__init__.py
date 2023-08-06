"""Model base para todos os modelos."""
from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from ..utils import uuid_default


class ModelMetodosBase():
    """Model base para todos os modelos."""
    _instancia = {
        'app': None,
        'db': None,
        'dba': None,
    }

    def add(self):
        """Adiciona o obj ao banco de dados."""
        self._instancia['db'].session.add(self)
        return self.flush()

    def save(self):
        """Faz Commit no banco de dados."""
        self._instancia['db'].session.commit()
        return self

    def flush(self):
        """Atualiza as informações do banco de dados."""
        self._instancia['db'].session.flush()
        return self


class ModelBase(ModelMetodosBase):
    """Model base para todos os modelos."""
    uuid = Column(
        String(36),
        primary_key=True,
        default=uuid_default,
        unique=True,
        nullable=False
    )
    data_criado = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    data_atualizado = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    excludo = Column(
        Boolean,
        default=False,
        nullable=False
    )
    ativo = Column(
        Boolean,
        default=True,
        nullable=False
    )
