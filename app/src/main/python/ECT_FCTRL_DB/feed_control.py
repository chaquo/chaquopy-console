from ECT_FCTRL_DB.feedCtrl.uiFunctionsHandler import UiFunctionHandler
#from ECT_FCTRL_DB.feedCtrl.uiFunctionsHandler import generate_test_data  # noqa: F401
##WE COMMENTED
##from ECT_FCTRL_DB.feedCtrl import ui
#from ECT_FCTRL_DB.logStore.verific.verify_insertion import Verification  # noqa: F401
#from ECT_FCTRL_DB.logStore.funcs.EventCreationTool import EventFactory  # noqa: F401
#from ECT_FCTRL_DB.logStore.appconn.feed_ctrl_connection import FeedCtrlConnection  # noqa: F401
import secrets
from nacl.signing import SigningKey
from ECT_FCTRL_DB.logStore.funcs.log import create_logger
import sys

logger = create_logger('test_feed_ctrl_connection')


class bcolors:
    TRUSTED = '\033[32m'
    BLOCKED = '\033[91m'
    ENDC = '\033[0m'


def split_inp(inp):
    _inp = inp.split(" ")
    return _inp

#WE ADDED PARAMETER
def cli(inp):

    # CLI test
    ufh = UiFunctionHandler()

    commandList = "\n-p: print List \n-t i j: Trust. i equals master index, j equals child index \n-ut i j: Untrust. " \
                  "i equals master index, j equals child index \n-r (int): without argument prints current radius, " \
                  "with argument sets new radius\n-n : prints the current username \n-n name: changes the username " \
                  "\n-reload: reload from database \n-q: quit"
    trusted = set(ufh.get_trusted())
    blocked = set(ufh.get_blocked())
    hostID = ufh.get_host_master_id()
    masterIDs = ufh.get_master_ids()
    #print("printing masterIDs")
    #print(masterIDs)
    radius = ufh.get_radius()

    print("Welcome to the Feed Control Demo! \n")


    #WE COMMENTED!
    #inp = input()
    sinp = split_inp(inp)
    cmd = sinp[0]
    args = sinp[1:]


    #(masterindex, username, feed_id_index, feedid, trusted?) per user in DB
    if cmd == '-p':
        list = []
        print("Host: " + ufh.get_username(hostID))
        if masterIDs is not None:
            i = 0
            for masterID in masterIDs:
                i = i + 1
                print('%d. ' % i + ufh.get_username(masterID))
                feedIDs = ufh.get_all_master_ids_feed_ids(masterID)
                j = 0
                for feedID in feedIDs:
                    j = j + 1
                    appName = ufh.get_application(feedID)
                    #print("printing appname!!")
                    #print(appName)
                    if appName != 'KotlinUI': # WE ADDED
                        continue
                    if feedID in trusted:
                        print("  %d. " % j + bcolors.TRUSTED + appName + bcolors.ENDC)
                        list.append((str(i), ufh.get_username(masterID), str(j), str(feedID), "1")) # WE ADDED
                    elif feedID in blocked:
                        print("  %d. " % j + bcolors.BLOCKED + appName + bcolors.ENDC)
                        list.append((str(i), ufh.get_username(masterID), str(j), str(feedID), "0")) # WE ADDED
                    else:
                        print("  %d. " % j + appName)
                        list.append((str(i), ufh.get_username(masterID),str(j), str(feedID), "0")) # WE ADDED
        #print("printing list")
        #print(list)
        return list

    elif cmd == '-t':
        masterID = masterIDs[int(args[0]) - 1]
        feed_id = masterID
        if int(args[1]) > 0:
                feed_id = ufh.get_all_master_ids_feed_ids(masterID)[int(args[1]) - 1]
        if feed_id not in trusted:
            ufh.set_trusted(feed_id, True)
            trusted.add(feed_id)

    elif cmd == '-ut':
        masterID = masterIDs[int(args[0]) - 1]
        feed_id = masterID
        if int(args[1]) > 0:
            feed_id = ufh.get_all_master_ids_feed_ids(masterID)[int(args[1]) - 1]
        ufh.set_trusted(feed_id, False)
        if feed_id in trusted:
            trusted.discard(feed_id)
            blocked.add(feed_id)

    elif cmd == '-r':
        if not args:
            print('Radius: %d' % radius)
        else:
            radius = int(args[0])
            ufh.set_radius(radius)

    elif cmd == '-n':
        if not args:
            print(ufh.get_username(hostID))
        else:
            ufh.set_username(args[0])

    elif cmd == '-reload':
        trusted = set(ufh.get_trusted())
        blocked = set(ufh.get_blocked())
        masterIDs = ufh.get_master_ids()
        radius = ufh.get_radius()

    elif cmd == '-q':
        running = False

    else:
        print(commandList)


def generate_random_feed_id():
    private_key = secrets.token_bytes(32)
    signing_key = SigningKey(private_key)
    public_key_feed_id = signing_key.verify_key.encode()
    return public_key_feed_id


if __name__ == '__main__':
    #generate_test_data()
    print("arg: " + sys.argv[1])
    if sys.argv[1] == 'cli':
        cli()
    #WE COMMENTED
    #elif sys.argv[1] == 'ui':
    #    ui.run()

