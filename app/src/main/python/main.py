from six.moves import input


def main():
    print("Enter your name, or an empty line to exit.")
    while True:
        try:
            name = input()
        except EOFError:
            break
        if not name:
            break
        print("Hello {}!".format(name))
