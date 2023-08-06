### mindmap: Command line tool for keeping notes simple way.

use pyenv (recommended), tested python 3.8.5
- https://github.com/pyenv/pyenv


#### Installation:
```
$ pip install mindmap
$ mindmap -r

```

#### Usage
```
$ mindmap 
usage: Command line tool for keeping notes simple way. [-h] [-s SCOPE [SCOPE ...]] [-q QUERY] [-i INDEX]
                                                       [-t TEXT] [-a] [-v] [-r] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -s SCOPE [SCOPE ...], --scope SCOPE [SCOPE ...]
                        scope of the note.
  -q QUERY, --query QUERY
                        search file names in scope.
  -i INDEX, --index INDEX
                        use index of the file.
  -t TEXT, --text TEXT  append text to scope content.
  -a, --all             set scope to all
  -v, --vim             save the content of vim
  -r, --read            print content of the scope.
  -l, --list            list files in scope.

```