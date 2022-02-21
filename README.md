# Dnotes from SQLite DB to .md

This short program was written specifically for automatically retrieving notes from a Dnote database (https://github.com/dnote/dnote) and creating .md files for each note while also creating folders with the Dnote books' names.

With a little modification, the same extraction can be used on other Sqlite3 databases.


#### Usage:
```cmd
python3 dnotes_to_md.py <database file path> [<output folder name>]
```
