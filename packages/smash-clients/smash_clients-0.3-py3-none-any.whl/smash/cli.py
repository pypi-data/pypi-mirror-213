# pylint: disable=too-many-branches
#   This is fine.
#
"""
Smash command-line interface client.
"""
import json
from smash import config
from smash import smash


def json_result(result):
    """ Print result as JSON. """
    print(result)


def json_error(errmsg):
    """ Print error as JSON. """
    print(f'"error":"{errmsg}"')


def print_result(result):
    """ Print result as text. """
    print(json.dumps(result, indent=2))


def print_error(errmsg):
    """ Print error as text. """
    print(f"Error: {errmsg}")


def main():
    """ Main client routine. """

    # load configuration
    # pylint: disable=invalid-name,broad-except
    try:
        conf = config.cli()
        args = conf.argparser.parse_args()
        conf.merge()
    except Exception as e:
        print(f"Could not load Smash configuration: {e}")
        return

    api = smash.ApiHandler(conf)

    # for collecting output and result
    output = None

    # DO put this next section in a try..except thingy (maybe)
    # the idea being to capture any exceptions and output them appropriately

    # handle command
    if args.cmd == 'get':

        output = []
        if args.nodestatus:
            for ns in args.nodestatus:
                if ns[1]:
                    output.append(api.get_node_status(ns[0], ns[1]))
                else:
                    output.append(api.get_node(ns[0]))
        else:
            output.append(api.get_all_status())

# Delete operation not yet supported--requires authentication
#    elif args.cmd in ['del', 'delete']:
#
#        output = []
#        for ns in args.nodestatus:
#            if ns[1]:
#                output.append(api.delete_node_status(ns[0], ns[1]))
#            else:
#                output.append(api.delete_node(ns[0]))

    elif args.cmd in ['ack', 'acknowledge']:
        output = api.acknowledge(args.nodestatus[0], args.nodestatus[1],
            args.message, args.state, args.expire_after)

    else:
        print_error(f"Not recognized: command {args.cmd}")

    # handle output
    if not output:
        if args.json:
            json_error(f"{args.cmd} unsuccessful")
        else:
            print_error(f"{args.cmd} unsuccessful")
    else:
        if args.json:
            json_result(output)
        else:
            print_result(output)


# if this module was called directly
if __name__ == '__main__':
    main()
