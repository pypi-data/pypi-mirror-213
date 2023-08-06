# pylint: disable=too-many-branches,too-many-statements,too-many-locals
#   All three of these Pylint exceptions are because this module is basically
#   one top-to-bottom procedure.
"""
Smash xbar client.  Displays status in format usable for [xbar](xbarapp.com).
"""
import os
import sys
from datetime import datetime
import requests
from smash import config
from smash import smash


def local_timestamp_from_javascript(reported):
    """
    Convert Javascript-style UTC timestamp to local readable one.  For
    example:
        given "2023-06-11T16:28:26.902741Z",
        returns "2023-06-11 09:28:26 PDT"
    """
    ts_utc = datetime.strptime(reported, "%Y-%m-%dT%H:%M:%S.%f%z")
    ts_local = ts_utc.astimezone()
    return ts_local.strftime("%Y-%m-%d %H:%M:%S %Z")


def xbar():
    """ Interpret Smash node and status information as menus for xbar.
    """
    # load configuration
    # pylint: disable=invalid-name,broad-except
    try:
        conf = config.xbar()
        conf.merge()
    except Exception as e:
        print(f"{config.APP_TAG} | color={smash.state_colours['unknown']}")
        print("---")
        print(f"Could not load Smash configuration: {e}")
        return

    api_url = conf['server'] + '/api'
    timeout = conf['request_timeout']

    # load node and status information
    try:
        nodes = smash.load_nodes(api_url, timeout)
    except requests.exceptions.ConnectionError:
        print(f"{config.APP_TAG} | color={smash.state_colours['unknown']}")
        print("---")
        print("Could not connect to Smash server")
        return

    # now do the BitBar/xbar stuff
    # TODO: move this stuff to APIHandler object?
    # determine and present the overall status in menu bar
    (overall, summary) = smash.overall_state(smash.state_totals)
    colour = smash.state_colours[overall]
    print(f"{config.APP_TAG} | color={colour}")
    print("---")

    # create menu entries for each node and its status items
    for node in nodes:

        # determine overall node status
        (overall, summary) = smash.overall_state(node['totals'])

        # present menu entry for node
        if overall == 'okay':
            print(node['node'])
        else:
            colour = smash.state_colours[overall]
            print(f"{node['node']} {smash.state_icons[overall]} {summary} | color={colour}")

        # build menu of node statuses
        for status in node['statuses']:
            nodename = node['node']
            test = status['test']
            state = status['state']
            message = status['message']
            reported = local_timestamp_from_javascript(status['reported'])

            # set basic status text
            status_text = f"{status['test']} {state} {message}"

            # enable acknowledgement if appropriate
            command = None
            alt_text = None
            if 'acknowledgement' in status:
                colour = 'blue'
                icon = ':see_no_evil:'
                message += ' (acknowledged)'
                # TODO: not implemented
                #command = f"unack {nodename}:{test}"
            else:
                colour = smash.state_colours[state]
                icon = smash.state_icons[state]
                if state != 'okay':
                    command = f"ack -s {state} {nodename}:{test}"
                    alt_text = f"Acknowledge {state} on {status['test']} (reported {reported})"
            if not alt_text:
                alt_text = f"{status['test']} reported {reported}"

            line = ""

            if icon:
                line += f"--{icon} "
            else:
                line += "--"
            alt = line

            line += f"{status_text} | color={colour}"
            alt += f"{alt_text} | color={colour} alternate=true"

            if command is not None:
                cmdlets = command.split()

                # extract callable
                smash_path = os.path.dirname(os.path.abspath(sys.argv[0]))
                smash_exec = f"{smash_path}/smash"
                alt += f" | shell={smash_exec}"

                # extract arguments
                for idx, arg in enumerate(cmdlets[0:]):
                    alt += f" param{idx+1}={arg}"

                # add terminal etc options
                alt += " terminal=false refresh=true"

            print(line)
            print(alt)


# if this module was called directly
if __name__ == '__main__':
    xbar()
