# -*- coding: utf-8 -*-
"""odb_grammar - grammar specification for the orbit database CLI"""
from prompt_toolkit.contrib.regular_languages.compiler import compile
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from orbit_database_shell.odb_completers import DatabaseCompleter, PathCompleter, TableCompleter, FieldCompleter, IndexCompleter, MyGrammarCompleter
from orbit_database_shell.odb_completers import MySQLDBCompleter, MySQLTableCompleter

commands = ['show', 'select', 'use', 'register', 'explain', 'clear', 'unique', 'analyse', 'dump', 'lexicon', 'match', 'help', 'delete', 'import', 'drop', 'fix', 'mode', 'create']
show_commands = ['databases', 'tables', 'indexes']
drop_commands = ['table', 'index']
mode_commands = ['user', 'advanced']
select_options = ['limit', 'index', 'where']
index_options = ['doc']
unique_options = ['index']

grammar_style = Style.from_dict({
    'database': '#00adad',
    'chevron': '#d68b00 bold',
    'command': 'green bold',
    'modes': 'red bold',
    'databases': 'blue',
    'name': 'orange',
    'path': 'green',
    'table': '#a8a800',
    'field': 'red',
    'terms': 'red',
    'limit': 'cyan',
    'index': 'cyan',
    'starts': 'orange',
    'id': 'red',
    'help': 'green bold'
})

grammar = compile(
        r"""
        (\s* (?P<command>help) \s*)|
        (\s* (?P<command>help) \s+ (?P<help_commands>\w+)? \s*) |
        (\s* (?P<command>exit) \s*) |
        (\s* (?P<command>quit) \s*) |
        (\s* (?P<command>fix) \s+ bad \s+ root \s+ (?P<name>[_|a-z|0-9|-|@]+) \s*) |
        (\s* (?P<command>show) \s+ (?P<show_commands>databases) \s*) |
        (\s* (?P<command>show) \s+ (?P<show_commands>tables) \s*) |
        (\s* (?P<command>mode) \s+ (?P<mode_commands>user|advanced) \s*) |
        (\s* (?P<command>analyse) \s+ (?P<table>[a-z|0-9|-]+) \s*) |
        (\s* (?P<command>dump) \s+ (?P<table>[a-z|0-9|-]+) \s+ (?P<id>[a-z|0-9|-]+) \s*) |
        (\s* (?P<command>show) \s+ (?P<show_commands>indexes) \s+ (?P<table>[a-z|0-9|-]+) \s*) |
        (\s*
            (?P<command>unique) \s+
            (?P<table>[a-z|0-9|-]+) \s+
            (?P<field>\w+) \s*
            (?P<unique_options>index=(?P<index>\w+))?
        \s*) |
        (\s* (?P<command>register) \s+ (?P<name>[a-z|0-9]+) \s+ (?P<path>[A-Z|a-z|0-9|_/.-]+) \s*) |
        (\s* (?P<command>create) \s+ (?P<name>[a-z|0-9]+) \s+ (?P<path>[A-Z|a-z|0-9|_/.-]+) \s*) |
        (\s* (?P<command>use) \s+ (?P<database>[a-z|0-9]+) \s*) |
        (\s* (?P<command>explain) \s+ (?P<table>[a-z|0-9|-]+) \s*) |
        (\s* (?P<command>clear) \s+ (?P<table>[a-z|0-9|-]+) \s*) |
        (\s* (?P<command>delete) \s+ (?P<table>[_|a-z|0-9|-]+) \s+ (?P<name>[_|a-z|0-9|-|@]+) \s*) |
        (\s* (?P<command>load) \s+ (?P<table>[a-z|0-9|-]+) \s+ (?P<path>[A-Z|a-z|0-9|_/.-]+) \s*) |
        (\s* (?P<command>save) \s+ (?P<table>[a-z|0-9|-]+) \s+ (?P<path>[A-Z|a-z|0-9|_/.-]+) \s*) |
        (\s* (?P<command>import) \s+  (?P<mysql_db>[A-Z|a-z|0-9|_]+) \s+ (?P<mysql_tb>[A-Z|a-z|0-9|_|*]+) \s*) |
        (\s* (?P<command>drop) \s+ (?P<table>[a-z|0-9|-]+) \s*) |
        (\s* (?P<command>drop) \s+ (?P<table>[a-z|0-9|-]+) \s+ (?P<index>[a-z|0-9|-|_]+) \s*) |
        (\s*
            (?P<command>select) \s+
            (?P<table>[_|a-z|0-9|-]+) \s+
            (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*])
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s* , \s* (?P<field>[A-Z|a-z|0-9|_-]+(?P<attributes>:[<|>]?([0-9]+)?(?P<custom>@\w+)?)?|[*]))?
            (\s+ (?P<select_options>limit=(?P<limit>[0-9]+)) \s*)?
            (\s+ (?P<select_options>index=(?P<index>[a-z|0-9|_-]+) (\s+ (?P<index_options>doc=(?P<doc>\{[^\}]*\})))?) \s*)?
            (\s+ where\s+(?P<where>'[^']*'|"[^"]*") \s*)?
        \s*) |
        (\s*
            (?P<command>lexicon) \s+
            (?P<table>\w+) \s+
            (?P<index>\w+) \s+
            (?P<terms>'[^']*'|"[^"]*"|\w+)
            (\s+ (?P<select_options>limit=(?P<limit>[0-9]+)))?
        \s*) |
        (\s*
            (?P<command>match) \s+
            (?P<table>\w+) \s+
            (?P<index>\w+) \s+
            (?P<terms>\s+ '[^']*'|"[^"]*"|\w+)
            (?P<select_options>\s+ limit=(?P<limit>[0-9]+))?
        \s*) |
        """)

lexer = GrammarLexer(
    grammar, lexers={
        'command': SimpleLexer('class:command'),
        'show_commands': SimpleLexer('class:databases'),
        'mode_commands': SimpleLexer('class:modes'),
        'database': SimpleLexer('class:database'),
        'name': SimpleLexer('class:name'),
        'path': SimpleLexer('class:path'),
        'table': SimpleLexer('class:table'),
        'field': SimpleLexer('class:field'),
        'select_options': SimpleLexer('class:option'),
        'limit': SimpleLexer('class:limit'),
        'index': SimpleLexer('class:index'),
        'starts': SimpleLexer('class:starts'),
        'id': SimpleLexer('class:id'),
        'terms': SimpleLexer('class:terms'),
        'exit': SimpleLexer('class:exit'),
        'quit': SimpleLexer('class:quit'),
        'help': SimpleLexer('class:help'),
    })

def Completer (actions):
    return MyGrammarCompleter(
        grammar, {
            'mysql_db': MySQLDBCompleter(actions=actions),
            'mysql_tb': MySQLTableCompleter(actions=actions),
            'command': WordCompleter(commands),
            'show_commands': WordCompleter(show_commands),
            'mode_commands': WordCompleter(mode_commands),
            'database': DatabaseCompleter(actions=actions),
            'path': PathCompleter(actions=actions),
            'table': TableCompleter(actions=actions),
            'field': FieldCompleter(actions=actions),
            'select_options': WordCompleter(select_options),
            'index': IndexCompleter(actions=actions),
            'index_options': WordCompleter(index_options),
            'unique_options': WordCompleter(unique_options),
            'help_commands': WordCompleter(commands)
        }
    )
