# SMASH client

Local Python clients for Smash.  And maybe a library you can use with them or
something, idk.

## SMASH xbar

The SMASH xbar client works with [xbar](https://xbarapp.com/) to provide
current information on node and service status in your Mac menu bar.

## SMASH CLI client

The CLI client provides a command-line interface to the Smash API.

```
smash register node	# wait isn't this done by the agent?  Did I mean
			# something else?  Otherwise what's the use case for
			# providing this functionality here?
smash get node[:status]
smash delete node[:status] [ node[:status] ... ]   ### NOT IMPLEMENTED sorry
smash ack[nowledge] node:status [-x expires when] message
```
