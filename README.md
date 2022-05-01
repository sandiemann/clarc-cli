#clarc (CommandLine Archiva)

clarc is a simple CLI tool to archive data like day-to-day commands, notes, text, passcodes etc.
The data is stored in a shared sqlite in-memory connection and can be archived & retrieved with helpful commands.
The output response is shown in the terminal as json.
##Install
* Install the dependencies:
```sh
$ python -m pip install -r requirements.txt
```
* Initialize the application (database initialize):
```sh
$ python -m clarc init
```

##Usage
```sh
$python -m clarc --help
Usage: clarc [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  fetch   fetch the archived entries '--all' or by '--key' ${key}
  init    initialize the database.
  remove  remove an archived entry by specefic --key' ${key}
  upsert  update on duplicate key else insert a new entry to db
```

## Features
**clarc** has the following features:

| Command    | Description      |
| :------------ |   :---:       | 
| `init`        | Initializes the application's sqlite database.| 
| `upsert`         | insert or update a new entry to the database with a `key:value` pair.         | 
| `fetch`         | fetch all or a specific entry by key from database.         | 
| `remove`         | removes an entry from db by `key` from database         | 

## Release History
- 0.1.0
