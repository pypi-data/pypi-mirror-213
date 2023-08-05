# Orbit Database Shell - Introduction

#### Welcome to the Orbit Database Shell repository and documentation. All project documentation is included within this repository and consists of markdown files and comments within the code. These are presented in real time by the "ZeroDocs" Orbit application which renders this content to HTML.

This project is the command line shell for the NoSQL database that underpins the Orbit Framework. It performs in much the same way as the MySQL shell other than it works with Orbit Databases rather than MySQL databases. Maybe with a few other visualisation improvements.

<table><tr><td width="50%"><img width="100%" src="https://gitlab.com/madpenguin/orbit-database-shell/-/raw/main/images/screenshot.png" /></td><td width="50%">
<h3 style="padding-left:1.4em">Features</h3>

* The ability to create and manage multiple databases
* Drill-down and testing facilities
* Examine data and database structures
* Import and export JSON data, import data directly from MySQL
* Grammar, colourisation and auto-complete for everything
* Operation timing and data size distribution analysis
* Detailed help system with examples
* It's all written in Python and it's <b>very</b> extensible

</td></tr></table>

### Installation

Start off by creating a virtual environment using the tool of your choosing (we currently use "pyenv") then (don't forget to activate the environment) do;
```bash
pip install orbit_database_shell
```
And to run the shell just do;

```bash
$ orbit_database_shell 

  .oooooo.             .o8        o8o      .           oooooooooo.   oooooooooo.
 d8P'  `Y8b           "888        `"'    .o8           `888'   `Y8b  `888'   `Y8b
888      888 oooo d8b  888oooo.  oooo  .o888oo          888      888  888     888
888      888 `888""8P  d88' `88b `888    888            888      888  888oooo888'
888      888  888      888   888  888    888   8888888  888      888  888    `88b
`88b    d88'  888      888   888  888    888 .          888     d88'  888    .88P
 `Y8bood8P'  d888b     `Y8bod8P' o888o   "888"         o888bood8P'   o888bood8P'

     Orbit Database Command Line Tool (c) Mad Penguin Consulting Ltd 2023
     To get started try help register or help for all available commands
none> 
```

And you're live ...