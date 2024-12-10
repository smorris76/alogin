# alogin
alogin is python code to send commands to Arista devices via eAPI. It can be run as a standalone script or be used as a library for other scripts.

```
usage: alogin.py [-h] [-a] [-A] [-C] [-c COMMAND] [-f FILENAME] [-p PASSWORD] [-e] [-s] [-u USERNAME]
                 SWITCH [SWITCH ...]

Run commands on one or more Arista switches

positional arguments:
  SWITCH                Hostname or IP of the switch to query

options:
  -h, --help            show this help message and exit
  -a, --ascii           Enable ASCII output (json is default)
  -A, --expandalias     Expand aliases when run on the switch
  -C, --autocomplete    Enable autocomplete for commands
  -c COMMAND, --command COMMAND
                        Command to be run on the switch(es)
  -f FILENAME, --filename FILENAME
                        Name of a file with commands to be run
  -p PASSWORD, --password PASSWORD
                        The user's password (default is 'admin')
  -e, --enable          Execute 'enable' before running commands
  -s, --https           Use HTTPS instead of HTTP
  -u USERNAME, --username USERNAME
                        Name of the user to connect as (default is admin)
```

Commands passed via '-c' ore processed in command-line order. Command files passed via '-f' are processed next and again in command-line order.