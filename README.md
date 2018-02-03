# SLRD [WORK IN PROGRESS]
> Early concept documentation. Nothing works just yet.
## General overview
### Description
SLRD is a project that aims to provide a convenient and secure way of storing
personal information, passwords and any other text secrets locally and remotely
under VCS.
### Planned features
* Encrypted key-value storage for text secrets
* Website-specific containers
* Strong accent on storing personal information such as full name, home
    address, phone number etc.
* Minimize risk of leaking any information connected to the values stored in
    the application
* Browser plugins that help user to fill in the data online (Firefox, Chrome)
* Online repository to store website-specific templates
* Pluggable UIs
* Plugins support
### Requirements (MVP)
* CRUD
* Support for multiple sites
* Support for multiple profiles for each site
* Provide a list of all sites where the user was registered and when (timeline)
* Store any textual key-value data. Support storing information not connected
    to any site/online resource (notes etc).
* Plugins?
## Architecture
Some random points:
* Index is kept in RAM only
* File containers has fixed size and random name and timestamp
* Split into multiple containers if container content > container size
* Using GPG/PGPMF for keys and encryption. Relying on GPG agent.
* Hardcap key content length to the container size
* User-defined templates for sites

### Template sketches
Template for online registration/login (websites etc):
```
name: Facebook registration template  |
type: online                          |
first_time_link: fb.com/register      |
link: fb.com/login                    |
keys:                                 |
    - first_name                      | => enforced and validated by backend
    - last_name                       |
    - email                           |
    - password                        |

- fronted_specific_content:           | => defined and handled by frontend
    - ...                             |
```

Template for handling plain text date:
```
name: Plain text content
type: plain
```

Frontend and other plugins should be able to create their own template types.

### Linkfile sketches
Linkfile created after user registered with template 1 from the previous
section:
```
id: <random_value>  # 32 random bytes from /dev/urandom
template: <template_name>  # value of a 'name' key in template file
keys:
    first_name: John
    last_name: Rodgerson
    email: johnjohn@mealforfree.de
    password: cookies_for_free_meal_for_free
created_on: dd.mm.yy hh:mm <Region>/<City>  # 02.02.2018 14:22 Africa/Accra
notes: My main FB profile
<
any_other_optional_keys: ...
>
```
### Keyfile sketches
Just a random example of keyfile for a `first_name` key
```
first_name:
    - John: [list of linkfile ids]
    - Dolori: [list of linkfile ids]
    - Bob: [...]
```
Keyfiles also are capable of storing shortcut information:
```
sites:
    - facebook.com: [...]
    - stackexchange.com: [...]
    - ...
```
### Store sketches
```
type: <plugin_name>.<type_defined_by_plugin>
....
(any KV data that can be exported to YAML)
```
### Modules etc
* Controllers - low level operations do not involving any business logic
    * `FSController`
    * `GitController`
    * `GPGController`
* Models - OOP definitions of objects to manipulate with
    * `Templates`
    * `Linkfiles`
    * `Keyfiles`
    * `Store`? - used to store data by plugins

## Random thoughts
### Plugin ideas
* Create new emails for user (actual emails with actual credentials)
* Store pictures
* Fetch templates from remote repository (resource)

### Things to consider
* Make sure all queries are as fast as it's possible
* Plugin system? Where to plug and what to plug
* Fake files, updates and commits masking

### Plugin interaction with core
* Core initialization
* Search and load plugins
* Poll plugins for supported types
* Index core models (templates, keyfiles and linkfiles)
* Index store model and group by type
* Feed supported types to respective plugins
* Allow plugins to write KV data to core index (as it's the only daemon)

> NOTE: core provides individual KV store for all plugins. By default all KV
> values of a particular plugin are kept private though plugin can export KV
> as public.

```
Plugin():
    # feed supported types to this plugin
    def on_init(core_ind):
        core_ind.insert(k, v, visibility)  # visibility:=Private|Public
```

### Plugin interaction with UI and core
Plugins define their capability using triplets `keyword - callback_function -
values_needed_with_types`. For example:
```
# For a notes plugin
add - add_note() - {
name: str
content: str
tags: [str, str, ...]
}
```
Interface is responsible for gathering required data. After processing data
plugin can return other data with specified types. For example:
```
status: created
image: ./success.jpg
etc: str
```
Interface is then again responsible for displaying the returned data in a
meaningful way.
