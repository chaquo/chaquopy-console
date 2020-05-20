from six.moves import input
from crypto import create_keys, ED25519
import feed
import sys
from com.chaquo.python import Python
from os.path import join
import os
import pcap

#from eventCreator import EventCreationToolTests

import viktor

    
CREATE_SECRET = "create_secret"
LS = "ls"
READ_SECRET = "read_secret"
DELETE_SECRET = "delete_secret"
DELETE_FEED = "delete_feed"
CREATE_FEED = "create_feed"
APPEND = "append"
DUMP = "dump"

options = [CREATE_SECRET, LS, READ_SECRET, DELETE_SECRET, CREATE_FEED, APPEND, DELETE_FEED, DUMP]

FILES_DIR = str(Python.getPlatform().getApplication().getFilesDir())

SECRET_ABSOLUTE_PATH = join(FILES_DIR, "secret")
MY_FEED_ABSOLUTE_PATH = join(FILES_DIR, "my_feed.pcap")
VIKTOR_DB_ABSOLUTE_PATH = join(FILES_DIR, "stData")

HELLO_WORLD_LOG = ["hello world!", 123, {"hello": "world", "this is a ": "dictionary"}]


class NON_ED25519_EXCEPTION(Exception):
	pass


def load_keyfile(fn):
	with open(fn, 'r') as f:
		key = eval(f.read())
	if key['type'] == 'ed25519':
		fid = bytes.fromhex(key['public'])
		signer = ED25519(bytes.fromhex(key['private']))
	else:
		print("Filetype not supported. Filthy hmac user")
		raise NON_ED25519_EXCEPTION
	return fid, signer


def dump():
	if not os.path.exists(MY_FEED_ABSOLUTE_PATH):
		print("no feed to dump!")
		print("try creating a feed first")
	else:
		s = pcap.dump(MY_FEED_ABSOLUTE_PATH)
		print(s)
		return s

def dumpList():
		if not os.path.exists(MY_FEED_ABSOLUTE_PATH):
			print("no feed to dump!")
			print("try creating a feed first")
		else:
			list = pcap.dump(MY_FEED_ABSOLUTE_PATH)
			print(list)
			return list


def append(log_to_be_appended):
	if not os.path.exists(MY_FEED_ABSOLUTE_PATH):
		print("no feed to append to!")
		print("try creating a feed first")
	else:
		fid, signer = load_keyfile(SECRET_ABSOLUTE_PATH)
		f = feed.FEED(MY_FEED_ABSOLUTE_PATH, fid, signer, create_if_notexisting=False)
		f.write(log_to_be_appended)
		print("append executed successfully!")


def create_feed():
	if not os.path.exists(SECRET_ABSOLUTE_PATH):
		print("secret file does not exist!")
		print("create an account first")
		return
	if os.path.exists(MY_FEED_ABSOLUTE_PATH):
		print("feed already exists!")
		print("try deleting it")
		return
	fid, signer = load_keyfile(SECRET_ABSOLUTE_PATH)
	print("Keys loaded successfully")
	f = feed.FEED(MY_FEED_ABSOLUTE_PATH, fid, signer, create_if_notexisting=True)
	print("Feed created successfully")
	f.write(HELLO_WORLD_LOG)
	print("Feed populated with a token example!")


def read_secret():
	if not os.path.exists(SECRET_ABSOLUTE_PATH):
		print("secret does not exist!")
		print("try creating an account first")
	else:
		file = open(SECRET_ABSOLUTE_PATH, "r")
		for line in file:
			print(line)
		file.close()

def list_directories():
	for root, dirs, files in os.walk(FILES_DIR):
		for filename in files:
			print(filename)

def delete_secret():
	if not os.path.exists(SECRET_ABSOLUTE_PATH):
		print("Secret does not exist!")
		print("nothing to delete ...")
	else:
		os.remove(SECRET_ABSOLUTE_PATH)
		print("secret file deleted successfully")


def delete_feed():
	if not os.path.exists(MY_FEED_ABSOLUTE_PATH):
		print("Feed does not exist!")
		print("nothing to delete ...")
	else:
		os.remove(MY_FEED_ABSOLUTE_PATH)
		print("Feed file deleted successfully")	


def create_secret(keypair):
	file = open(SECRET_ABSOLUTE_PATH, "w")
	file.write(keypair)
	file.close()


def test_db():
	connector = viktor.SqLiteConnector(name=VIKTOR_DB_ABSOLUTE_PATH)
	connector.start_database_connection()
	connector.create_table('chat')
	connector.insert_to_table('chat', '20:45', 'Peter', 'Hallo')
	connector.insert_to_table('chat', '20:46', 'Max', 'Hallo')
	connector.insert_to_table('chat', '20:47', 'Gustavo', 'Hallo')
	connector.commit_changes()
	connector.get_all_from_table('chat')
	rows = connector.cursor.fetchall()

	for row in rows:
		print(row)


def main():
	try:
		############### DB TEST##############
		#test_db() # comment me out
		#return # comment me out too
		#####################################


		print("Avaliable commands: {}".format(options))
		action = input()
		if action not in options:
			print("Invalid command, try again")

		if action == LS:
			#EventCreationToolTests.main()
			list_directories()

		if action == READ_SECRET:
			read_secret()

		if action == DELETE_SECRET:
			delete_secret()

		if action == DELETE_FEED:
			delete_feed()

		if action == CREATE_SECRET:
			keypair = create_keys()
			create_secret(keypair)

		if action == CREATE_FEED:
			create_feed()

		if action == APPEND:
			print("Enter log to be appended")
			log_to_be_appended = input()
			append(log_to_be_appended)

		if action == DUMP:
			dump()

		main()

	except Exception as e:
		# print the exception and the line number at where it happened
		#https://stackoverflow.com/questions/14519177/python-exception-handling-line-number/20264059
		print("ERROR IN main")
		_, _, tb = sys.exc_info()
		print(e)
		print("At line number {}".format(tb.tb_lineno))
