# -*- coding: utf-8 -*-
"""odb_help - help documentation for the CLI prompt"""
class Help:

    def topic(self, topic):
        if not topic or not len(topic):
            topic = 'help'
        method = f'do_{topic}'
        if not hasattr(self, method):
            return f'<orange>Sorry, no help available for <red><b>{topic}</b></red></orange>'
        return getattr(self, method)()

    def do_help(self):
        return """
        <b>help</b> - provide some insight into the available commands and what they do

        <green><b>help]</b>          - this topic</green>
        <green><b>help [command]</b> - provide help on the selected command</green>

        <green><b>commands</b> - <b>show select use register explain clear unique analyse dump
                   lexicon match delete import drop fix mode create</b></green>

        <b>Examples:</b><green>
        "he" followed by tab will complete to "help", hit space, then tab, and all available
        topics will be displayed on the next line down. Type "se" then tab, then return, and you
        will see the help screen for "select".</green>

        <b>Notes:</b><green>
        - most components provide 'readline' style <b>tab</b> completion, so when you are faced
          with an explicit choice, hitting <b>tab</b> should list the available choices on the next
          line down. Once you have typed the unique portion of one of those choices, hitting <b>tab</b>
          will auto complete the word.
        - historic auto-complete is also provided, previous commands will pop-up in gray, use the right arrow
          key to select a previous command in it's entirety.
        - all commands should have some help information, more complex commands should include examples</green>
        """

    def do_show(self):
        return """
        <b>show</b> - show details about different database resources

        <green><b>show databases</b>       - show the databases currently registered</green>
        <green><b>show tables</b>          - show the tables that exist within the selected database</green>
        <green><b>show indexes <blue>[table]</blue></b> - show indexes for the specified table</green>

        <b>Examples:</b><green>
        none> show databases</green><brown>
        ┌───────────────┬──────────┬─────────┬─────┬─────────────────────────────────────────────┐
        │ Database name │   Mapped │    Used │ (%) │ Path                                        │
        ├───────────────┼──────────┼─────────┼─────┼─────────────────────────────────────────────┤
        │ starwars      │   32.00G │   0.00G │   0 │ /home/gareth/scm/graphql-examples/star-wars │
        │ orbit         │   32.00G │  16.25G │  50 │ /home/sandbox/scm/Orb/server/.database      │
        │ sw            │   24.00K │  24.00K │ 100 │ /home/gareth/scm/graphql-examples/sw        │
        └───────────────┴──────────┴─────────┴─────┴─────────────────────────────────────────────┘</brown><green>

        orbit> show tables</green><brown>
        ┌───────────────┬────────┬───────┬───────┬────────┬──────────────────────────────────────────────────────────────┐
        │ Table name    │ # Recs │ Codec │ Depth │ Oflow% │ Index names                                                  │
        ├───────────────┼────────┼───────┼───────┼────────┼──────────────────────────────────────────────────────────────┤
        │ accounts      │      4 │ ujson │     1 │      0 │ by_name                                                      │
        │ addressbook   │    555 │ ujson │     2 │      0 │ by_email, by_name                                            │
        │ assets        │      5 │ ujson │     1 │      0 │                                                              │
        │ cache         │  75890 │ ujson │     3 │      0 │ by_cid, by_envelope_ref, by_filename                         │
        │ cacheblob     │  75890 │ raw   │     4 │   4348 │                                                              │
        │ contacts      │  34541 │ ujson │     3 │      1 │ by_addr, by_name                                             │
        │ conversations │  37269 │ ujson │     3 │      1 │ by_date, by_message_id, by_participant                       │
        │ envelopes     │ 189456 │ ujson │     4 │      0 │ by_conversation, by_date, by_from, by_fromdate, by_in_reply_ │
        │               │        │       │       │        │ to, by_message_body_id, by_message_date, by_message_id, by_r │
        │               │        │       │       │        │ eply_reminder, by_tags, by_tagsdate                          │
        │ folders       │    119 │ ujson │     2 │      0 │ by_account, by_account_name                                  │
        │ mailq         │      6 │ ujson │     1 │      0 │                                                              │
        │ messages      │ 218802 │ raw   │     4 │   4462 │ by_raw                                                       │
        │ notifications │      0 │ ujson │     0 │      0 │                                                              │
        │ progress      │    120 │ ujson │     2 │      0 │                                                              │
        │ receipts      │   1643 │ ujson │     2 │      0 │ by_message_id                                                │
        │ rules         │     17 │ ujson │     2 │     66 │ by_order                                                     │
        │ search        │      9 │ ujson │     1 │      0 │                                                              │
        │ services      │     20 │ ujson │     1 │      0 │ by_asset, by_type                                            │
        │ signatures    │      3 │ ujson │     1 │      0 │                                                              │
        │ tags          │     35 │ ujson │     1 │      0 │ by_path, by_tag                                              │
        │ users         │      4 │ ujson │     1 │      0 │                                                              │
        └───────────────┴────────┴───────┴───────┴────────┴──────────────────────────────────────────────────────────────┘</brown><green>

        orbit> show indexes envelopes</green><brown>
        ┌────────────┬────────────────────┬─────────┬───────┬──────────────────────────────────────────────────────────────┐
        │ Table name │ Index name         │ Entries │ Dups  │ Key                                                          │
        ├────────────┼────────────────────┼─────────┼───────┼──────────────────────────────────────────────────────────────┤
        │ envelopes  │ by_conversation    │   75448 │ True  │ {conversation}                                               │
        │ envelopes  │ by_date            │  189456 │ True  │ {date:14.0f}                                                 │
        │ envelopes  │ by_from            │  189409 │ True  │ def func(doc): return [(f.get("mailbox","") + "@" + f.get("h │
        │            │                    │         │       │ ost", "")).encode() for f in doc.get("from_", [])]           │
        │ envelopes  │ by_fromdate        │  189409 │ True  │ def func(doc): return [(f.get("mailbox","") + "@" + f.get("h │
        │            │                    │         │       │ ost","") + "|" + "%14.f" % doc["date"]).encode() for f in do │
        │            │                    │         │       │ c.get("from_", [])]                                          │
        │ envelopes  │ by_in_reply_to     │   75447 │ True  │ {in_reply_to}                                                │
        │ envelopes  │ by_message_body_id │  189455 │ False │ {message_body_id}                                            │
        │ envelopes  │ by_message_date    │  189456 │ True  │ {message_id}|{date}                                          │
        │ envelopes  │ by_message_id      │  189456 │ True  │ {message_id}                                                 │
        │ envelopes  │ by_reply_reminder  │       2 │ True  │ {reply_reminder:14.0f}                                       │
        │ envelopes  │ by_tags            │  296296 │ True  │ def func(doc): return [t.encode() for t in doc["tags"] if t] │
        │ envelopes  │ by_tagsdate        │  296296 │ True  │ def func(doc): return [(t + "|" + "%14.f" % doc["date"]).enc │
        │            │                    │         │       │ ode() for t in doc["tags"] if t]                             │
        └────────────┴────────────────────┴─────────┴───────┴──────────────────────────────────────────────────────────────┘</brown>

        <b>Notes:</b><green>
        - see <b>use</b> to select a particular database
        - indexes are either based on python format strings, or embedded Python functions, so you can literally index on
          any expression you can derive from the record using Python
        - index expressions that resolve to lists are treated as multiple entries in the index, hence tags for a record with
          a tags field of ['TAG1', 'TAG2', 'TAG3'] will have three entries in the 'by_tags' index.</green>
        """

    def do_select(self):
        return """
        <b>select</b> - select data from a table and display in tabular format

        <green><b>select <blue>[table] *</blue></b>      - display all fields for the first few rows from [table]</green>
        <green><b>select <blue>[table] f1, f2</blue></b> - display fields "f1" and "f2" first few rows from [table]</green>

        <b>Modifiers:</b><green>
        - limit=[n]     - specify the number of rows from which to show information
        - index=[index] - use a specific index rather than the natural table order
        - where [expr]  - specify a lambda expression to filter each record</green>

        <b>Extended modifiers:</b><green>
        - index can also include <b>doc={dictionary}</b> where the dictionary contains terms
          to create an index entry. This will use the specified index to search only for the
          data specified in the dictionary.
        - each field can also be postfixed with a <b>':'</b> which can introduce justification,
          column width specification, and custom formatting. The form is;
          <b>:[&gt;|&lt;][width][@custom]</b>
          So <b>fred:>10</b> would right justify the field "fred" in a column of width 10 and
          <b>fred:@date</b> would apply the custom date formatter to convert a date/time stamp into
          a human readable datetime string.</green>

        <b>Examples:</b><green>
        Assuming a table called <b>envelopes</b> with an index of <b>tags</b> where the attribute
        <b>tags</b> is a list, to do an indexed lookup of the first 10 rows tagged with 'SPAM'
        using the <b>by_tags</b> index;</green>

        <blue>select envelopes date:@date,subject,tags index=by_tags doc={"tags": ["SPAM"]}</blue><brown>
        ┌─────────────────────┬─────────────────────────────────────────────────┬───────────────────┐
        │ date                │ subject                                         │ tags              │
        ├─────────────────────┼─────────────────────────────────────────────────┼───────────────────┤
        │ 2021-08-02 18:38:40 │ Re: Any type of Website Ranking Issue.          │ ['SPAM', 'TRASH'] │
        │ 2021-08-06 18:16:52 │ GOD BLESS YOU!                                  │ ['SPAM', 'TRASH'] │
        │ 2021-08-05 15:12:57 │ Re: Increase traffic on your website !!!        │ ['SPAM', 'TRASH'] │
        │ 2021-08-04 01:35:31 │ Re: Increase Traffic on your website.           │ ['SPAM', 'TRASH'] │
        │ 2021-08-04 00:40:42 │ Re: A Quick Call to Discuss Website Proposal.   │ ['SPAM', 'TRASH'] │
        │ 2021-08-04 02:01:16 │ Re: Any type of Website Ranking Issue.          │ ['SPAM', 'TRASH'] │
        │ 2021-08-05 23:49:27 │ Re-Designing and Re-Developing Your Website !!! │ ['SPAM', 'TRASH'] │
        │ 2021-08-04 23:06:57 │ Re: Increase Traffic on your website.           │ ['SPAM', 'TRASH'] │
        │ 2021-08-04 22:22:06 │ Re: A Quick Call to Discuss Website Proposal.   │ ['SPAM', 'TRASH'] │
        │ 2021-08-08 11:51:24 │ Re: Are you on the top #1st page of Google?     │ ['SPAM', 'TRASH'] │
        └─────────────────────┴─────────────────────────────────────────────────┴───────────────────┘
        Displayed 10 records in 0.0014s (Limited view) 7225/sec</brown>

        <b>Notes:</b><green>
        There is scope for adding custom formatters depending on your date, another formatter is <b>email</b>
        which expects either a single or list of dictionary items containing 'hostname' and 'mailbox' (and
        optionally 'name') attributes.</green>
        """

    def exit(self):
        return self.quit()

    def do_quit(self):
        return """
        <b>quit</b> - exit the shell

        <b>Notes:</b><green>
        - the shell will also exit on <b>exit</b> or <b>Ctrl+D</b></green>
        """

    def do_use(self):
        return """
        <b>use</b> - select the database to operate on

        <green><b>use [database]</b>   - select [database] as the current database</green>

        <b>Notes:</b><green>
        - the current prompt will be set to the selected database name assuming it can be opened</green>
        """

    def do_register(self):
        return """
        <b>register</b> - tell the shell about a new database

        <green><b>register [name] [database]</b>  - register a database called [name] with the path [path]</green>

        <b>Examples:</b><green>
        none&gt; show databases</green><brown>
        ┌───────────────┬──────────┬─────────┬─────┬─────────────────────────────────────────────┐
        │ Database name │   Mapped │    Used │ (%) │ Path                                        │
        ├───────────────┼──────────┼─────────┼─────┼─────────────────────────────────────────────┤
        │ starwars      │   32.00G │   0.00G │   0 │ /home/gareth/scm/graphql-examples/star-wars │
        │ orbit         │   32.00G │  16.25G │  50 │ /home/sandbox/scm/Orb/server/.database      │
        └───────────────┴──────────┴─────────┴─────┴─────────────────────────────────────────────┘</brown><green>
        none&gt; register sw /home/gareth/scm/graphql-examples/sw</green>
        <brown>Registered sw => /home/gareth/scm/graphql-examples/sw</brown>

        <green>none&gt; show databases</green><brown>
        ┌───────────────┬──────────┬─────────┬─────┬─────────────────────────────────────────────┐
        │ Database name │   Mapped │    Used │ (%) │ Path                                        │
        ├───────────────┼──────────┼─────────┼─────┼─────────────────────────────────────────────┤
        │ starwars      │   32.00G │   0.00G │   0 │ /home/gareth/scm/graphql-examples/star-wars │
        │ orbit         │   32.00G │  16.25G │  50 │ /home/sandbox/scm/Orb/server/.database      │
        │ sw            │   24.00K │  24.00K │ 100 │ /home/gareth/scm/graphql-examples/sw        │
        └───────────────┴──────────┴─────────┴─────┴─────────────────────────────────────────────┘</brown>

        <b>Notes:</b><green>
        - the specified path is the path to the directory containing the database's <b>.mdb</b> files.
        - following registration, the database will show up in the results of <b>show databases</b></green>
        """

    def do_explain(self):
        return """
        <b>explain</b> - provide some insight into the structure of records within a table

        <green><b>explain [table]</b> - provide a breakdown of the specified table's record structure</green>

        <b>Examples:</b><green>
        orbit> explain envelopes</green><brown>
        ┌─────────────────┬─────────────┬─────────────────────────────────────────────────────────────────┐
        │ Field name      │ Field Types │ Sample                                                          │
        ├─────────────────┼─────────────┼─────────────────────────────────────────────────────────────────┤
        │ date            │ ['float']   │                                                    1628419884.0 │
        │ subject         │ ['str']     │ Re: Are you on the top #1st page of Google?                     │
        │ from_           │ ['list']    │ [{'mailbox': 'kate', 'host': 'chipxworld.online'}]              │
        │ sender          │ ['list']    │ [{'mailbox': 'kate', 'host': 'chipxworld.online'}]              │
        │ reply_to        │ ['list']    │ [{'mailbox': 'katewebseox', 'host': 'gmail.com'}]               │
        │ to              │ ['list']    │ [{'mailbox': 'zathras', 'host': 'linux.co.uk'}]                 │
        │ account_id      │ ['str']     │ 41d845464f98c9c5005732a7b982                                    │
        │ message_id      │ ['str']     │ f0a7f3f72b5d386bea9ccb6a0beb661cda8f10256d2a36b85726421535af... │
        │ tags            │ ['list']    │ ['SPAM', 'TRASH']                                               │
        │ message_body_id │ ['str']     │ 41d843edcb01000341d84546502227fcb986                            │
        │ description     │ ['str']     │ Hi, Hope you are doing well. Are you looking to get SEO done... │
        │ spam_score      │ ['str']     │ 8.5                                                             │
        └─────────────────┴─────────────┴─────────────────────────────────────────────────────────────────┘</brown>

        <b>Notes:</b><green>
        - although NoSQL tables have no formal schema, recommended practice is to group items with
          similar structures into one table. Explain works by scanning a small subset of records and
          showing all fields found (i.e. a union of fields from all records) with some sample date
          for each field. So not every record will necessarily contain all of the fields listed, however
          all of the fields listed exist in at least some of the records.
        - note that there may be more fields available in the database if they only exist in some records,
          i.e. none of the records in explain's sample.</green>
        """

    def do_clear(self):
        return """
        <b>clear</b> - clear all records from the table leaving the indexes intact

        <green><b>clear [table]</b> - delete all records from the specified table</green>

        <b>Examples:</b><green>
        orbit> clear envelopes</green><brown>

        <b>Notes:</b><green>
        - there is no confirmation, this will immediately rip through your table</green></brown>
        """

    def do_unique(self):
        return """
        <b>unique</b> - provide a count of the number of records with a given field in common

        <green><b>unique [table] [field]</b>               - scan the entire database and count the number of each field</green>
        <green><b>unique [table] [field] index=[index]</b> - as above, but use the names index (much faster)</green>

        <b>Examples:</b><green>
        orbit> explain envelopes tags</green><brown>
        ┌──────────────────┬────────┐
        │ tags             │ count  │
        ├──────────────────┼────────┤
        │ 1999             │    376 │
        │ 2000             │     56 │
        ...
        │ TODO             │      2 │
        │ TRASH            │    555 │
        │ UNREAD           │    247 │
        └──────────────────┴────────┘
        Displayed 36 records in 2.2171s  16/sec</brown><green>

        The above example scanned around 200,000 records and around 8G of actual raw data, if
        we try the same thing again with an index, well, you get the idea;

        orbit> unique envelopes tags index=by_tags</green><brown>
        ┌──────────────────┬────────┐
        │ tags             │ count  │
        ├──────────────────┼────────┤
        │ 1999             │    376 │
        │ 2000             │     56 │
        ...
        │ TODO             │      2 │
        │ TRASH            │    555 │
        │ UNREAD           │    247 │
        └──────────────────┴────────┘
        Displayed 36 records in 0.0005s  73022/sec</brown>

        Just for context, this would be the equivalent of;
        <b>SQL> select tag, count(distinct tag) from envelopes;</b>

        <b>Notes:</b><green>
        - yes, this might sound crazy, but you can have 200,000 records, add an array of tags to each record,
          then summarize the entire collection (i.e. count of the number of each type of tag available) in
          half a millisecond.</green>
        """

    def do_analyse(self):
        return """
        <b>analyse</b> - dig down into the record size distribution for a given table

        <green><b>analyse [table]</b> - provide a basic chart showing record size distribution</green>

        <b>Examples:</b><green>
        orbit> analyse envelopes</green><brown>

        Breakdown of record size distribution
        ###############################################################################
        █████████████████████████████████████████████████████████████████████  95K  980
        █████████████████████████████████████████████████████████████████      90K  1K
                                                                                85  2K
                                                                                13  3K
                                                                                 2  4K
                                                                                 2  5K
                                                                                 1  6K
                                                                                 1  7K
                                                                                 4  8K
                                                                                 0  9K
                                                                                 0  10K
                                                                                 0  11K
                                                                                 1  12K
                                                                                 0  13K
                                                                                 0  14K
                                                                                 2  15K
                                                                                 0  16K
                                                                                 0  17K
                                                                                 0  18K
                                                                                 0  19K
                                                                                 1  20K
        Displayed 189456 records in 0.3258s  581431/sec</brown>

        <b>Notes:</b><green>
        - this becomes important for determining performance, bottlenecks etc.
        - in this example, the vast majority of records are under 2K in size
        - the entire table is read in order to determine record sizes, so for
          large tables, be prepared to wait ...</green>
        """

    def do_dump(self):
        return """
        <b>dump</b> - display the raw contents of a given record

        <green><b>dump [table] [_id]</b> - dump out the record with <b>_id</b> from [table]</green>

        <b>Examples:</b><green>
        orbit> dump envelopes 41d845464ffe9985005732a7b986</green><brown>
        {
            "date": 1628037331.0,
            "subject": "Re: Increase Traffic on your website.",
            "from_": [
                {
                    "mailbox": "len",
                    "host": "silverxlead.online"
                }
            ],
            "to": [
                {
                    "name": "Recipients",
                    "mailbox": "len",
                    "host": "silverxlead.online"
                }
            ],
            "account_id": "41d845464f98c9c5005732a7b982",
            "message_id": "50ca8b8ae3ba4a35b7c53e0960a5d9740d40c4a8cc7a881bb461ad92baa7f884",
            "tags": [
                "SPAM",
                "TRASH"
            ],
            "message_body_id": "41d8427834c0100341d845464ffe87f1b986",
            "description": "Hello, I have noticed that the keywords you\u2019ve been using ...",
            "spam_score": "10.1"
        }</brown>

        <b>Notes:</b><green>
        - if the record is in JSON format (which it would be by default) it is dumped in a colourized
          structured format. If on the other hand the table is in RAW mode, then the raw data is dumped
          with no structure or colour manipulation.</green>
        """

    def do_lexicon(self):
        return """
        <b>lexicon</b> - interrogate the lexicon for a full-text index

        <green><b>lexicon [table] [index] [term]</b> - show the first 10 matching items for [term]</green>

        <b>Examples:</b><green>
        orbit> lexicon messages by_raw gareth</green><brown>
        ┌──────────────────────┬────────┐
        │ Term                 │ Count  │
        ├──────────────────────┼────────┤
        │ gareth               │ 177490 │
        │ gareth.a             │      7 │
        │ gareth.2011          │      3 │
        │ gareth.01443         │      2 │
        │ gareth.01            │      1 │
        │ gareth.08            │      1 │
        │ gareth.10            │      1 │
        │ gareth.109.70.157.46 │      1 │
        │ gareth.110           │      1 │
        │ gareth.192.168.1.166 │      1 │
        └──────────────────────┴────────┘
        Displayed 10 records in 0.0884s  113/sec</brown><green>

        orbit> lexicon messages by_raw woz</green><brown>
        ┌─────────┬───────┐
        │ Term    │ Count │
        ├─────────┼───────┤
        │ woz     │    70 │
        │ wozniak │     8 │
        │ wozn    │     1 │
        │ wozzeck │     1 │
        └─────────┴───────┘
        Displayed 4 records in 0.0026s  1537/sec</brown>

        <b>Notes:</b><green>
        - this command was designed to facilitate 'search as you type' word lookup functionality
          for full-text indexes. As a rule of thumb, the more results, the longer the search takes.</green>
        """
    
    def do_fix(self):
        return """
        <b>fix</b> - remove a root key from the database index (DANGEROUS!)

        <green><b>fix bad root [key]</b> remove the specified key from the index</green>
        
        <green>This is for fixing database errors, don't use it unless you know what you are doing. For example it
        can be used to fix an 'incompatible flags' issue where a node has been written as a key into what should be a list
        of sub-databases. If you do this on a key that is a database, it will vanish!</green>
        """

    def do_match(self):
        return """
        <b>match</b> - recover a results list from a full text index based on a search term

        <green><b>match [table] [index] [term]</b> - show the first 10 matching items for [term]</green>

        <b>Examples:</b><green>
        orbit> match messages by_raw "gareth,woz"</green><brown>
        ┌─────────────────────────────────────────┐
        │ _id                                     │
        ├─────────────────────────────────────────┤
        │ 41cc1188c800000041d8454687aab435b9b1    │
        │ 41cc1e82c080000041d845468fcfc03fb9b1    │
        │ 41cc2b267600000041d84546947b7dd2b9b1    │
        │ 41cc2be18400000041d845469315c1a6b9b1    │
        │ 41cc2fba5f00000041d8454682b1fa32b9b1    │
        │ 41cc466af200000041d84546c97ea9dab9b4    │
        │ 41cc56039700000041d84546d0016e75b9b4    │
        │ 41cc668fce80000041d84546bfaf7cfbb9b3    │
        │ 41cc75004b80000041d84546c5920addb9b3    │
        │ 41cc7501f680000041d84546c5b93893b9b3    │
        └─────────────────────────────────────────┘
        Displayed 69 records in 0.0003s (Limited view) 244680/sec</brown>

        <green>orbit> match messages by_raw "gareth"</green><brown>
        ┌─────────────────────────────────────────┐
        │ _id                                     │
        ├─────────────────────────────────────────┤
        │ 41cb47dbc980000041d8454694fcc8c3b9b0    │
        │ 41cb57846f80000041d8454694f58efcb9b0    │
        │ 41cb6ee55280000041d8454694f23439b9b0    │
        │ 41cb6ee56b00000041d8454695127f95b9b0    │
        │ 41cb6f241d00000041d84546950cc66db9b0    │
        │ 41cb6f466380000041d84546950ad706b9b0    │
        │ 41cb6f466e00000041d8454695097107b9b0    │
        │ 41cb6f542580000041d8454695071b3db9b0    │
        │ 41cb6f550100000041d8454695250a61b9b0    │
        │ 41cb71d55380000041d8454695228c02b9b0    │
        └─────────────────────────────────────────┘
        Displayed 177375 records in 0.2295s (Limited view) 772845/sec</brown>

        <green>orbit> dump messages 41cc56039700000041d84546d0016e75b9b4</green><brown>
        b'Received: by server.net  id\r\n\t%lt;01BF00EF.7EF3E4C0@server.net&gt;;
        etc...</brown>

        <b>Notes:</b><green>
        - this example is showing records from a full-text index that contain the words <b>gareth</b>
          and <b>woz</b>, any number of terms can be added with little / no performance penalty.
        - generally this is very quick, but as you can see, the more matches, the slower it gets.</green>
        """
    
    def do_mode(self):
        return """
        <b>mode</b> - switch between basic and advanced views
               in <b>user</b> mode, 'normal' tables only are shown
               in <b>advanced</b> mode, all tables including indexes and metadata are shown
        """
    def do_delete(self):
        return """
        <b>delete</b> - delete a record from a table

        <green><b>delete table_name primary_key</b> - delete the record with primary_ley from table_name</green>

        <b>Examples:</b>
        vcheck> <green>delete</green> <brown>filecache</brown> <orange>41d90b1947bfbc36005732a7bf9a</orange>
        <red>delete "41d90b1947bfbc36005732a7bf9a" from "filecache"</red>
        """

    def do_import(self):
        return """
        <b>import</b> - import data from a local MySQL database

        <green><b>import database_name table_name</b> - import the MySQL table "table_name" from the MySQL database "database_name"</green>
        <green><b>import database_name *</b>          - import all MySQL tables from the MySQL database "database_name"</green>

        <b>Examples:</b>
        <cadetblue>none></cadetblue> <brown>create sql /home/sandbox/.local/sqlsandbox</brown>
        <green>Registered sql => /home/sandbox/.local/sqlsandbox</green>
        <cadetblue>none></cadetblue> <brown>use sql</brown>
        <cadetblue>sql></cadetblue> import linuxforum smf_geoip_regions
        <green>100%|███████████████████████████████████████████████████████████| 4056/4056 [49505.87it/s]</green>
        <green>Imported 4056 rows into smf_geoip_regions</green>
        <green>Completed in 0:00:00.097857 seconds</green>
        <cadetblue>sql></cadetblue> <brown>select smf-geoip-regions *</brown><cadetblue>
        ┏━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ cc    ┃ rc   ┃ rn                              ┃
        ┡━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ CA    │ AB   │ Alberta                         │
        │ CA    │ BC   │ British Columbia                │
        │ CA    │ MB   │ Manitoba                        │
        │ CA    │ NB   │ New Brunswick                   │
        │ CA    │ NL   │ Newfoundland                    │
        │ CA    │ NS   │ Nova Scotia                     │
        │ CA    │ NU   │ Nunavut                         │
        │ CA    │ ON   │ Ontario                         │
        │ CA    │ PE   │ Prince Edward Island            │
        │ CA    │ QC   │ Quebec                          │
        └───────┴──────┴─────────────────────────────────┘</cadetblue>
        <green>Time: 0.0000s => 204080/sec (Limited view[10])  </green>
        """

    def do_drop(self):
        return """
        <b>drop</b> - drop a table or index from the database

        <green><b>drop table [index]</b> drop the specified table, or index if specified</green>
        <b>Examples:</b>
        <cadetblue>none></cadetblue> <brown>use sql</brown>
        <cadetblue>sql></cadetblue> <brown>show tables</brown>
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ Table name        ┃ #Recs ┃ Codec ┃ Depth ┃ Oflow% ┃ Index names ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
        │ smf-geoip-regions │ 4056  │ ujson │ 2     │ 0.0    │             │
        └───────────────────┴───────┴───────┴───────┴────────┴─────────────┘
        <cadetblue>sql></cadetblue> <brown>drop smf-geoip-regions</brown>
        Table smf-geoip-regions dropped!
        <cadetblue>sql></cadetblue> <brown>show tables</brown>
        ┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ Table name ┃ #Recs ┃ Codec ┃ Depth ┃ Oflow% ┃ Index names ┃
        ┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
        └────────────┴───────┴───────┴───────┴────────┴─────────────┘
        """

    def do_create (self):
        return """
        <b>import</b> - create a new database and register it with the database shell

        <green><b>create database_name path_to_database</b> - create a folder called path_to_database/database_name</green>

        <b>Examples:</b>
        <cadetblue>none></cadetblue> <brown>create sql /home/sandbox/.local/sqlsandbox</brown>
        <green>Registered sql => /home/sandbox/.local/sqlsandbox</green>
        """
    
    def do_load (self):
        return """
        <b>load</b> - load a raw JSON formatted file and store it in a new table

        <green><b>load table_name pathname</b> - load records from path_name into table table_name</green>

        <b>Examples:</b>
        <cadetblue>sql></cadetblue> <brown>load mimedb /tmp/mimedb.json</brown>
        <cadetblue>sql></cadetblue> <brown>show tables</brown>
        ┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ Table name ┃ #Recs ┃ Codec ┃ Depth ┃ Oflow% ┃ Index names ┃
        ┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
        │ mimedb     │ 1860  │ ujson │ 2     │ 0.0    │             │
        └────────────┴───────┴───────┴───────┴────────┴─────────────┘
        <cadetblue>sql></cadetblue> <brown>save mimedb /tmp/mimedb2.json</brown>
        Export of mimedb => /tmp/mimedb2.json is complete
        <cadetblue>sql></cadetblue> <brown>load mimedb2 /tmp/mimedb2.json</brown>
        <cadetblue>sql></cadetblue> <brown>show tables</brown>
        ┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ Table name ┃ #Recs ┃ Codec ┃ Depth ┃ Oflow% ┃ Index names ┃
        ┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
        │ mimedb     │ 1860  │ ujson │ 2     │ 0.0    │             │
        │ mimedb2    │ 1860  │ ujson │ 2     │ 0.0    │             │
        └────────────┴───────┴───────┴───────┴────────┴─────────────┘
        """
    
    def do_save (self):
        return """
        <b>save</b> - save a table to JSON formatted file

        <green><b>save table_name pathname</b> - save records to path_name from table table_name</green>

        <b>Examples:</b>
        <cadetblue>sql></cadetblue> <brown>load mimedb /tmp/mimedb.json</brown>
        <cadetblue>sql></cadetblue> <brown>show tables</brown>
        ┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ Table name ┃ #Recs ┃ Codec ┃ Depth ┃ Oflow% ┃ Index names ┃
        ┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
        │ mimedb     │ 1860  │ ujson │ 2     │ 0.0    │             │
        └────────────┴───────┴───────┴───────┴────────┴─────────────┘
        <cadetblue>sql></cadetblue> <brown>save mimedb /tmp/mimedb2.json</brown>
        Export of mimedb => /tmp/mimedb2.json is complete
        <cadetblue>sql></cadetblue> <brown>load mimedb2 /tmp/mimedb2.json</brown>
        <cadetblue>sql></cadetblue> <brown>show tables</brown>
        ┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ Table name ┃ #Recs ┃ Codec ┃ Depth ┃ Oflow% ┃ Index names ┃
        ┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
        │ mimedb     │ 1860  │ ujson │ 2     │ 0.0    │             │
        │ mimedb2    │ 1860  │ ujson │ 2     │ 0.0    │             │
        └────────────┴───────┴───────┴───────┴────────┴─────────────┘
        """    