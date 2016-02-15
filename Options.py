# -*- coding: utf-8 -*-
#
# Copyright 2016 Vale Tolpegin
# Distributed under the terms of the MIT License.

# -- Modules ------------------------------------------------------------------

from optparse import OptionParser


# -- global options -----------------------------------------------------------

global __Options__


# -- getOption ===-------------------------------------------------------------

def getOption(string):
	"""
	Fetches an option by name
	"""

	return getattr(__Options__, string)


# -- splitCommaSeparatedList --------------------------------------------------

def setCommaSeparatedList(option, opt, value, parser):
	setattr(parser.values, option.dest, value.split(','))


# -- parseOptions -------------------------------------------------------------

def parseOptions():
	"""
	Does command line argument parsing
	"""
	parser = OptionParser(usage='usage: %prog [options] portname[-portversion]', version='0.0.1')
	parser.add_option('-d', '--directory', dest='directory', help="haikuports directory")

	global __Options__

	(__Options__, args) = parser.parse_args()

	return (__Options__, args)
