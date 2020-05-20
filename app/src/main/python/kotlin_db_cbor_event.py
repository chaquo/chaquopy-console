# not static
import database.appconn.kotlin_connection as kotlin
import eventCreator.EventCreationTool as ect
import eventCreator.Event as event
from com.chaquo.python import Python

#if application_action == 'post':
#    username = content[1]['username']
#    timestamp = content[1]['timestamp']
#    text = content[1]['text']
#    self.__sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no,
#                                                   application=application_action,
#                                                   username=username, oldusername='',
#                                                   timestamp=timestamp, text=text)
#

#timestamp=timestamp, text=text)
#
#elif application_action == 'username':
#username = content[1]['newUsername']
#oldusername = content[1]['oldUsername']
#
#timestamp = content[1]['timestamp']
#self.__sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no,
#application=application_action,
#username=username, oldusername=oldusername,
#timestamp=timestamp, text='')




def insert_cbor(type, username, timestamp, text, key_exists):
    """

    :param type:
    :param username:
    :param timestamp:
    :param text:
    :param key_exists:
    :return:
    """
    if key_exists == "true":
        key_exists = True
    else:
        key_exists = False

    path = str(Python.getPlatform().getApplication().getFilesDir())

    if not key_exists:
        eg = ect.EventFactory(path_to_keys=path, path_to_keys_relative=False)
        db = kotlin.KotlinFunction()
        # very first event where the user get assigned the name Anonymous
        first_event = eg.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": timestamp})
        db.insert_data(first_event)

    print("printing last kotlin event ....")
    print(db.get_last_kotlin_event())
    print("last event printed")

    eg = ect.EventFactory(last_event=db.get_last_kotlin_event(), path_to_keys= path, path_to_keys_relative= False)
    if type == "username":
        new_event = eg.next_event("KotlinUI/username", {"newUsername": username, "oldUsername": "Anonymous", "timestamp": timestamp})
    else:
        new_event = eg.next_event("KotlinUI/post", {"username": username, "timestamp": timestamp, "text": text})
    db.insert_data(new_event)

    print("it worked")
