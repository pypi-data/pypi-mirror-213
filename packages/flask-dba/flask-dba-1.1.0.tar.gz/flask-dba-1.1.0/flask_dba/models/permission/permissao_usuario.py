"""Módulo de permissão de usuário."""
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..base import ModelBase


class PermissaoUsuario(ModelBase):
    """Permissão de usuário."""
    __tablename__ = 'PermissaoUsuario'
    usuario_uuid = Column(String(36), nullable=False)

    permissao_uuid = Column(String(36), ForeignKey(
        "Permissao.uuid"), nullable=False)
    permissao = declared_attr(lambda cls: relationship(
        'Permissao', backref='PermissaoUsuario',
    ))

    def insert_permissao(self, permissao_uuid, usuario_uuid, **_):
        """Insere permissão."""
        self.permissao_uuid = permissao_uuid
        self.usuario_uuid = usuario_uuid
        return self
