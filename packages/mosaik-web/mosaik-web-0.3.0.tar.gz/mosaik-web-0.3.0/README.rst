mosaik-web
==========

A simple mosaik simulation visualization for web browsers.


Installation
------------

::

    $ pip install mosaik-web


Add mosaik-web to sim_config:

::

    sim_config = {
        'WebVis': {
            'cmd': 'mosaik-web -s 127.0.0.1:8000 %(addr)s',
        },
    }

Start mosaik-web without SSL:

::

    webvis = world.start('WebVis', start_date='2014-01-01 00:00:00', step_size=60)

Start mosaik-web with SSL:

::

    webvis = world.start('WebVis', start_date='2014-01-01 00:00:00', step_size=60, activate_ssl=True, keyfile=keyfile, certfile=certfile)

