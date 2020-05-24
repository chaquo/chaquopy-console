# logStore-feedCtrl: logCtrl

logCtrl is a Python library to enable both application groups as well as the network layer groups to store, retrieve and filter the data they need to provide their respective services.

## Content

* [Installation](#installation)
* [Usage](#usage)
  - [Application layer](#application-layer)
    * [What we need to build you an interface](#what-we-need-to-build-an-interface-for-your-application-group)
    * [Example for requirements](#example-for-requirements)
    * [How to use it in code](#how-to-use-it-in-code)
  - [Network layer](#network-layer)
    * [Current status](#current-status)
    * [Goal](#goal)
* [Testing](#testing)
* [Contributors](#contributors)
* [Contributing](#contributing)
* [License](#license)
* [Contributing](#contributing)
* [Changelog](#changelog)

## Installation

Download the package 07-14-logCtrl from the [Github repository](https://github.com/cn-uofbasel/BACnet/tree/master/groups/07-14-logCtrl)

Unzip the package into any folder. 

## Usage

Usage of logCtrl can be split up in the usage for the application layer groups and the network layer groups. Important for usage is that the groups use the [EventCreationTool](https://github.com/cn-uofbasel/BACnet/tree/master/groups/04-logMerge/eventCreationTool) provided by group 04.

#### Application layer:

Most application layer groups have requested specific interfaces for their applications which have been subsequently implemented by us. If your applications needs another interface please don't hesitate to contact us.

If an application group would prefer to implement the functionality themselves they may access the same functionalities as the network layer groups to get and insert cbor events into the database. Those methods can be found in `groups/07-14-logCtrl/src/logStore/appconn/connection.py`.

Best practice for the demo would be to put ones own code and the code of the network layer group in directories on the same level as the directories tests, logStore and feedCtrl and start the application from a main function similar to `feed_control.py`.

It is also very important that the first event ever submitted by the application to the database contains the master feed. If a new feed is created for an app, the first event has to contain `appname/MASTER` and data as `{'master_feed': master_feed_id}`, the master feed id can be retrieved with `get_host_master_id` which is available to all application groups in their respective interface. Please also check beforehand with group 04 if their Event factory already does a similar thing.

##### How to use it in code:

The application group would then get a corresponding class where all those functions can be imported from. In this example we would call this class `chat_connection` and it could be used correspondingly:

```python
from logStore.appconn.chat_connection import ChatFunction as cf

chat_id = '21b1235u4'
ecf = EventFactory()
new_event = ecf.next_event('whateverapp/whateveraction', {'oneKey': 'somevalue', 'someotherkey': 1})
cf.insert_chat_msg(new_event)

cf.get_chat_since(application, timestamp, feed_id, chat_id)
cf.get_full_chat(application, feed_id, chat_id)
cf.get_last_event(feed_id)
```

For a detailed example either have a look at the tests or at `feed_control.py` which imports functionality of our code.

#### Requirements

Before you can start your Application for the first time you'll have to run the feed controller for at least ones!

``python feed_control.py cli`` for using the command-line interfae

``python feed_control.py ui`` for using the graphical interface 

Your own masterfeed will then be generated, without a masterfeed the database won't accept your data. 

Inside the feedcontroller you can then configure on who to trust and whom you won't. The list of feeds is generated from the masterfeeds from other user. So before you can start trusting other users you'll have to collect masterfeeds.

**Usage of the CLI:**

|cmd|parameter|return value|explanation|
|-------------|-----------------|---|-------|
|`-p`| |`list` of `feeds`|Prints a list of feeds with their corresponding index. For each masterfeed the childfeeds will be printed indented.|
|`-t`|`i` master index `j` child index| |Sets a given feed to trusted.|
|`-ut`|`i` master index `j` child index| |Sets a given feed to untrusted.|
|`-r`| |current radius|Prints the current radius on to the console.|
|`-r`|`radius` as integer| |Changes the current set radius to the new value.|
|`-n`| |current name|Prints the current username you have.|
|`-n`|`name`| |Changes your username to the new name.|
|`-reload`| | |If there were any changes to database on runtime you can load the new data with this command.|
|`-q`| | |Exit the program|

**Usage of the ui:**

The tree is a visualization of master feeds with their corresponding child feeds. The color code is as followed:

*The colorization of the nodes might not work on windows systems!*

|Color|Meaning|
|-----|-------|
|`White`|If the color is `white` no tag has yet been set to a feed. So it's neither trusted nor blocked, but it behaves as it is blocked|
|`Green`|A `green` feed is a trusted feed. This one will be accepted by feedCtrl
|`Red`|A `red` feed is a blocked feed. This one will be discarded by feedCtrl|
|`Yellow`|A `yellow` feed is a `MASTER` feed, those represent the User|

The `UpdateFeedIDs` button is used for updating the feed tree. If there were any changes to the database while the feedCtrl application was running just push this button.

With `Trust` or `Untrust` you can change the state of the currently selected feed.

With `Update Username` your Username will be changed to the currently set Name in the upper text box.

With `Update Radius` your Radius will be set to the currently set Radius in the upper text box.



#### Network layer:

##### Current status:
Currently both group 4 and 12 can access the database with the functions inside `logStore/transconn/database_connection` and currently consist of:

| function name | parameter | return value |
|-------------|-----------------|---|
| `add_event(event)`    | `event` type `bytes` | adding an event originally created by an `eventCreationTool` to the database |
| `get_current_seq_no(feed_id)`  | `feed_id` type `bytes` | returns the highest sequence number as `int` or -1 if no sequence number exists to this feed id | 
| `get_event(feed_id, seq_no)` | `feed_id` type `bytes`, `seq_no` type `int` | returns an event as `bytes` or None if no such event exists | 
| `get_current_event(feed_id)` | `feed_id` type `bytes` | returns an event as `bytes` or None if no such event exists | 
| `get_all_feed_ids()` | empty | returns a list of feed ids of type `bytes` | 
| `check_incoming(feed_id, app_name)` | `feed_id` type `bytes` `app_name` type `string` | returns whether an incoming feed id is trusted | 
| `check_outgoing(feed_id)` | `feed_id` type `bytes` | returns whether an outgoing feed id is trusted | 


The functionality can be used as described following:

DatabaseConnector:

```python
from logStore.transconn.database_connector import DatabaseConnector as dc

chat_id = '21b1235u4'

dc.add_event(event)

dc.get_current_seq_no(feed_id)
dc.get_event(feed_id, seq_no)
dc.get_current_event(feed_id)
dc.get_all_feed_ids()
```

Verification:

```python
from logStore.verific.verify_insertion import Verification

# If the feed is a master feed
ver = Verification()
ver.check_incoming(master_id, 'MASTER') # returns true

#If the feed is a child feed
ver.check_incoming(feed_id, 'ExampleApp1')
```
##### Verification:
The Idea for `check_incoming()` and `check_outgoing()` is to verify if we wan't to import or export a given feed to the database. It's recommended to run the test before importing a feed into the database, depending on the result a feed is accepted or not. Else a feed won't be validated and can be corrupted.

## Testing:
The module has been extensively tested by us and there are unit tests for most if not all functionalities. For use cases please have a look at the unit tests as those represent on how the code is intended to be used.

## Contributors:
Various parts of the code have been created by different people and different groups. As we wanted an early integration we have closely worked with other groups from the beginning.

* Group 04: Contributed by allowing us to use `/logStore/funcs/EventCreationTool.py` for testing and `/logStore/funcs/event.py` for event creation and for event decoding.
* Group 14: Contributed by creating `/logStore/verific/verify_insertion.py` and `/feedCtrl` and by working together with group 07 to integrate our two projects early on to allow for an easier usage for other groups.
* Group 07: Contributed by creating the rest of `/logStore` and by working together with group 14 to integrate our two projects early on to allow for an easier usage for other groups.

The two main contributors to this code have been [vGsteiger](https://github.com/vGsteiger) and [DKnuchel](https://github.com/DKnuchel), who are members of group 07 and group 14.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Changelog

* V1.0: Initial functionality implemented and proper readMe written.
* V2.0: The packages of group 7 and group 14 are now merged into one package.
