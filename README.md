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
* External plugins support
* Pluggable UIs
* Plugins support
### Requirements (MVP)
* CRUD
* Support for multiple sites
* Support for multiple profiles for an each site
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
template: <template_identification>  | TODO: open problem, how to specify?
keys:
    first_name: John
    last_name: Rodgerson
    email: johnjohn@mealforfree.de
    password: cookies_for_free_meal_for_free
created_on: <date_specification>     | TODO: how exactly? Time zones?
notes: My main FB profile
<
any_other_optional_keys: ...
>
```
### Keyfile sketches
Just a random example of keyfile for a `first_name` key
```
first_name:
    - John: [list of linkfile ids]    |
    - Dolori: [list of linkfile ids]  | => TODO: open problem
    - Bob: [...]                      |
```
Keyfiles also are capable of storing shortcut information:
```
sites:
    - facebook.com: [...]
    - stackexchange.com: [...]
    - ...
```
### Things to consider
* Make sure all queries are as fast as it's possible
* Plugin system? Where to plug and what is to plub
* Fake files, updates and commits masking
