# pylint:
#
"""
Smash client code.
"""
import requests

state_colours = {
    'okay': 'green',
    'unknown': 'gray',
    'warning': 'orange',
    'error': 'red',
    'unusable': 'black',
    'stale': 'brown',
    'acknowledged': 'blue'
}

state_icons = {
    'okay': '',
    'unknown': ':question:',
    'warning': ':grimacing:',
    'error': ':cry:',
    'unusable': ':dizzy_face:',
    'stale': ':bread:',
    'acknowledged': ':see_no_evil:'
}

state_totals = {
    'okay': 0,
    'unknown': 0,
    'warning': 0,
    'error': 0,
    'unusable': 0,
    'stale': 0,
    'acknowledged': 0,
    'all': 0
}


def overall_state(totals):
    """ Determines overall state of a set to be the worst occurring, given
    totals for each possible state in the set, and a short string summary.
    """
    summary_parts = []
    overall = None
    if totals['unusable'] > 0:
        summary_parts.append(f"{totals['unusable']}U")
        overall = 'unusable'
    if totals['error'] > 0:
        summary_parts.append(f"{totals['error']}E")
        overall = overall or 'error'
    if totals['warning'] > 0:
        summary_parts.append(f"{totals['warning']}w")
        overall = overall or 'warning'
    if totals['unknown'] > 0:
        summary_parts.append(f"{totals['unknown']}?")
        overall = overall or 'unknown'
    if totals['stale'] > 0:
        summary_parts.append(f"{totals['stale']}s")
        overall = overall or 'stale'
    if totals['acknowledged'] > 0:
        summary_parts.append(f"{totals['acknowledged']}a")
        overall = overall or 'acknowledged'
    if totals['okay'] > 0:
        overall = overall or 'okay'
    if summary_parts:
        summary = " ".join(summary_parts) + f" of {totals['all']}"
    else:
        summary = f"All {totals['all']} ok"
    return(overall, summary)

# TODO: Make this unit-testable, so given the JSON, interpret the objects
#   With whatever mechanism uses `yield()`, create function that takes the
#   URL and creates the node objects
# TODO: simplify with new /status/ API call
def load_nodes(api_url, timeout):
    """ Loads nodes from Smash server and their statuses.
    """
    nodes = requests.get(api_url + '/nodes/', timeout=timeout).json()
    for node in nodes:

        node['totals'] = {
            'okay': 0,
            'unknown': 0,
            'warning': 0,
            'error': 0,
            'unusable': 0,
            'stale': 0,
            'acknowledged': 0,
            'all': 0
        }

        # request status
        node['statuses'] = requests.get(
            f"{api_url}/nodes/{node['node']}/status/", timeout=timeout
        ).json()
        for status in node['statuses']:
            if 'acknowledgement' in status:
                state_totals['acknowledged'] += 1
                node['totals']['acknowledged'] += 1
            elif status['stale']:
                state_totals['stale'] += 1
                node['totals']['stale'] += 1
            else:
                state = status['state']
                state_totals[state] += 1
                node['totals'][state] += 1
            state_totals['all'] += 1
            node['totals']['all'] += 1
            status['message'] = status['message'].replace('\n','; ')

    return nodes


class ApiHandler:
    """
    ApiHandler class something something
    """

    def __init__(self, conf):
        self._api_url = conf['server'] + '/api'
        self._timeout = conf['request_timeout']

    def get_node(self, node):
        """
        Retrieve node information and status
        """
        # TODO: Not DRY along with load_nodes()

        obj = {
            'totals': {
                'okay': 0,
                'unknown': 0,
                'warning': 0,
                'error': 0,
                'unusable': 0,
                'stale': 0,
                'acknowledged': 0,
                'all': 0
            },
            'status': []
        }

        # request status
        statuses = requests.get(
            f"{self._api_url}/nodes/{node}/status/", timeout=self._timeout
        ).json()
        for status in statuses:
            if 'acknowledgement' in status:
                state_totals['acknowledged'] += 1
                obj['totals']['acknowledged'] += 1
            elif status['stale']:
                state_totals['stale'] += 1
                obj['totals']['stale'] += 1
            else:
                state = status['state']
                state_totals[state] += 1
                obj['totals'][state] += 1
            state_totals['all'] += 1
            obj['totals']['all'] += 1
            status['message'] = status['message'].replace('\n','; ')
            obj['status'].append(status)

        return obj

    def get_node_status(self, node, status):
        """
        Retrieve a particular status for a node.
        """

        # request status
        status = requests.get(
            f"{self._api_url}/nodes/{node}/status/{status}", timeout=self._timeout
        ).json()

        return status

    def get_all_status(self):
        """
        Retrieve all current status.
        """

        return requests.get(
            f"{self._api_url}/", timeout=self._timeout
        ).json()

    def acknowledge(self, node, status, message=None, state=None, expiry=None):
        """
        Acknowledge a particular status on a node.
        """

        result = requests.put(
            f"{self._api_url}/nodes/{node}/status/{status}/acknowledgement",
            timeout=self._timeout,
            data={
                'message': message,
                'state': state,
                'expiry': expiry
            }
        ).json()

        return result

    def delete_node(self, node):
        """
        Delete a node.
        """

        result = requests.delete(
            f"{self._api_url}/nodes/{node}",
            timeout=self._timeout
        ).json()

        return result

    def delete_node_status(self, node, status):
        """
        Delete the given status for the given node.
        """

        result = requests.delete(
            f"{self._api_url}/nodes/{node}/status/{status}",
            timeout=self._timeout
        ).json()

        return result
