Detanglement
============

This repo contains a research project I work on at FKI/HTW Berlin.
As with most of my repositories, this is a work-in-progress, more specifically,
an alpha.

It is a tool that visulizes big amounts of geolocalized data on-demand.
At the moment, only a proof-of-concept plugin for WorldBank's Indicator API
is working with it, but it can theoretically be extended to work with many
different APIs; that is the goal, anyway.

Usage
-----

Coming soon.


Writing Plugins
---------------

Coming soon.

Contribute
----------

What needs to be done? Well, many things. I documented most of the bugs in a file
in `rc` called `KNOWN_BUGS`. You can add to it or open an issue. There is also file
in the directory called `PLANNED_FEATURES`, documenting what needs to be done.

The feature I am currently working on is a GUI frontend for the database so you can
conveniently add new APIs and API keys to the application. A database wrapper needs
to be created sooner or later as well(as it stands, the only database code is inlined
into a definition in the main script; not very beautiful).

I suggest you code a plugin and see if it works. If it does not, we can look at what is
the problem and fix it together.
