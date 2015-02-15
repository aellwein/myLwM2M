myLwM2M - Lightweight M2M Server
================================

### About
myLwM2M is an ongoing [LWM2M](https://github.com/OpenMobileAlliance/OMA-LwM2M-Public-Review) 
server implementation in Python 3.

### Requirements
* [Python 3.4+](http://python.org/downloads/)
* [aiocoap](https://github.com/chrysn/aiocoap) -- a [CoAP](http://coap.technology) framework

### Installation
* After downloading and installing [Python 3.4+](http://python.org/downloads/),
  use ``pip`` tool bundled with Python in order to install aiocoap:
  ``pip install aiocoap`` (requires root priviledges) or
  ``pip install aiocoap --user`` (user-local installation).
* Install myLwM2M:
  ``python setup.py install`` (requires root priviledges) or
  ``python setup.py install --user`` (user-local installation).

### License
myLwM2M is licensed under the terms of [MIT License](LICENSE.md).

### ToDo
* ~~Register/Update/Delete~~
* Binding Modes (~~U~~/Q/S)
* Security Modes (DTLS, PSK, Raw PKC, X.509, SMS Sec)
* Device Management & Service Enablement:
    * Read
    * Write
    * Execute
    * WriteAttributes
    * Observe
    * Discover
    * Create
    * Delete
* Bootstrap functionality
* Documentation
* OMA Tests Conformance

