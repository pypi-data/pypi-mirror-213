#!/usr/bin/env python3.8

#
# Purpose:
#
# Send metrics to graphite server.
# Works as module or command line tool
#

import os
import sys
from socket import *

import argparse
import re

#
# Constants
#

# Version (Mine, and PEP defactos)
VERSION=(0,0,1)
Version = __version__ = ".".join([ str(x) for x in VERSION ])

# Text Submit Port
TextPort = 2003
# UDP/Statsd Submit Port
StatsdPort = UDPPort = 8125

# Server RegExp
__FieldsExp__ = r"^(?P<server>[^\:]+)(\:(?P<port>[0-9]+)){1}$"

#
# Module Variables
#

# Graphite Server
GraphiteServer = None

# Graphite Root Label
GraphiteRoot = None

#
# Module Functions
#

def TextSend(metric_name,metric_value,root=None,timestamp=-1,server=None,silent=False):
	"""Text Send To Graphite"""

	global GraphiteServer, GraphiteRoot, TextPort

	success = True

	if server is None:
		# If not provided, use the module-global one
		server = GraphiteServer
	else:
		# If provided in various forms, make sure its in the correct format
		if type(server) is str:
			server = (server,TextPort)
		elif server[1] != TextPort:
			server = (server,TextPort)

	if root is None:
		root = GraphiteRoot

	if server is not None and server[1] == TextPort:
		try:
			packet = f"{root}.{metric_name} {metric_value} {timestamp}\n"

			with socket() as gs:
				gs.connect(server)
				gs.sendall(packet.encode("utf-8"))
		except Exception as err:
			success = False
			if not silent:
				print(f"gsubmit::TextSend failed because : {err}")
	else:
		success = False

	return success

def UDPSend(metric_name,metric_value,root=None,server=None,silent=False):
	"""Statsd UDP Send"""

	global GraphiteServer, GraphiteRoot, StatsdPort

	success = True

	if server is None:
		server = GraphiteServer
	else:
		# If provided in various forms, make sure its in the correct format
		if type(server) is str:
			server = (server,StatsdPort)
		elif server[1] != StatsdPort:
			server = (server,StatsdPort)

	if root is None:
		root = GraphiteRoot

	if server is not None and server[1] == StatsdPort:
		try:
			data = { f"{root}.{metric_name}" : metric_value }

			with socket(AF_INET,SOCK_DGRAM) as UDPSocket:
				UDPSocket.sendto(":".join(data).encode("utf-8"),server)
		except Exception as err:
			success = False
			if not silent:
				print(f"gsubmit::UDPSend failed because : {err}")
	else:
		success = False

	return success

#
# Main Loop
#

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Send Metrics to Graphite tool")

	parser.add_argument("server",help="Server to send to, in the form, server:port, if port is omitted, assumed to be 2003")
	parser.add_argument("root_label",help="Root label for metric in graphite")
	parser.add_argument("metric_name",help="Metric name/path")
	parser.add_argument("metric_value",help="Metric Value")
	parser.add_argument("-t","--timestamp",default=-1,required=False,help="Optional timestamp, in the form, YYYYMMDDHHmmss")

	args = parser.parse_args()

	server = args.server
	root = args.root_label
	metric_name = args.metric_name
	metric_value = args.metric_value
	timestamp = args.timestamp if args.timestamp is not None else -1

	match = re.search(__FieldsExp__,server)

	if match is not None:
		server = ( match.group("server"), int(match.group("port")) )
	else:
		server = ( server, TextPort )

	if server[1] == TextPort:
		TextSend(metric_name,metric_value,root=root,server=server,timestamp=timestamp)
	elif server[1] == StatsdPort:
		UDPSend(metric_name,metric_value,root=root,server=server)
	else:
		print(f"{server[1]} is an invalid port, either 2003 or 8125")
