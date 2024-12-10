#!/home/shawn/venv/eapi-test/bin/python3
import argparse
import jsonrpclib
import sys
import pprint

def main():
    parser = argparse.ArgumentParser(description="Run commands on one or more Arista switches")
    parser.add_argument("switches", metavar="SWITCH", nargs="+",
                        help="Hostname or IP of the switch to query")
    parser.add_argument('-a', '--ascii', default=False, action="store_true",
                        help="Enable ASCII output (json is default)")
    parser.add_argument('-A', '--expandalias', default=False, action="store_true",
                        help="Expand aliases when run on the switch")
    parser.add_argument('-C', '--autocomplete', default=False, action="store_true",
                        help="Enable autocomplete for commands")
    parser.add_argument('-c', '--command', action='append',
                        help="Command to be run on the switch(es)")
    parser.add_argument('-f', '--filename', action='append',
                        help="Name of a file with commands to be run")
    parser.add_argument('-p', "--password", default="admin",
                        help="The user's password (default is 'admin')")
    parser.add_argument('-e', "--enable", action="store_true",
                        help="Execute 'enable' before running commands")
    parser.add_argument("-s","--https", help="Use HTTPS instead of HTTP",
                        action="store_const", const="https", default="http")
    parser.add_argument('-u', "--username", help="Name of the user to connect as (default is admin)",
                        default="admin")
    args = parser.parse_args()
    # Either -c or -f must be selected 
    if not (args.command or args.filename):
        parser.error("At least one of -c or -f must be specified.")
    apiEndpoints = getEndpoints(args.switches, args.https,
                               args.username, args.password)
    cmdList = []
    if args.enable:
        cmdList = ['enable']
    if args.command != None:
        for cmd in args.command:
            cmdList.append(cmd)
    if args.filename != None:
        for file in args.filename:
            with open(file) as fh:
                for line in fh:
                    cmdList.append(line)
    if args.ascii:
        output="text"
    else:
        output="json"
    if cmdList:
            runCmds(apiEndpoints, cmdList, output, args.autocomplete, args.expandalias)
    
def getEndpoints(switchHostnames, protocol, username, password):
    """ Check that each server is up, and return a mapping from
    hostname to jsonrpclib.Server """
    apiEndpoints = {} # mapping from hostname to the API endpoint
    for switch in switchHostnames:
       url = "{protocol}://{user}:{pw}@{hostname}/command-api".format(
          protocol=protocol, user=username, pw=password, hostname=switch)
       server = jsonrpclib.Server(url)
       try:
          # We should at least be able to 'enable'
          server.runCmds(1, ["show hostname"])
       except Exception as e:
          print("Unable to run 'show hostname' on " + switch)
          sys.exit(1)
       apiEndpoints[switch] = server
    return apiEndpoints
 
def runCmds(endpoints, cmdList, output, acomplete, aliases):
    for rtr in endpoints:
        try:
            result = endpoints[rtr].runCmds(version=1, cmds=cmdList, format=output, autoComplete=acomplete, expandAliases=aliases)
        except jsonrpclib.ProtocolError as e:
                print("[ERROR]")
                print("  ", e)
                # jsonrpclib isn't very friendly at getting the error data as
                # specified by the spec. This is a shortcut for getting the
                # last error:
                errorResponse = jsonrpclib.loads(jsonrpclib.history.response)
                print("   Details:", errorResponse["error"]["data"][-1]["errors"])
                print(jsonrpclib.history.request)
        else:
            if output == "json":
                pprint.pp(result)
            elif output == "text":
                for i in result:
                    print(i['output'])
                

if __name__ == "__main__":
    main()