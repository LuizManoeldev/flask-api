"""
Autor: Luiz Dantas
Data: 11/02/2025
===================================================================================================================
    Este arquivo define um conjunto de comandos CLI para gerenciamento do banco de dados e execução de testes na aplicação.

    1. cov(pattern="tests_*.py") - Executa os testes unitários da aplicação com cobertura de código e exibe um resumo.
    2. cov_html(pattern="tests_*.py") - Executa os testes unitários com cobertura de código e gera um relatório HTML.
    3. tests(pattern="tests_*.py") - Executa os testes unitários sem gerar um relatório de cobertura.
    4. create_db() - Cria todas as tabelas do banco de dados.
    5. reset_db() - Reseta o banco de dados, excluindo e recriando todas as tabelas.
    6. drop_db() - Remove todas as tabelas do banco de dados.
    7. populate_db(username="root") -Popula o banco de dados com um usuário root e permissões básicas.
    8. init_app(app) - Registra os comandos CLI na aplicação Flask, incluindo operações de banco de dados e testes. Em ambiente de produção, apenas os comandos relacionados ao banco de dados são registrados.
"""

import unittest

import click
import coverage

from app.db import db


@click.option(
    "--pattern", default="tests_*.py", help="Test search pattern", required=False
)
def cov(pattern):
    """
    Run the unit tests with coverage
    """
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()
    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print("Coverage Summary:")
        cov.report()
        cov.erase()
        return 0
    return 1


@click.option(
    "--pattern", default="tests_*.py", help="Test search pattern", required=False
)
def cov_html(pattern):
    """
    Run the unit tests with coverage and generate an HTML report.
    """
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()

    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        cov.stop()
        cov.save()

        print("Coverage Summary:")
        cov.report()
        cov.html_report(directory="report/htmlcov")
        cov.erase()
        return 0

    return 1


@click.option("--pattern", default="tests_*.py", help="Test pattern", required=False)
def tests(pattern):
    """
    Run the tests without code coverage
    """
    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def create_db():
    """
    Create Database.
    """
    db.create_all()
    db.session.commit()


def reset_db():
    """
    Reset Database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


def drop_db():
    """
    Drop Database.
    """
    db.drop_all()
    db.session.commit()



def populate_db(username="root"):
    """
    Popular banco com Usuario Root e Permissoes basicas
    """
    #root = UserModel.query.filter_by(username=username).first()
    root = "User"
    if root is None:
        print("root-user is not created before!")
        #init_db()
    else:
        print("root-user is created!")


def init_app(app):
    """
        Create App in Prod and Dev Enviroments

        In Prodcution, only db commands are registered.
        In Dev, all commands are registered.
    
    """
    if app.config["APP_ENV"] == "production":
        commands = [create_db, reset_db, drop_db, populate_db]
    else:
        commands = [
            create_db,
            reset_db,
            drop_db,
            populate_db,
            tests,
            cov_html,
            cov,
        ]

    for command in commands:
        app.cli.add_command(app.cli.command()(command))
