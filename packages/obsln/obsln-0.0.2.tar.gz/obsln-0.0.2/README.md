
ObsLn
======

Introduction
------------

ObsPy is a wonderful toolset for seismologists. However, it can be bulky and it has several large dependencies which have to be installed for it to work, even for simple tasks like reading and writing files. ObsLn provides a very limited range of functionality from ObsPy without many of the dependencies and size. In particular this supports:

* Data stream and trace stuctures
* Reading/Writing  SEGY files
* Reading SEG2

As you will see the much of the code has been shamelessly hacked from ObsPy and the documentation has been left deliberately unaltered. Accordingly it is released under the same license as ObsPy. 

For full ObsPy functionality please see the ObsPy project on GitHub [here](https://github.com/obspy)

Installation
------------

    pip install obsln


Building the Docker Image
-------------------------

	docker build -t obsln:latest .


Running Examples in Docker Image
--------------------------------


	docker run -v `pwd`:/src/obsln --entrypoint=/bin/bash obsln:latest -c "python3 /src/obsln/runtest.py"