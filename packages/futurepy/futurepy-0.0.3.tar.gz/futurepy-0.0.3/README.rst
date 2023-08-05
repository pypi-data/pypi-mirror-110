futurepy
========

An unofficial CLI version for `FutureMe <https://www.futureme.org/>`__.

Installation
------------

``pip install futurepy``

Usage
-----

.. code:: python

   futurepy [options]

   Options:
       -s --subject <subject>  Your message subject.
       -b --body <body>        Your message body.
       -d --date <date>        The future date to which to send your message to.
                               Format: YYYYMMDD
       -e --email <email>      Your email.
       -p --public             Post publicly
                               Default: False
       -c --confirm            Display a preview of the message before sending
                               Default: False
       -h --help               Display this message.

Example
-------

``futurepy -s 'Message to the future' -b 'Hello, this will arrive in the future.' -d 20301009 -e email@mail.com -p``
