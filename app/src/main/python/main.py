from six.moves import input
from crypto import create_keys, ED25519
import feed
import sys
from com.chaquo.python import Python
from os.path import join
import os
import re
import pcap
import ECT_FCTRL_DB.eventCreationTool.EventCreationTool as ect

import ECT_FCTRL_DB.logStore.appconn.kotlin_connection as kotlin

#from eventCreator import EventCreationToolTests

import viktor


LIST_PUBLIC_KEYS = "list pks"
DELETE_PUBLIC_KEYS = "del pks"
GET_USERNAME = "gu"
LS = "ls"
    
options = [LIST_PUBLIC_KEYS, GET_USERNAME, DELETE_PUBLIC_KEYS, LS]

FILES_DIR = str(Python.getPlatform().getApplication().getFilesDir())

SECRET_ABSOLUTE_PATH = join(FILES_DIR, "secret")
#MY_FEED_ABSOLUTE_PATH = join(FILES_DIR, "my_feed.pcap")
#VIKTOR_DB_ABSOLUTE_PATH = join(FILES_DIR, "stData")


def list_directories():
	for root, dirs, files in os.walk(FILES_DIR):
		for filename in files:
			print(filename)

def delete_pks():
	p = re.compile("[a-zA-Z0-9]+\.key")
	for root, dirs, files in os.walk(FILES_DIR):
		for filename in files:
			m = p.match(filename)
			if m:
				print("deleteing: {}".format(filename))
				path = join(FILES_DIR, filename)
				os.remove(path)

def list_pks():
	p = re.compile("[a-zA-Z0-9]+\.key")
	for root, dirs, files in os.walk(FILES_DIR):
		for filename in files:
			m = p.match(filename)
			if m:
				print(filename)


def get_pk():
	p = re.compile("[a-zA-Z0-9]+\.key")
	for root, dirs, files in os.walk(FILES_DIR):
		for filename in files:
			m = p.match(filename)
			if m:
				return filename[:-4]

def get_uname():
	path = str(Python.getPlatform().getApplication().getFilesDir())
	public_key = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)
	if not public_key:
		return "NOT FOUND - PUBLIC KEY ARRAY EMPTY"
	else: public_key = public_key[0]

	db = kotlin.KotlinFunction()

	list = db.get_usernames_and_feed_id()
	print(len(list))
	for tuple in list:
			#print("comparing {} to {}".format(str(tuple[1]), str(public_key)))
			#print(str(tuple[1]))
			if str(tuple[1]) == str(public_key):
				uname = str(tuple[0])
				return uname
	return "NOT FOUND - USER NOT IN DB"



def main():

	try:
		while True:
			print("Avaliable commands: {}".format(options))
			action = input()
			if action not in options:
				print("Invalid command, try again")
			if action == LIST_PUBLIC_KEYS:
				list_pks()
			if action == DELETE_PUBLIC_KEYS:
				delete_pks()
			if action == LS:
				list_directories()
			if action == GET_USERNAME:
				u = get_uname()
				print(u)

	except Exception as e:
		# print the exception and the line number at where it happened
		#https://stackoverflow.com/questions/14519177/python-exception-handling-line-number/20264059
		print("ERROR IN main")
		_, _, tb = sys.exc_info()
		print(e)
		print("At line number {}".format(tb.tb_lineno))
