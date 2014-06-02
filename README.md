Detanglement
============

This repo contains a research project I work on at FKI/HTW Berlin.
As with most of my repositories, this is a work-in-progress, more specifically,
an alpha.

It is a tool that visualizes big amounts of geolocalized data on-demand.
At the moment, only a proof-of-concept plugin for WorldBanks' Indicator API
is working with it, but it can theoretically be extended to work with many
different APIs; that is the goal, anyway.

Requirements
------------

The tool requires a few additional python libraries to work, namely:

```
PyQt5
pygeoip
geopy
```

Additionally, if you want the WorldBank plugin to work(which is the
only working plugin right now, so you might), you need to install
`wbpy`.
Also, if you want to check out the nonworking plugin for Twitter(which
adds markers to the map, but the data is not visualized), you need
to install `TwitterAPI`.

I have included all Javascript APIs you might need, hoping that no
licensing issues will emerge.

Usage
-----

There are many ways to invoke/use the application. I suggest you `git clone`
the repository first, change into the directory and check out the command-line
features(by invoking `./Tangle.py -h`). To wrap up what I just told you, 
it should look like this:

```bash
git clone https://github.com/hellerve/Detanglement.git
cd Detanglement
./Tangle.py -h
```

After you have made yourself familiar with the main scripts' features, you 
can explore the tool by typing:

```bash
./Tangle.py -a WorldBank
```

Which loads the script with WorldBanks' Indicator API and shows the tools
capabilities pretty well. Click around, make yourself at home.

(NOTE: In case you are wondering what the empty window popping up when you
click on the dotted rectangle means: that is where you will be able to add
APIs in the app itself, providing keys et cetera)

More coming soon.


Writing Plugins
---------------

Coming soon.

Contribute
----------

What needs to be done? Well, many things. I documented most of the bugs in a file
in `rc` called `KNOWN_BUGS`. You can add to it or open an issue. There is also file
in the directory called `PLANNED_FEATURES`, documenting what needs to be done.
You can also look at both files by invoking `./Tangle.py -d` or `./Tangle.py --devel`
or, if you have installed it (kudos, you are likely to use Linux, because it is a pain
to install it on any other platform at the moment) `Tangle -d`.

The feature I am currently working on is a GUI frontend for the database so you can
conveniently add new APIs and API keys to the application. A database wrapper needs
to be created sooner or later as well(as it stands, the only database code is inlined
into a definition in the main script; not very beautiful).

Also, the help file is a mess that needs to be cleaned up by someone who enjoys writing
HTML files more than me. It is a non-informative mess.

I suggest you code a plugin and see if it works. If it does not, we can look at what is
the problem and fix it together.
