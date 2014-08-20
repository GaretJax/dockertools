"""
docker-tools

MIT License. See LICENSE for more details.
Copyright (c) 2013, Jonathan Stoppani
"""

__version__ = '0.1.0'
__url__ = 'https://github.com/GaretJax/dockertools'


# TODO: Monkey path requests 1.2.3 to support SNI. The lateste version supports
# this out of the box, but docker-py currently requires requests==1.2.3

import requests

if hasattr(requests, 'pyopenssl'):
    def fileno(self):
        return self.socket.fileno()

    def close(self):
        return self.connection.shutdown()

    requests.pyopenssl.WrappedSocket.close = close
    requests.pyopenssl.WrappedSocket.fileno = fileno
