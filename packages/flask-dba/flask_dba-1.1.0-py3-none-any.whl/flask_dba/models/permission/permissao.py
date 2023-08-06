"""Modelo de permissao de rota."""
import os
from loguru import logger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean
from ..base import ModelBase


class Permissao(ModelBase):
    """Permissao de rota."""
    __tablename__ = 'Permissao'
    endpoint = Column(String(255), nullable=False)
    method = Column(String(255), nullable=False)
    rule = Column(String(255), nullable=False)
    descricao = Column(String(255))
    publico = Column(Boolean, default=False, nullable=False)
    custom = Column(Boolean, default=False, nullable=False)
    app = Column(String(255), nullable=False)

    @staticmethod
    def gerar_permissao(cls, app: Flask, db: SQLAlchemy):
        logger.debug('Criando permissões')
        app_name = os.environ.get('FLASK_DBA_NAME', 'principal')
        cls.query.filter(
            cls.custom == 0,
            cls.app == app_name,
        ).update({'excludo': True})
        for rule in app.url_map.iter_rules():
            for method in rule.methods:
                permissao = cls.query.filter(
                    cls.endpoint == rule.endpoint,
                    cls.method == method,
                    cls.custom == 0
                ).first()
                if not permissao:
                    permissao = cls(
                        endpoint=rule.endpoint,
                        method=method,
                        rule=rule.rule,
                        custom=False,
                        app=app_name,
                    )
                    permissao.add()
                else:
                    permissao.update(excludo=False, rule=rule.rule)

        db.session.commit()
        logger.debug('Permissões criadas')

    def update(self, excludo, rule):
        """Atualiza as informações da permissão."""
        self.excludo = excludo
        self.rule = rule

    @staticmethod
    def permissoes_sem_grupo_correspondente(db) -> object:
        """
        SELECT DISTINCT endpoint
        FROM Permissao P
            LEFT JOIN Grupo G ON
                P.endpoint == G.nome
                AND G.custom == 0
        WHERE
            G.uuid IS NULL
            AND P.custom == 0
            AND P.excludo == 0
        """
        query = db.text("""
        SELECT DISTINCT endpoint
        FROM Permissao P
            LEFT JOIN Grupo G ON
                P.endpoint == G.nome
                AND G.custom == 0
        WHERE
            G.uuid IS NULL
            AND P.custom == 0
            AND P.excludo == 0
        """)
        return db.session.execute(query).fetchall()

    def add_to_user(
        self,
        usuario_uuid: str
    ):
        PUser = self._instancia['dba'].PermissaoUsuario
        p_user = PUser()
        p_user.insert_permissao(
            permissao_uuid=self.uuid,
            usuario_uuid=usuario_uuid,
        )
        p_user.add()

        return p_user
