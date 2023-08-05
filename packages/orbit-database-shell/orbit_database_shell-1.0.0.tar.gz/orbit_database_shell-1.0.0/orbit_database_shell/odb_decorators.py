# -*- coding: utf-8 -*-
"""odb_decorators - general decorators for the actions module"""
from functools import wraps
from typing import Callable, Any

def selected(func: Callable) -> Callable:
    @wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if not args[0]._db:
            return args[0].warning(f'No database selected!')
        else:
            return func(*args, **kwargs)
    return wrapped


def has_table(func: Callable) -> Callable:
    @wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        table_name = args[1].get('table')
        if table_name not in list(args[0]._db.tables(args[0]._mode)):
            return args[0].warning(f'No valid table specified!')
        else:
            return func(*args, **kwargs)
    return wrapped


def has_index(func: Callable) -> Callable:
    @wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        table_name = args[1].get('table')
        index_name = args[1].get('index')
        table = args[0]._db[table_name]
        if index_name not in list(table.indexes()):
            return args[0].warning(f'No valid index specified!')
        else:
            return func(*args, **kwargs)
    return wrapped


banner = """<green><b>
  .oooooo.             .o8        o8o      .           oooooooooo.   oooooooooo.
 d8P'  `Y8b           "888        `"'    .o8           `888'   `Y8b  `888'   `Y8b
888      888 oooo d8b  888oooo.  oooo  .o888oo          888      888  888     888
888      888 `888""8P  d88' `88b `888    888            888      888  888oooo888'
888      888  888      888   888  888    888   8888888  888      888  888    `88b
`88b    d88'  888      888   888  888    888 .          888     d88'  888    .88P
 `Y8bood8P'  d888b     `Y8bod8P' o888o   "888"         o888bood8P'   o888bood8P'
</b></green>
<gray>     Orbit Database Command Line Tool (c) Mad Penguin Consulting Ltd 2023</gray>
<green>     To get started try <b>help register</b> or <b>help</b> for all available commands</green>"""
