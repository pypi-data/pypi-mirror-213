# -*- coding: utf-8 -*-
"""orbit-database-shell - command line tool for accessing and managing orbit-database databases"""
from pathlib import Path, PosixPath
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import CompleteStyle
from orbit_database_shell.odb_grammar import Completer, lexer, grammar, grammar_style
from orbit_database_shell.odb_actions import Actions
from orbit_database_shell.odb_decorators import banner

__author__ = 'Gareth Bult'
__banner__ = 'Orbit-DB'
__copyright__ = 'Copyright 2023, Mad Penguin Consulting Ltd'
__credits__ = ['Gareth Bult']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Gareth Bult'
__email__ = 'gareth@madpenguin.uk'
__status__ = 'Development'


def main ():
    actions = Actions().notice(banner)
    folder = Path('~/.orbit').expanduser()
    folder.mkdir(exist_ok=True, parents=True)
    session = PromptSession(
        history=FileHistory(PosixPath(folder / 'shell_history')),
        complete_style=CompleteStyle.READLINE_LIKE,
        auto_suggest=AutoSuggestFromHistory(),
        validate_while_typing=True,
        lexer=lexer,
        completer=Completer(actions),
        style=grammar_style
    )
    while True:
        try:
            user_input = grammar.match(session.prompt(actions.database_name))
            if not user_input:
                actions.warning('Command failed, syntax error')
                continue
            action = user_input.variables().get('command')
            if not action:
                continue
            actions.complete(action, user_input.variables())
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
    actions.info('[shell terminated]')


if __name__ == '__main__':
    main()
