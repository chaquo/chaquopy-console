from six.moves import input
from crypto import create_keys, test_keys
import sys

CREATE = "create_keys"
TEST = "test_keys"

HMAC = "hmac"
ED = "ED25519"

options = [CREATE, TEST]
types = [HMAC, ED]

def main():
	try:
		run()
	except Exception as e:
		# print the exception and the line number at where it happened
		#https://stackoverflow.com/questions/14519177/python-exception-handling-line-number/20264059
		print("ERROR!!!!")
		_, _, tb = sys.exc_info()
		print(e)
		print("At line number {}".format(tb.tb_lineno))


def run():
	print("Avaliable commands: {}".format(options))

	action = input()

	if action not in options:
		print("Invalid command, try again")
		main()

	if action == "create_keys":
		print("Avaliable types: {}".format(types))
		type_ = input()
		if type_ not in types:
			print("Invalid type, try again")
			main()
		if type_ == HMAC:
			create_keys(hmac=True)
		else:
			create_keys(hmac=False)
		run()

	if action == "test_keys":
		print("Avaliable types: {}".format(types))
		type_ = input()
		if type_ not in types:
			print("Invalid type, try again")
			main()
		if type_ == HMAC:
			test_keys(hmac=True)
		else:
			test_keys(hmac=False)
		run()


#def main():
#    print("Enter your name, or an empty line to exit.")
#    while True:
#        try:
#            name = input()
#        except EOFError:
#            break
#        if not name:
#            break
#        print("Hello {}!".format(name))
