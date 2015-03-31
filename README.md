myLwM2M - Lightweight M2M Server
================================

### About
myLwM2M is an ongoing [LWM2M](https://github.com/OpenMobileAlliance/OMA-LwM2M-Public-Review) 
server implementation in Python 3.

### Prerequisites
- [Python 3.4+](http://python.org/downloads/)
- [aiocoap](https://github.com/chrysn/aiocoap) -- a [CoAP](http://coap.technology) framework

### Installation
You will currently need to install aiocoap manually. Here are the required steps:
  - Clone it using ``git clone https://github.com/chrysn/aiocoap.git``
  - ``python setup.py install`` (system wide installation, requires root privileges) or
  - ``python setup.py install --user`` (for user-local installation).

- Install myLwM2M:
    - ``python setup.py install`` (system wide, requires root privileges) or
    - ``python setup.py install --user`` (user-local installation).

### Dev Mode
You can use [OMA LWM2M DevKit](https://addons.mozilla.org/de/firefox/addon/oma-lwm2m-devkit/) for 
testing/development. Just point it to ``coap://localhost:5683`` and load the "example client".
You should notice console output like:
```
DEBUG:myLwM2M-server:POST called with options {'lt': '60', 'b': 'U', 'ep': 'DEVKIT'}
```

### License
myLwM2M is licensed under the terms of [MIT License](LICENSE).

### ToDo
See [TODO](TODO.md).