==============
scrapy-jsonrpc
==============

scrapy-jsonrpc is an extension to control a running Scrapy web crawler via
JSON-RPC. The service provides access to the main Crawler object via the
`JSON-RPC 2.0`_ protocol.

It's enabled by the `JSONRPC_ENABLED`_ setting. The web server will listen
in the port specified in `JSONRPC_PORT`_, and will log to the file
specified in `JSONRPC_LOGFILE`_.

The endpoint for accessing the crawler object is::

    http://localhost:6080/crawler

Example client
==============

There is a command line tool provided for illustration purposes on how to build
a client. You can find it in ``example-client.py``. It supports a few basic
commands such as listing the running spiders, etc.

Settings
========

These are the settings that control the web service behaviour:

JSONRPC_ENABLED
---------------

Default: ``True``

A boolean which specifies if the web service will be enabled (provided its
extension is also enabled).

JSONRPC_LOGFILE
---------------

Default: ``None``

A file to use for logging HTTP requests made to the web service. If unset web
the log is sent to standard scrapy log.

JSONRPC_PORT
------------

Default: ``[6080, 7030]``

The port range to use for the web service. If set to ``None`` or ``0``, a
dynamically assigned port is used.

JSONRPC_HOST
------------

Default: ``'127.0.0.1'``

The interface the web service should listen on.

.. _JSON-RPC 2.0: http://www.jsonrpc.org/
