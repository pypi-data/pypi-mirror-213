# -*- coding: utf-8 -*-
"""odb_completers - auto completion routines for Grammar parser"""
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.completion import Completion, Completer as PTCompleter
from prompt_toolkit.document import Document
from pathlib import PosixPath
from loguru import logger as log
try:
    import mysql.connector
except Exception:
    pass


class Completer(PTCompleter):

    def __init__(self, *args, **kwargs):
        if 'actions' in kwargs:
            self._actions = kwargs.pop('actions')
        self._mysql = None
        self._database = None
        super().__init__(*args, **kwargs)


class DatabaseCompleter(Completer):
    def get_completions(self, document, complete_event):
        for name in self._actions.databases:
            if name.startswith(document.text):
                yield Completion(name, -len(document.text))


class TableCompleter(Completer):
    def get_completions(self, document, complete_event):
        for name in self._actions.tables:
            if name.startswith(document.text):
                yield Completion(name, -len(document.text))


class IndexCompleter(Completer):
    def get_completions(self, document, complete_event):
        for name in self._actions.indexes(document.variables):
            if name.startswith(document.text):
                yield Completion(name, -len(document.text))


class FieldCompleter(Completer):
    def get_completions(self, document, complete_event):
        for name in self._actions.fields(document.variables):
            if name.startswith(document.text):
                yield Completion(name, -len(document.text))


class PathCompleter(Completer):
    def get_completions(self, document, complete_event):
        if document.text.startswith('/'):
            path = PosixPath(document.text)
        else:
            path = PosixPath('~').expanduser() / document.text
        if path.is_dir():
            root = path
            name = None
        else:
            root = path.parent
            name = path.name
        if root.exists():
            for item in root.iterdir():
                word = str(item).split('/')[-1]
                if not name or word.startswith(name):
                    yield Completion(str(item), -len(document.text))
        else:
            yield Completion(document.text)


class MyGrammarCompleter(GrammarCompleter):

    def get_completions(self, document, complete_event):
        user = self.compiled_grammar.match_prefix(document.text_before_cursor)
        if not user:
            return
        Document.variables = user.variables()
        completions = self._remove_duplicates(
            self._get_completions_for_match(user, complete_event)
        )
        for completion in completions:
            yield completion


class MySQLDBCompleter(Completer):

    def get_completions (self, document, complete_event):
        if not self._mysql:   
            try:
                self._mysql = mysql.connector.connect(
                    host="127.0.0.1",
                    port=3306)
            except Exception as e:
                log.error(str(e))
                return

        cursor = self._mysql.cursor()
        cursor.execute("show databases")
        for row in cursor.fetchall():
            name = row[0]
            if name.startswith(document.text):
                yield Completion(name, -len(document.text))
        cursor.close()


class MySQLTableCompleter(Completer):

    def get_completions (self, document, complete_event):
        if not self._mysql:   
            try:
                self._mysql = mysql.connector.connect(
                    host="127.0.0.1",
                    port=3306)
            except Exception as e:
                log.error(str(e))
                return

        cursor = self._mysql.cursor()
        cursor.execute(f"use {document.variables['mysql_db']}")
        cursor.execute("show tables")
        for row in cursor.fetchall():
            name = row[0]
            if name.startswith(document.text):
                yield Completion(name, -len(document.text))
        cursor.close()
