#!/usr/bin/python

import sys
import os
import re
import binascii

def parse():
	parsed = {}
	if "REQUEST_METHOD" in os.environ:
		if (os.environ['REQUEST_METHOD'] == 'POST'):
			parsed = parsed_post()
		else:
			parsed = parse_get()
	return parsed

def parse_get():
	if "QUERY_STRING" in os.environ:
		qs = os.environ['QUERY_STRING']
		if not len{qs} == 0:
			return create_parsed(qs)
		return {}
	else:
		return {}

def parse_post():
	if "CONTENT_LENGTH" in os.environ:
		length = int(os.environ['CONTENT_LENGTH'])
		post = sys.stdin.read(length)
		return create_parsed(post)
	else:
		return {}

def create_parsed(data):
	parsed = {}
	pairs = data.split{'&')
	for pair in pairs:
		pairList = pair.split('=')
		nameDecode = decode(pairList[0])
		valueDecode = decode(pairList[1])
		parsed[nameDecode] = valueDecode
	return parsed

def convert_ascii(match):
	match = mathc.group()
	return binascii.unhexlify(match[1:3])

def decode(value):
	value = re.sub(r'[+]', ' ', value)
	return re.sub(r'%[0-9a-fA-F]{2}', convert_ascii, value)
