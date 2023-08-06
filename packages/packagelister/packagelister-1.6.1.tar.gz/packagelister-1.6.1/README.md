# packagelister
Determine what packages and versions a project imports. <br>
Install with:
<pre>pip install packagelister</pre>

Only has one function: <pre>packagelister.scan()</pre><br>
It takes one optional argument and that is the directory or file to scan.<br>
If an argument isn't given, the current working directory will be scanned.

<br>
Usage:
<pre>
>>> from pathlib import Path
>>> import packagelister
>>> import json
>>> packages = packagelister.scan()
 [___________________________________________________]-100.00% Scanning packagelister.py
>>> print(json.dumps(packages, indent=2))
{
  "pathcrawler": {
    "files": [
      "src/packagelister/packagelister.py"
    ],
    "version": "0.1.0"
  },
  "printbuddies": {
    "files": [
      "src/packagelister/packagelister.py"
    ],
    "version": "0.4.1"
  }
}
</pre>
Can also be used as a cli tool:
<pre>
>packagelister packagelister -sf
 [___________________________________________________]-100.00% Scanning packagelister_cli.py
Packages used in packagelister:
pathcrawler==0.0.3     src\packagelister\packagelister.py
printbuddies==0.2.2    src\packagelister\packagelister.py
</pre>
Cli help:
<pre>
>packagelister -h
usage: packagelister_cli.py [-h] [-sf] [-gr] [-ib] [project_path]

positional arguments:
  project_path          The project directory path to scan.

options:
  -h, --help            show this help message and exit
  -sf, --show_files     Show which files imported each of the packages.
  -gr, --generate_requirements
                        Generate a requirements.txt file in --project_path.
  -ib, --include-builtins
                        Include built in standard library modules.
</pre>