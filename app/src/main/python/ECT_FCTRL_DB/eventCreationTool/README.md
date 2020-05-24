# EventCreationTool

This is a simple tool for creating BACnet feeds and events.
Current version is 1.5

## Content

* [Requirements and installation](#requirements-and-installation)
* [Supported signing and hashing algorithms](#supported-signing-and-hashing-algorithms)
* [Quick start guide](#quick-start-guide)
  - [Additional important information](#additional-important-information)
* [Full API specification](#full-api-specification)
  - [Private key file format](#private-key-file-format)
  - [exception HashingAlgorithmNotFoundException](#exception-hashingalgorithmnotfoundexception)
  - [exception SigningAlgorithmNotFoundException](#exception-signingalgorithmnotfoundexception)
  - [exception KeyFileNotFoundException](#exception-keyfilenotfoundexception)
  - [exception IllegalArgumentTypeException](#exception-illegalargumenttypeexception)
  - [class EventFactory](#class-eventfactory)
  - [class EventCreationTool](#class-eventcreationtool)
* [Changelog](#changelog)

## Requirements and installation
In order to use the tool, you have to install the following python packages:
* PyNaCl
* cbor2

We recommend to install them using pip:
```
> pip install cbor2
> pip install pynacl
```

The tool provides the two python classes `PythonCreationTool` and `EventFactory` which you can use as API. 
To use the tool you need the two  python files `PythonCreationTool.py` and `Event.py`. Copy them over to your 
project (you could drop them in a separate folder) in order to use the tool.

We are thinking about creating a `pip install` package, but are currently busy. As for now, you can install the 
dependencies by running `pip install path/to/eventCreationTool` (or simply `pip install .` if your command line 
is inside the `eventCreationTool` folder). 

## Supported signing and hashing algorithms
Currently we support the following signing algorithms:
* ed25519
* hmac_sha256

And the following hashing algorithms:
* sha256

Feel free to contact us if you need different ones!

## Quick start guide 
Once you installed the tool, you probably want to start off by creating a new feed. The simplest way to do so is by 
creating a new object of the class `EventFactory`:
```python
import EventCreationTool
ecf = EventCreationTool.EventFactory()
```
This will create a new feed. If you want to create multiple feeds, you can simply create multiple `EventFactory` 
objects. You can now create events on that feed by using the `next_event()` method  and 
passing your custom content as follows:
```python
new_event = ecf.next_event(content_identifier, content_parameter)
```
When using this, please stick to the conventions for BACnet 
([here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md)). 
Thus `content_identifier` should be a string like `'yourapp/yourcommand'` and `content_parameter` could 
be whatever you want (but using dictionaries is probably most convenient). 
Our tool does not, however, enforce the convention. 

If you restart your application and need the factory for the same feed again, you can simply obtain the last event 
from your database and pass that event when creating the factory object like this:
```python
last_event =  # Obtain the last event of the feed you want to append to from the database
ecf = EventCreationTool.EventFactory(last_event)
```
Make sure that the event you pass is really the most recent one. Otherwise the event chain of your feed will diversify.

If you need the feed ids of the feeds you have the private key for, you can obtain them by using the following static 
method:
```python
list_of_feed_ids = EventCreationTool.EventCreationTool.get_stored_feed_ids()
```
You will get a `list` of `bytes`, which are the feed ids so you can obtain an event from the database and therewith 
reinitialize the `EventFactory`ies (as stated above).

#### Additional important information

The call `EventCreationTool.EventFactory()` will automatically create a `.key` file in your current working 
directory (i.e. the directory from which you ran the program that called the EventCreationTool). You can also 
specify another location to store your keys, as specified in the full API specification.

These files contain the private keys to your feeds. MAKE SURE TO NOT LOOSE THEM! If you loose these files, you will 
not be able to create new events (and our tool will throw some custom exceptions as specified 
[below](#full-api-specification))

The tools provides even more functionality as specified in the next section. There you will learn how to set custom 
private key paths, obtain private keys (you need them if you use hmac signing) or even set different signing 
and hashing algorithms.
Also, if you need a tool that allows more control, you could use the `EventCreationTool` class instead of 
`EventFactory`. API is specified below.

## Full API specification
#### Private key file format
Whenever a feed is created, a private key is generated. This key is binary saved in a file.
The naming convention we use is: `feed_id.key` (please note that the feed id and public key is the same thing.)
The file will be generated by default in the current working directory but the path can be adjusted as specified below.

#### exception HashingAlgorithmNotFoundException
This exception is thrown whenever you try to use a hashing algorithm that is not known to your used version of the tool.

#### exception SigningAlgorithmNotFoundException
This exception is thrown whenever you try to use a signing algorithm that is not known to your used version of the tool.

#### exception KeyFileNotFoundException
This exception is thrown whenever the tool needs access to a private key but this key is not available at the provided 
path. (For example thrown if you try to append to a feed that is not yours and you thus have not the private key.)

#### exception IllegalArgumentTypeException
This exception is thrown when you pass an argument which is of the wrong type. The exception message sometimes provides 
a list of accepted types, but you do best if you stick to the API below.

#### exception FirstEventWasNotCreatedException
This exception is thrown when you try to use the EventFactory to yield a `next_event` without creating a first event 
using the `first_event()` method first. This is used only in the highly abstract EventFactory class, as the 
EventCreationTool class is intended for the more advanced user which we do not protect from himself.

#### exception FirstEventWasAlreadyCreatedException
This exception is thrown when you try to create a first event using the `first_event` function, but a first event was 
already created. This is used only in the highly abstract EventFactory class, as the EventCreationTool class is 
intended for the more advanced user which we do not protect from himself.

#### class EventFactory
The class EventFactory is the recommended API of this tool.

```python
__init__(last_event=None, path_to_keys=None, path_to_keys_relative=True,
             signing_algorithm='ed25519', hashing_algorithm='sha256')
```
* Returns: A new object of the class.
* Throws: `SigningAlgorithmNotFoundException`, `HashingAlgorithmNotFoundException`
* Parameters:
  - optional `last_event`: Type: `bytes` (cbor encoded as you can get it from the database).
  Event on which base the object is created. Sets up the created factory to yield following events. If this is not 
  specified, a new feed will be created.
  - optional `path_to_keys`: Type: `str`. If you need a specific path to private keys. Can be a relative or absolute 
  path (See following parameter). Default is the current working directory.
  - optional `path_to_keys_relative`: Type: `bool`. Must be set to `False` if the above specified path was an absolute 
  path.
  - optional `signing_algorithm`: Type: `str`. The signing algorithm you want to use. Refer to 
  [here](#supported-signing-and-hashing-algorithms) for supported algorithms.
  - optional `hashing_algorithm`: Type: `str`. The hashing algorithm you want to use.
* NOTE: After creating a new feed (creating EventFactory object not using `last_event` parameter), you will have to 
immediately create a first event using the `first_event()` method and add it to the database. See also in the quick 
start guide.
* NOTE2: `signing_algorithm` and `hashing_algorithm` will be ignored if you specify a `last_event`. In this case, the 
algorithms will be chosen to match the previous events of the feed. This is to protect you from misusing a feed.

```python
get_feed_id()
```
* Returns: Type: `bytes`. The feed id (i.e. the public key) of the associated feed.

```python
get_private_key()
```
* Returns: Type: `bytes`. The private key of the associated feed. If you need to obtain the key for a partner when using 
the `hmac` signing algorithms.
* Throws: `KeyFileNotFoundException`

```python
first_event(app_name, master_feed_id)
```
* Returns: Type: `bytes` (cbor format). The first event of the associated feed  with the correct master feed 
 reference as specified in the parameters.
* Throws: `KeyFileNotFoundException`, `IllegalArgumentTypeException`
* Parameters:
  - `app_name`: Type: `str`. The identifier of your application. Please use this same identifier as first part of your 
   event identifier when using the `create_event` methods. Please stick to the conventions 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md). Looks 
  somehow like this: `appname/command` **wherefrom only `appname` should be passed!**
  - `master_feed_id`: Type: `bytes`. The feed of your local master feed id. Please refer to the documentation of Group 7 
  logStore on how to obtain it and also on Group 14 feedCtrl on what it is for.

```python
next_event(content_identifier, content_parameter=None)
```
* Returns: Type: `bytes` (cbor encoded). The new event that is generated together with your content. 
* Throws: `KeyFileNotFoundException` (If you try to append to a feed and do not have the private key at the specified 
location), `FirstEventWasNotCreatedException` (If you try to create a next event without creating a first event using 
the `first_event()` method first.)
* Parameters:
  - `content_identifier`: Type: `str`. The identifier of the content you append. Please stick to the conventions 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md). Looks 
  somehow like this: `appname/command`
  - optional `content_parameter`: Type: whatever. The content you want to save. Could be whatever but dictionary is 
  probably most convenient. A event without this parameter(s) is also valid. Also look 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md)

#### class EventCreationTool
If you need some more control, you can use this class instead of `EventFactory`.
Using this class you do not need a separate object for each feed. It is however recommended to use separate objects 
for different hashing and signing algorithms (so you don't have to set the algorithm each time). Here comes the API:

```python
@classmethod
get_stored_feed_ids(directory_path=None, relative=True, as_strings=False)
```
This is the only static method.
* Returns: Type: `list` of `bytes` or `str`. The list of those feed ids (i.e. public keys), for which the private key 
is present at the (specified) keys directory and thus the feeds on which ownership can be claimed and new events can 
be appended.
* Parameters:
  - optional `directory_path`: Type: `str`. The path to the private keys. Default is the current working directory, 
  i.e. the root directory from which the program that called the tool run. Could be an absolute or relative path.
  - optional `relative`: Type: `bool`. Specifies whether the path passed to the previous argument is a relative or 
  absolute path. Must be set to False if an absolute path is passed.
  - optional `as_strings`: Type: `bool`. If set to true, a `list` of `str` is returned instead of a `list` of `bytes`. 
  If so, the `str` values are the hexadecimal representations of the `bytes` typed private keys.

```python
set_path_to_keys(directory_path, relative=True)
```
* Parameters:
  - `directory_path`: Type: `str`. Set the path at which the private keys can be found. (The default at declaration 
  is the current working directory.) Can be absolute or relative to the current working directory.
  - optional `relative`: Type: `bool`. Must be set to `False` if the previous parameter was an absolute path.

```python
get_own_feed_ids(as_strings=False)
```
* Returns: Type: `list` of `bytes` or `str`. Returns all feed ids of which the private keys are stored at the currently 
set path to keys (This is the feed ids that belong to the user).
* Parameter:
  - optional `as_strings`: Type: `bool`. When set to `True` the method will return a `list` of `str`. Else or if 
  not provided it will return a `list` of `bytes`.
 
```python
set_hashing_algorithm(hashing_algorithm)
```
* Throws: `HashingAlgorithmNotFoundException` if the supplied algorithm is not supported.
* Parameter:
  - `hashing_algorithm`: Type: `str`. One of the supported hashing algorithms (see 
  [here](#supported-signing-and-hashing-algorithms)). This algorithm will be used to hash whenever events are created 
  with the associated EventCreationTool object.
  
```python
set_signing_algorithm(signing_algorithm)
```
* Throws: `SigningAlgorithmNotFoundException` if the supplied algorithm is not supported.
* Parameter:
  - `signing_algorithm`: Type: `str`. One of the supported signing algorithms (see 
  [here](#supported-signing-and-hashing-algorithms)). This algorithm will be used to sign whenever events are created 
  with the associated EventCreationTool object.  

```python
get_supported_hashing_algorithms()
```
* Returns: Type: `list` of `str`. A list of the names of the supported hashing algorithms.

```python
get_supported_signing_algorithms()
```
* Returns: Type: `list` of `str`. A list of the names of the supported signing algorithms.

```python
generate_feed_and_create_first_event(app_name, master_feed_id)
```
* Returns: Type: `bytes` (cbor format). The first event of a newly generated feed with the correct master feed 
 reference as specified in the parameters.
* Throws: `SigningAlgorithmNotFoundException`, `IllegalArgumentTypeException`
* Parameters:
  - `app_name`: Type: `str`. The identifier of your application. Please use this same identifier as first part of your 
   event identifier when using the `create_event` methods. Please stick to the conventions 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md). Looks 
  somehow like this: `appname/command` **wherefrom only `appname` should be passed!**
  - `master_feed_id`: Type: `bytes`. The feed of your local master feed id. Please refer to the documentation of Group 7 
  logStore on how to obtain it and also on Group 14 feedCtrl on what it is for.

```python
generate_feed()
```
* Returns: Type: `bytes`. The feed id (i.e. the public key as this is the same) of the newly generated feed.
* Throws: `SigningAlgorithmNotFoundException`

```python
create_first_event(feed_id, app_name, master_feed_id)
```
* Returns: Type: `bytes` (cbor format). The first event of the associated feed  with the correct master feed 
 reference as specified in the parameters.
* Throws: `KeyFileNotFoundException`, `IllegalArgumentTypeException`
* Parameters:
  - `feed_id`: Type: `bytes` or `str`. The feed id and thus public key of the feed we want to append to. The 
  private key must obviously be in the keys path, else a custom exception is thrown.
  - `app_name`: Type: `str`. The identifier of your application. Please use this same identifier as first part of your 
   event identifier when using the `create_event` methods. Please stick to the conventions 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md). Looks 
  somehow like this: `appname/command` **wherefrom only `appname` should be passed!**
  - `master_feed_id`: Type: `bytes`. The feed of your local master feed id. Please refer to the documentation of Group 7 
  logStore on how to obtain it and also on Group 14 feedCtrl on what it is for.

```python
create_event(feed_id, last_sequence_number, hash_of_previous_meta, content_identifier, content_parameter)
```
This method should not be used to create the first event of a feed. Please refer to `create_first_event()` instead.
* Returns: Type: `bytes` (cbor format). The event of the associated feed with content as specified in the parameters.
* Throws: `KeyFileNotFoundException`, `IllegalArgumentTypeException`
* Parameters:
  - `feed_id`: Type: `bytes` or `str`. The feed id and thus public key of the feed we want to append to. The 
  private key must obviously be in the keys path, else a custom exception is thrown.
  - `last_sequence_number`: Type: `int`. The sequence number of the most recent event of that feed. The sequence 
  number of this event will be set to this number plus one.
  - `hash_of_previous_meta`: Type: `list` with two elements: `int` (first) and `bytes`. The second one is the 
  hash value for the cbor encoded meta header of the previous event, the first being an indicator for which 
  hashing algorithm was used to calculate that hash. Please refer to 
  [this](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md) convention for more 
  information.
  - `content_identifier`: Type: `str`. The identifier of the content you append. Please stick to the conventions 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md). Looks 
  somehow like this: `appname/command`
  - `content_parameter`: Type: whatever. The content you want to save. Could be whatever but dictionary is 
  probably most convenient. A event without this parameter(s) is also valid. Also look 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md)

```python
create_event(previous_event, content_identifier, content_parameter)
```
This is the more convenient variant of the previous `create_event()` method, as you do not need to mine the 
information about the feed and events, but you can simply pass the last event and the tool will do the magic for you. 
This method should not be used to create the first event of a feed. Please refer to `create_first_event()` instead. 
* Returns: Type: `bytes` (cbor format). The event of the associated feed with content as specified in the parameters.
* Throws: `KeyFileNotFoundException`
* Parameters:
  - `previous_event`: Type: `bytes` (encoded as cbor). The most recent event of the feed we want to append. The 
  returned event will be chained after this event.
  - `content_identifier`: Type: `str`. The identifier of the content you append. Please stick to the conventions 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md). Looks 
  somehow like this: `appname/command`
  - `content_parameter`: Type: whatever. The content you want to save. Could be whatever but dictionary is 
  probably most convenient. A event without this parameter(s) is also valid. Also look 
  [here at the bottom](https://github.com/cn-uofbasel/BACnet/blob/master/doc/BACnet-event-structure.md)

```python
get_private_key_from_feed_id(feed_id)
```
The private key should remain a secret. This method is just visible, because you may need to share the key if you are 
using hmac signing. If you are not: You are better off not using this method.
* Returns: Type: `bytes`. The private key of the specified feed.
* Throws: `KeyFileNotFoundException` if the private key was not found in the keys path.
* Parameter: 
  - `feed_id`: Type: `bytes` or `str`. The feed id and thus the public key of the feed we want the private key of. 
  (In hexadecimal representation when passed as string)

```python
get_private_key_from_event(event)
```
The private key should remain a secret. This method is just visible, because you may need to share the key if you are 
using hmac signing. If you are not: You are better off not using this method.
* Returns: Type: `bytes`. The private key of the associated feed.
* Throws: `KeyFileNotFoundException` if the private key was not found in the keys path.
* Parameter: 
  - `event`: Type: `bytes` (cbor encoded). A event from the feed we want the private key for. The feed id and thus the 
  public key is thereof obtained and used to find the corresponding private key.

## Changelog
* V1.0: First release for extern use. API as specified [above](#full-api-specification).
* V1.1: Added EventFactory class for even simpler creation of events. Also some bugfixes and renaming.
* V1.2: Added possibility to obtain feed id from EventFactory. Added a static method to EventCreationTool that returns 
the feed ids of the own feeds (i.e. the ones we have private keys for). Also minor convenience changes. First version 
with complete README.md file.
* V1.3: Added setup.py for easier install using `pip install .`.
* V1.4: Added Tests for EventFactory class.
* V1.5: Changed the tool to create the first event according to Group 14 feedCtrl Feeds specifications.
