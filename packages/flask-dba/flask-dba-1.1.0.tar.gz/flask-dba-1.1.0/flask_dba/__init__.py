"""Main module."""
from .models.utils import relacao_usuario
from loguru import logger
import click


class FlaskDBA():
    """Main class."""
    from .models.base import ModelBase
    from .models.permission import (
        Permissao,
        Grupo,
        PermissaoGrupo,
        PermissaoUsuario,
        GrupoUsuario,
    )
    from .models.agendamento import (
        Agendamento,
        Coleta,
        Credencial,
        ExecucaoItem,
        Execucao,
    )
    from .models.endereco import (
        Endereco,
        Estado,
        UsuarioEndereco
    )
    from .models.usuario import Usuario

    from .models.empresa import (
        Empresa,
        EmpresaEndereco,
        Colaborador,
        PermissaoColaborador,
        GrupoColaborador,
    )

    def __init__(self, app=None, db=None):
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        """Initialize the FlaskDBA extension."""
        logger.debug("Inicializando a extensão FlaskDBA")
        self.app = app
        self.db = db

        self.ModelBase._instancia['app'] = app
        self.ModelBase._instancia['db'] = db
        self.ModelBase._instancia['dba'] = self

        @click.command()
        def init_rules():
            """Initialize permissions."""
            self.init_rules()
        app.cli.add_command(init_rules, name='init_rules')

    def init_permissions(self, usuario=False):
        """Initialize permissions."""
        logger.debug("Inicializando as permissões")
        with self.app.app_context():
            self.init_table('Permissao')
            self.init_table('Grupo')
            self.init_table('PermissaoGrupo')
            if usuario:
                logger.debug("Inicializando as permissões de usuário")
                ref_permissao = relacao_usuario('PermissaoUsuario')
                ref_grupo = relacao_usuario('GrupoUsuario')
                self.init_table('PermissaoUsuario', ref_permissao)
                self.init_table('GrupoUsuario', ref_grupo)

    def init_rules(self):
        """Gera as permissões de acordo com as rotas do app."""
        logger.debug("Inicializando as regras de permissão")
        self.Permissao.gerar_permissao(self.Permissao, self.app, self.db)
        self.Grupo.gerar_grupos(self.Grupo, self.Permissao, self.db)
        self.PermissaoGrupo.gerar_relacoes(self.PermissaoGrupo, self.db)

    def init_agendamento(self):
        """Initialize agendamento."""
        logger.debug("Inicializando o agendamento")
        with self.app.app_context():
            self.init_table("Agendamento")
            self.init_table("Coleta")
            self.init_table("Credencial")
            self.init_table("ExecucaoItem")
            self.init_table("Execucao")

    def init_endereco(self, usuario=False):
        """Initialize endereco."""
        logger.debug("Inicializando o endereço")
        with self.app.app_context():
            self.init_table("Endereco")
            self.init_table("Estado")
            if usuario:
                ref_usuario = relacao_usuario('UsuarioEndereco')
                self.init_table("UsuarioEndereco", ref_usuario)

    def init_usuario(self):
        """Initialize usuario."""
        logger.debug("Inicializando o usuário")
        with self.app.app_context():
            self.init_table("Usuario")

    def init_table(self, name, *extras):
        """Initialize table."""
        logger.debug(f"Inicializando a tabela {name}")
        new = type(
            name,
            (*extras, getattr(self, name), self.db.Model), {}
        )
        setattr(self, name, new)
        return new

    def init_empresa(
        self,
        with_endereco=False,
        with_colaborador=False,
        with_permissions=False
    ):
        logger.debug("Inicializando a empresa")
        with self.app.app_context():
            self.init_table("Empresa")
            if with_endereco:
                self.init_table("EmpresaEndereco")
            if with_colaborador:
                self.init_table("Colaborador")
                if with_permissions:
                    self.init_table("PermissaoColaborador")
                    self.init_table("GrupoColaborador")
