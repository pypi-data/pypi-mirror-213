# -*- coding: utf-8 -*-
"""odb_actions - implementation for CLI routines defined by Grammer"""
from pathlib import PosixPath, Path
from json import loads, dumps, JSONDecodeError
from prompt_toolkit import print_formatted_text as print, HTML, ANSI
from prompt_toolkit.styles import Style
from datetime import datetime
from termcolor import colored
from pygments import highlight, lexers, formatters
from orbit_database import Manager, Doc, SerialiserType, ReadTransaction, WriteTransaction
from orbit_database_shell.odb_help import Help
from orbit_database_shell.odb_decorators import selected, has_table, has_index
from rich.console import Console
from rich.table import Table
from tqdm import tqdm
from datetime import datetime
import collections
collections.Iterable = collections.abc.Iterable

try:
    import mysql.connector
except Exception:
    pass


class Actions():

    def __init__(self):
        self._manager = Manager()
        self._help = Help()
        self._home = PosixPath('~/.orbit').expanduser()
        self._databases = {}
        self._db = None
        self._db_name = None
        self._table = None
        self._limit = 10
        self._mode = False
        self._mysql = None
        Path.mkdir(self._home, exist_ok=True)

    def get_table(self, name):
        if name in list(self._db.tables(True)):
            return self._db.table(name)
        else:
            self.error(f'no such table "{name}"')
            return None

    def complete(self, action, variables):
        if hasattr(self, f'do_{action}'):
            getattr(self, f'do_{action}')(variables)
        else:
            self.error(f'Syntax Ok but {action} is not available')

    def warning(self, text):
        print(HTML(f'<orange>{text}</orange>'))
        return self

    def error(self, text):
        print(HTML(f'<red>{text}</red>'))
        return self

    def info(self, text):
        print(HTML(f'<green>{text}</green>'))
        return self

    def notice(self, text):
        print(HTML(f'<blue>{text}</blue>'))
        return self

    @property
    def database_name(self):
        name = self._db_name if self._db else 'none'
        return [('class:database', name), ('class:chevron', '> ')]

    @property
    def databases(self):
        return self.load_databases()

    @property
    def tables(self):
        return [name for name in self._db.tables(self._mode)] if self._db else []

    def indexes(self, variables):
        table_name = variables.get('table')
        return [name for name in self._db.table(table_name).indexes()] if self._db and table_name in self._db.tables(self._mode) else []

    def fields(self, variables):
        return self._fields(variables.get('table'), variables.getall('fields'))

    def all_fields(self, table_name):
        return self._fields(table_name, [])

    def _fields(self, table_name, base_fields):
        if table_name not in self._db.tables(self._mode):
            return []
        fields = []
        table = self.get_table(table_name)
        if table._codec != SerialiserType.RAW:
            for result in table.filter(page_size=10):
                for key in result.doc.keys():
                    if key not in fields and key not in base_fields:
                        fields.append(key)
        return fields
    
    def add_stats (self, tab, taken, count, limit=None):
        caption = f'Time: {taken.total_seconds():0.4f}s '
        caption += f'=> {int(1/(taken).total_seconds())*count}/sec '
        caption += '' if (not limit or count < limit) else f'(Limited view[{limit}])'
        tab.caption = caption

    def richTable (self, fields):
        tab = Table(min_width=50)
        for field in fields:
            tab.add_column(field, style='cyan', header_style='deep_sky_blue4', no_wrap=True)
        return tab

    def load_databases(self):
        regfile = self._home / 'databases'
        if regfile.exists():
            with open(regfile.as_posix(), 'r') as io:
                text = io.read()
                return loads(text) if len(text) else {}
        return {}

    def save_databases(self, databases):
        regfile = self._home / 'databases'
        with open(regfile.as_posix(), 'w') as io:
            return io.write(dumps(databases))

    @selected
    def do_import(self, vars):
        database_name = vars.get('mysql_db')
        table_name = vars.get('mysql_tb')
        if table_name in self._db.tables(self._mode):
            return self.warning(f'<b>{table_name}</b> already exists, drop it first!')
        
        if not self._mysql:   
            try:
                self._mysql = mysql.connector.connect(
                    host="127.0.0.1",
                    port=3306)
            except Exception as e:
                return self.error(f'Error connecting to local db: {str(e)}')

        cursor = self._mysql.cursor()
        cursor.execute(f"use {database_name}")
        if table_name == '*':
            cursor.execute("show tables")
            table_names = [row [0] for row in cursor.fetchall()]
        else:
            table_names = [table_name]      

        start = datetime.now()
        for name in table_names:
            cursor.execute(f"select * from {name}")
            rows = cursor.fetchall()
            table = self._db.table(name.replace('_', '-'))
            with WriteTransaction(self._db) as txn:
                for row in tqdm(rows, colour="green"):
                    doc = Doc()
                    for i in range(len(row)):
                        if row[i]:
                            t = cursor.description[i][1]
                            if t == 6:
                                value = None
                            elif t==7 or t == 12:
                                value = row[i].isoformat()
                            elif t < 10 or t == 13 or t == 246:
                                value = row[i]
                            else:
                                value = str(row[i])
                            doc[cursor.description[i][0]] = value
                    try:
                        table.append(doc, txn=txn)
                    except Exception as e:
                        self.error(str(e))
                        self.info(str(row))
                        self.info(cursor.description[i])
            self.info(f'Imported <b>{cursor.rowcount}</b> rows into <b>{name}</b>')
        self.info(f'Completed in {datetime.now() - start} seconds')
        cursor.close()

    def do_show(self, vars):
        cmd = vars.get('show_commands')
        if cmd == 'databases':
            self.show_databases()
        elif cmd == 'tables':
            self.show_tables()
        elif cmd == 'indexes':
            self.show_indexes(vars)
        else:
            print(f'Invalid: {cmd}')
        return
    
    @selected
    def do_load (self, vars):
        name = vars.get('table')
        path = vars.get('path')
        table = self._db.table(name)
        if table.records():
            return self.warning(f' <b>{name}</b> already has records!')
        if not Path(path).exists():
            return (f' <b>{path}</b> not found!')
        table.import_from_file(path)

    @selected
    def do_save (self, vars):
        name = vars.get('table')
        path = vars.get('path')
        table = self.get_table(name)
        table.export_to_file(path)
        self.info(f' Export of <b>{name}</b> => <b>{path}</b> is complete')

    def do_mode (self, vars):
        mode = vars.get('mode_commands')
        if mode == 'user':
            self._mode = False
            self.info('Switched to <b>USER</b> mode')
        if mode == 'advanced':
            self._mode = True
            self.info('Switched to <b>ADVANCED</b> mode')

    @selected
    @has_table
    def do_drop (self, vars):
        table_name = vars.get('table')
        index_name = vars.get('index')
        table = self.get_table(table_name)
        if index_name and table_name:
            if index_name in table:
                table.drop(index_name)
                self.info(f'Index <b>{index_name}</b> dropped!')
            else:
                self.error(f'no such index: {index_name}')
        elif table_name:
            self._db.drop(table_name)
            self.info(f'Table <b>{table_name}</b> dropped!')

    def do_register(self, vars):
        name = vars.get('name')
        path = vars.get('path')
        databases = self.load_databases()
        if name in databases:
            return self.warning(f'<b>{name}</b> already exists!')
        if not Path(path).exists():
            return (f'<b>{path}</b> does not exist!')
        if not (Path(path) / 'data.mdb').exists():
            return self.warning(f'<b>{path}</b> does not contain a database!')
        databases[name] = path
        self.save_databases(databases)
        self.info(f'Registered <b>{name}</b> => <b>{path}</b>')
        print()

    def do_create(self, vars):
        name = vars.get('name')
        path = vars.get('path')
        databases = self.load_databases()
        if name in databases:
            return self.warning(f'<b>{name}</b>  already exists!')
        if Path(path).exists():
            return self.warning(f'<b>{path}</b>  already exists!')
        if (Path(path) / 'data.mdb').exists():
            return self.warning(f'<b>{path}</b>  already contains a database!')
        Path(path).mkdir(parents=True)
        databases[name] = path
        self.save_databases(databases)
        self.info(f'Registered <b>{name}</b> => <b>{path}</b>')

    def do_use(self, vars):
        database = vars.get('database')
        if self._db_name == database:
            return self.warning(f'database "{database}" is already selected!')

        databases = self.load_databases()
        if database in databases:
            try:
                db = self._manager.database(database, databases[database], config={
                    'map_size': 1024*1024*1024*1024,
                    'writemap': False,
                    'max_dbs': 2048,
                })
                if self._db:
                    self._db.close()
                self._db = db
                self._db_name = database
            except Exception as e:
                self.error(f'Unable to open <b>{databases[database]}</b> => {str(e)}')
                raise
        else:
            self.error(f'Unknown database: <b>{database}</b>')

    def show_databases(self):
        """Display a list of currently registered databases"""
        databases = self.load_databases()
        if not len(databases):
            return self.error(f'No databases registered!')
        
        tab = self.richTable(['Database name', 'Mapped', 'Used', '(%)', 'Path'])
        for name, path in databases.items():
            mdb = Path(path) / 'data.mdb'
            try:
                stat = mdb.stat()
            except FileNotFoundError:
                self.error(f'Database is missing: {path}')
                continue
            mapped = stat.st_size
            divisor = 1024
            units = 'K'
            if mapped > 1024 * 1024 * 1024:
                divisor = 1024 * 1024 * 1024
                units = 'G'
            elif mapped > 1024 * 1024:
                divisor = 1024 * 1024
                units = 'M'

            tab.add_row(
                name,
                '{:7.2f}{}'.format(stat.st_size / divisor, units),
                '{:6.2f}{}'.format(stat.st_blocks * 512 / divisor, units),
                str(int((stat.st_blocks * 512 * 100) / stat.st_size)),
                path
            )
        Console().print(tab)

    @selected
    def show_tables(self):
        """Display a list of tables available within this database"""
        tab = self.richTable(['Table name', '#Recs', 'Codec', 'Depth', 'Oflow%', 'Index names'])
        for name in self._db.tables(self._mode):
            table = self.get_table(name)
            try:
                db = self._db.env.open_db(name.encode())
                with self._db.env.begin() as txn:
                    stat = txn.stat(db)
                leaf = int(stat['leaf_pages'])
                indexes = ', '.join(table.indexes())
                names, indexes = indexes[:60], indexes[60:]
                codec = str(table._codec.value)
            except Exception as e:
                self.error(str(e))
                stat = {}
                codec = '?'
                leaf = 0
                names = ''
                indexes = []

            tab.add_row(
                name,
                str(stat.get('entries',0)),
                codec,
                str(stat.get('depth',0)),
                str(int(stat.get('overflow_pages',0)) * 100 / (leaf if leaf else 1)),
                names)
        Console().print(tab)


    @selected
    @has_table
    def show_indexes(self, vars):
        """Display a list of indexes for the specified table\n"""
        table_name = vars.get('table')
        table = self.get_table(table_name)
        
        tab = self.richTable(['Table name', 'Index name', 'Entries', 'Dups', 'Key'])
        with ReadTransaction(self._db) as transaction:
            for index in table.indexes(txn=transaction.txn):
                d = self._db.meta.fetch_index(table_name, index, transaction.txn)
                conf = d['conf']
                if not d or 'conf' not in d:
                    self.error(f' Unable to locate metadata for {table_name}!')
                    continue
                if conf.get('iwx'):
                    key = 'Full Text Index'
                else:
                    key = conf.get('func', 'None')
                    if not key:
                        key = 'None'
                text, key = key[:60], key[60:]

                tab.add_row(
                    table_name if table_name else 'None',
                    index if index else 'None',
                    str(table[index].records() if index in table else '?'),
                    'True' if conf.get('dupsort') else 'False',
                    text)
                while len(key):
                    text, key = key[:60], key[60:]
                    tab.add_row('', '', '', '', text)
        Console().print(tab)

    @selected
    @has_table
    def do_explain(self, vars):
        table_name = vars.get('table')
        table = self.get_table(table_name)
        if table._codec == SerialiserType.RAW:
            return self.error(f' table is <b>RAW</b> - no schema available')
        keys = {}
        samples = {}
        for result in table.filter(page_size=10):
            for key in result.doc.keys():
                ktype = type(result.doc[key]).__name__
                if ktype in ['str', 'int', 'bool', 'bytes', 'float']:
                    sample = result.doc[key]
                    if sample:
                        if ktype == 'bytes':
                            sample = sample.decode()
                        if ktype in ['bytes', 'str']:
                            sample = sample.replace('\n', ' ')
                            if len(sample) > 60:
                                sample = sample[:60] + '...'
                        samples[key] = sample
                else:
                    sample = str(result.doc[key]).replace('\n', ' ')
                    if len(sample) > 60:
                        sample = sample[:60] + '...'
                    samples[key] = sample

                if key not in keys:
                    keys[key] = [ktype]
                else:
                    if ktype not in keys[key]:
                        keys[key].append(ktype)

        tab = self.richTable(['Field names', 'Field types', 'Sample'])
        for key in keys:
            tab.add_row(str(key), str(keys[key]), str(samples.get(key, '')))
        Console().print(tab)
    
    @selected
    @has_table
    def do_clear(self, vars):
        table_name = vars.get('table')
        table = self.get_table(table_name)
        records = table.records()
        table.empty()
        self.info(f'Cleared <brown><b>{records}</b></brown> records from <b><brown>{table_name}</brown></b>')

    @selected
    @has_table
    def do_select(self, vars):
        table_name = vars.get('table')
        fields = vars.getall('field')
        limit = int(vars.get('limit', 10))
        order = vars.get('index', None)
        if '*' in fields:
            fields.remove('*')
            fields += self.all_fields(table_name)
        starts = vars.get('doc', None)
        table = self.get_table(table_name)
        params = {'page_size': limit}
        if starts:
            try:
                lower = loads(starts)
            except JSONDecodeError as e:
                self.error(str(e))
                return
            params['lower'] = Doc(lower)
            upper = dict(lower)
            for item in upper:
                if isinstance(upper[item], str):
                    upper[item] += chr(254)
                elif isinstance(upper[item], (int, float)):
                    upper[item] += 1
            params['upper'] = Doc(upper)
        where = vars.get('where')
        if where:
            if where.startswith('"'):
                where = where.strip('"')
            else:
                where = where.strip("'")
            try:
                params['expression'] = eval(where)
            except Exception as e:
                return self.error(f'Invalid expression: <b>{where}</b> :: {str(e)}, valid lambda expected')

        def docval(doc, k):
            if k == '_id':
                return doc.key
            if ':' in k:
                k, att = k.split(":")
            if '.' not in k:
                return doc[k] if k in doc else 'null'
            parts = k.split('.')
            while len(parts):
                k = parts.pop(0)
                doc = doc[k] if k in doc else {}
            return doc

        if table._codec == SerialiserType.RAW:
            tab = self.richTable(['id', 'len'])
        else:
            tab = self.richTable(fields)
        try:
            beg = datetime.now()
            count = 0
            for result in table.filter(order, **params):
                count += 1
            taken = datetime.now() - beg
            for result in table.filter(order, **params):
                if table._codec == SerialiserType.RAW:
                    tab.add_row(str(result._oid), str(len(result.raw)))
                else:
                    tab.add_row(*[str(docval(result.doc, f)) for f in fields])           
            self.add_stats(tab, taken, count, limit)
            Console().print(tab)
        except KeyError as e:
            self.error(f'unable to process key: {str(e)}')
 
    @selected
    @has_table
    def do_unique(self, vars):
        table_name = vars.get('table')
        field_name = vars.get('field')
        order = vars.get('index', None)
        table = self.get_table(table_name)

        tab = self.richTable(['Field name', 'Count'])
        beg = datetime.now()
        count = 0
        if order:
            params = {'suppress_duplicates': True}
            if order not in table.indexes():
                return self.error(f' index <b>{order}</b> does not exist!')
            params['index_name'] = order
            for result in table.filter(**params):
                count += 1
                tab.add_row(str(result.key.decode()), str(result.count))
        else:
            values = {}
            for result in table.filter():
                count += 1
                value = result.doc[field_name]
                if not value:
                    continue
                if not isinstance(value, (str, int, float, bool)):
                    if isinstance(value, list):
                        for item in value:
                            if item in values:
                                values[item] += 1
                            else:
                                values[item] = 1
                else:
                    if value in values:
                        values[value] += 1
                    else:
                        values[value] = 1

            keys = [key for key in values.keys()]
            keys.sort()
            for key in keys:
                tab.add_row(str(key), str(values[key]))
        self.add_stats(tab, datetime.now()-beg, count)
        Console().print(tab)

    @selected
    @has_table
    def do_analyse(self, vars):
        """Analyse a table to see how record sizes are broken down"""
        table_name = vars.get('table')
        count = 0
        rtot = 0
        rmax = 0
        vals = []
        beg = datetime.now()
        table = self.get_table(table_name)
        with ReadTransaction(self._db) as transaction:
            for result in table.filter(txn=transaction.txn):
                rlen = len(result.raw)
                rtot += rlen
                vals.append(rlen)
                if rlen > rmax:
                    rmax = rlen
                count += 1
        end = datetime.now()

        max = 20
        div = rmax / max
        arr = [0 for i in range(max + 1)]
        for item in vals:
            idx = int(item / div)
            arr[idx] += 1

        test = []
        n = div
        maxitem = 0
        for item in arr:
            label = int(n)
            if n > 1024:
                label = str(int(n / 1024)) + 'K' if n > 1024 else str(label)
            else:
                label = str(label)

            test.append((label, item))
            if item > maxitem:
                maxitem = item
            n += div

        tab = self.richTable(['Field size', 'Count', 'Bar'])
        for item in test:
            tab.add_row(str(item[0]), str(item[1]), int(80*item[1]/maxitem)*'#')
        self.add_stats(tab, end-beg, count)
        Console().print(tab)

    @selected
    @has_table
    def dump(self, vars):
        table_name = vars.get('table')
        id = vars.get('id')
        if table_name not in list(self._db.tables(self._mode)):
            return self.error(f'table <b>{table_name}</b> does not exist!')
        table = self.get_table(table_name)
        doc = table.get(id)
        if not doc:
            return self.error(f' id <b>{id}</b> not found!')
        if table._codec == SerialiserType.RAW:
            print(doc.doc.decode())
        else:
            if doc:
                formatted = dumps(doc.doc, indent=4)
                colorful_json = highlight(formatted, lexers.JsonLexer(), formatters.TerminalFormatter())
                print(ANSI(colorful_json))

    @selected
    def fix (self, vars):
        name = vars.get('name')
        try:
            db = self._db.env.open_db()
            with self._db.env.begin(write=True) as txn:
                if not txn.delete(name.encode()):
                    self.warning(f'Unable to find key: {name}')
                else:
                    self.info(f'Deleted: {name}')
        except Exception as e:
            self.error(str(e))

    @selected
    @has_table
    def do_delete(self, vars):
        table_name = vars.get('table')
        key_name = vars.get('name')
        self.error(f'delete "{key_name}" from "{table_name}"')
        table = self.get_table(table_name)
        table.delete(key_name)
        return

    @selected
    @has_table
    @has_index
    def do_lexicon(self, vars):
        table_name = vars.get('table')
        order = vars.get('index', None)
        table = self.get_table(table_name)
        terms = vars.get('terms').strip('"').strip("'").strip()
        limit = int(vars.get('limit', 10))
        
        tab = self.richTable(['Term', 'Count'])
        count = 0
        beg = datetime.now()
        for result in table.lexicon(order, [terms], max=limit if limit else self._limit):
            count += 1
            tab.add_row(str(result[0]), str(result[1]))
        end = datetime.now()
        self.add_stats(tab, end-beg, count, limit)
        Console().print(tab)

    @selected
    @has_table
    @has_index
    def do_match(self, vars):
        table_name = vars.get('table')
        order = vars.get('index', None)
        table = self.get_table(table_name)
        terms = vars.get('terms').strip('"').strip("'").strip().split(',')
        limit = int(vars.get('limit', 10))

        beg = datetime.now()
        count, results = table.match(order, terms)
        end = datetime.now()

        tab = self.richTable(['_id'])
        for result in results[:limit]:
            tab.add_row(str(result))
        self.add_stats(tab, end-beg, count, limit)
        Console().print(tab)

    # def exit(self, vars):
    #     raise EOFError

    # def quit(self, vars):
    #     raise EOFError

    def do_help(self, vars):
        topic = vars.get('help_commands')
        self.notice(self._help.topic(topic))
