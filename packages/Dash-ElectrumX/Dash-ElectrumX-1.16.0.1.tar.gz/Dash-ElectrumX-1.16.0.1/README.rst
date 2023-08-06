================================================================
Dash ElectrumX - Reimplementation of electrum-server (Dash fork)
================================================================

  :Licence: MIT
  :Language: Python (>= 3.7)
  :Original Author: Neil Booth

This project is a fork of `spesmilo/electrumx <https://github.com/spesmilo/electrumx>`_.

Dash ElectrumX allows users to run their own Dash Electrum server. It connects to your
full node and indexes the blockchain, allowing efficient querying of history of
arbitrary addresses. The server can be exposed publicly, and joined to the public network
of servers via peer discovery. As of May 2020, a significant chunk of the public
Electrum server network runs ElectrumX.


Documentation
=============

- changelog_
- HOWTO_
- Documentation_

.. _changelog: https://github.com/akhavr/electrumx/blob/master/docs/changelog.rst
.. _HOWTO: https://github.com/akhavr/electrumx/blob/master/docs/HOWTO.rst
.. _Documentation: https://github.com/akhavr/electrumx/blob/master/docs/


Simple Install
==============

Dash-ElectrumX can be installed from PyPi::

    pip install Dash-ElectrumX

Simple run script (``server.crt``, ``server.key`` must be placed in the ``data`` dir)

.. code:: bash

    #!/bin/bash

    export EX_BASE=$(pwd)
    export EX_DATA=${EX_BASE}/data
    export DB_DIRECTORY=${EX_DATA}/db
    export USERNAME=$USER
    export SSL_CERTFILE=${EX_DATA}/server.crt
    export SSL_KEYFILE=${EX_DATA}/server.key

    export COIN=Dash
    export NET=mainnet
    export SERVICES=ssl://127.0.0.1:51002
    export DAEMON_URL=http://rpc_user:rcp_password@127.0.0.1

    ${EX_BASE}/electrumx_server
