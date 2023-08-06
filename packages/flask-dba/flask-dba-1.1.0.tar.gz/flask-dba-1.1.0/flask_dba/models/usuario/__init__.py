from sqlalchemy import Column, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from ..base import ModelBase


class Usuario(ModelBase):
    """Usuário do sistema."""
    __tablename__ = 'Usuario'

    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    admin = Column(Boolean, default=False, nullable=False)

    def insert_credencial(self, username, password, **_):
        """Insere credencial."""
        self.username = username
        self.insert_password(password)
        return self

    def insert_password(self, password, **_):
        """Insere senha."""
        self.password = generate_password_hash(password)

    def check_password(self, password, **_):
        """Verifica senha."""""
        return check_password_hash(self.password, password)

    def insert_contato(self, email, **_):
        """Insere email."""
        self.email = email
        return self
