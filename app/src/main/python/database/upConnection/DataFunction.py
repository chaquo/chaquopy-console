from .Function import Function


class DataFunktion(Function):

    def insert_data(self, data):
        return False

    def set_data_structure(self, data_type):
        pass

    def retrieve_data_since(self, hash):
        pass

    def get_usernames_and_publickeys(self):
        return self.__handler.get_usernames_and_publickey()

    def get_all_entries_by_publickey(self, publicKey):
        return self.__handler.get_all_entries_by_publickey(publicKey)

    def get_all_kotlin_event(self):
        return self.__handler.get_all_kotlin_events()
