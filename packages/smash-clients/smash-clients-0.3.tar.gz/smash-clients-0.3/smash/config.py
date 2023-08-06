# pylint:
#
"""
Smash configuration.
"""
import os.path
import argparse
import re
import mergeconf

# constants
#
# application identifiers
APP_TAG = "Smash"
APP_NAME = "smash"

# default configuration file paths
CONFIG_FILE_PATHS = [
    f"{os.path.abspath(os.path.curdir)}/{APP_NAME}.conf",
    os.path.expanduser(f"~/.config/{APP_NAME}.conf"),
    f"/etc/{APP_NAME}.conf"
]

def determine_config_file():
    """
    Determine configuration file to use.

    Returns:
        Configuration file path or None if nothing suitable found.
    """
    for path in CONFIG_FILE_PATHS:
        if os.path.exists(path):
            return path
    return None


def common():
    """ General/common client configuration.
    """
    conf = mergeconf.MergeConf(APP_TAG, files=determine_config_file())
    conf.add('server', mandatory=True)
    conf.add('request_timeout', type=int, value=30,
        description='Time limit for requests to server in seconds (default 30)')

    # get command-line options
    parser = argparse.ArgumentParser(prog=APP_NAME)
    parser.add_argument("-c", "--config", type=str,
                      help="Configuration file",
                      default=determine_config_file())
    parser.add_argument("--json", action='store_true',
                      help="Provide output in JSON format")
    #parser.add_argument("-d", "--debug",
    #                    help="Debug output",
    #                    action='store_true')
    #parser.add_argument("-q", "--quiet",
    #                    help="No output",
    #                    action='store_true')
    # patch in argument parser
    conf.argparser = parser

    return conf

def xbar():
    """ xbar client configuration.
    """
    return common()

def cli():
    """ CLI client configuration.
    """

    class NodeStatusSplitAction(argparse.Action):
        """ Action for splitting `node:status` parameters.

        TODO: will this integrate with Mergeconf?  If not maybe the way the
        values are set can be changed.
        """

        @staticmethod
        def splitter(nodestatus):
            """
            Splits node:status string given by client into node and status.
            """
            splits = nodestatus.split(':', 1)
            return (splits[0], splits[1])

        def __call__(self, parser, namespace, values, option_string=None):

            newvalues = None
            # TODO: verify this can be expected to work for all possible nargs
            if self.nargs is None:
                newvalues = self.splitter(values)
            else:
                newvalues = [
                    self.splitter(nodestatus) for nodestatus in values
                ]

            setattr(namespace, self.dest, newvalues)

    class NodeMaybeStatusSplitAction(NodeStatusSplitAction):
        """
        Action for splitting `node[:status]` parameters into node and status,
        and status part is optional.
        """

        @staticmethod
        def splitter(nodestatus):
            splits = nodestatus.split(':', 1)
            return (splits[0], splits[1] if len(splits) > 1 else None)

    class TimeIntervalValidation(argparse.Action):
        """ Validate a time interval is like 10m, 2h, 12d.
        """

        # regex for shorthand time intervals
        re_grok_interval = re.compile(r'^(\d+)([mhd])$')

        def __call__(self, parser, namespace, values, option_string=None):
            # pylint: disable=invalid-name
            m = TimeIntervalValidation.re_grok_interval.match(values)
            if not m:
                # pylint: disable=anomalous-backslash-in-string
                raise ValueError("Interval should be expressed as r'\d+[mhd]' such as 10m, 2h, 14d")

            # TODO: super() returns a blank?
            # `.__call__() not defined` (is the whole message)
            #super().__call__(parser, namespace, values)
            setattr(namespace, self.dest, values)

    conf = common()
    conf.config_argparser(conf.argparser)
    parsers = conf.argparser.add_subparsers(
        help='CLI command help', dest='cmd', required=True
    )

    # get command
    get_parser = parsers.add_parser('get', help='Get node status')
    get_parser.add_argument('nodestatus', type=str, nargs='*',
        help='nodes and/or node-status pairs to retrieve',
        metavar='node[:status]',
        action=NodeMaybeStatusSplitAction)

    # delete command
    delete_parser = parsers.add_parser('delete', aliases=['del'],
        help='Delete node or status')
    delete_parser.add_argument('nodestatus', type=str, nargs='+',
        help='nodes and/or node-status pairs to delete',
        metavar='node[:status]',
        action=NodeMaybeStatusSplitAction)

    # acknowledge command
    ack_parser = parsers.add_parser('acknowledge', aliases=['ack'],
        help='Acknowledge node status')
    ack_parser.add_argument('-x', '--expire-after', type=str,
        help="interval in r'\\d+[mhd]' format (ex. 26m, 3h, 2d)",
        action=TimeIntervalValidation)
    ack_parser.add_argument('-s', '--state', type=str,
        help='State to acknowledge')
    ack_parser.add_argument('nodestatus', type=str,
        help='Node and status to acknowledge', metavar='node:status',
        action=NodeStatusSplitAction)
    ack_parser.add_argument('message', type=str,
        help='Acknowledgement message', nargs='?')

    return conf
