def createEvent(content, timestamp, type):
    eg = EventCreationTool.EventFactory(path_to_keys=str(Python.getPlatform().getApplication().getFilesDir()), path_to_keys_relative=False)
    if type == n:
        event = eg.next_event('KotlinUI/post', {'username' : "Bob", 'publickey' : eg.get_feed_id(),
                                            'timestamp' : 1, 'text' : "HELOOOO"})