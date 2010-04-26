
This is Glu.


Files
=====
You can see the following files and directories:

src/            Contains the source code

src/python      Contains the Python code (this includes some test utilities).
                The glu/ directory there contains most of the code. starter.py
                and glujson.py are the exception.

src/python/starter.py      The start script for the Glu server. It is outside of the
                glu/ directory, because this is going to change depending on
                whether Glu runs in a container or standalone.

src/python/glujson.py      It's very annoying that this file is even necessary. The reason
                is that we would like to use JSON, but the available JSON
                library is different depending on the runtime: jython, python
                or Google AppEngine. It imports the 'right' JSON for each
                case. This file will eventually go away once we have it
                ported to pure Java, I assume.

src/python/glu_make_sample_resources.py    This is a small utility that creates some
                                resources on a running server. It's not fancy
                                and was just created for testing.


src/java        Contains the Java code

static_files/   The directory from where the Glu erver can serve static files.

app.yaml        This file is used for Google AppEngine. It contains the
                configuration for the application on GAE. OUTDATED!

index.yaml      This file is used for Google AppEngine. It's automatically
                updated by the GAE tools. OUTDATED!



Getting started
===============

Pure Python
-----------
0. Tell Glu that you are running in pure Python:
   Edit glu/platform_specifics.py and make sure that
   the PLATFORM variable is assigned like this:

    PLATFORM = PLATFORM_PYTHON

1. Set your PYTHONPATH to point to this directory:

    % export PYTHONPATH=`pwd`

2. Install 'paste' if you have not done so already:

    % easy_install paste

3. Make sure that 'simplejson' is available in your
   Python installation. If not do:

    % easy_install simplejson

4. In your /tmp directory, create a /rdb/ directory.
   That is where the server stores resource definitions.

5. Start the Glu server:

    % python src/python/starter.py


Jython
------
0. Tell Glu that you are running in Jython:
   Edit glu/platform_specifics.py and make sure that
   the PLATFORM variable is assigned like this:

    PLATFORM = PLATFORM_JYTHON

1. Set your PYTHONPATH to point to this directory:

    % export PYTHONPATH=`pwd`

2. Install 'simplejson' if you have not done so already:

    % wget http://peak.telecommunity.com/dist/ez_setup.py
    % jython ez_setyp.py
    % ln -s $JYTHON_HOME/bin/easy_install /usr/local/bin/jython_easy_install
    % jython_easy_install simplejson

3. In your /tmp directory, create a /rdb/ directory.
   That is where the server stores resource definitions.

4. Start the Glu server:

    % jython src/python/starter.py


Google AppEngine (OUTDATED!)
----------------
0. Tell Glu that you are running on AppEngine:
   Edit glu/platform_specifics.py and make sure that
   the PLATFORM variable is assigned like this:

     PLATFORM = PLATFORM_GAE

1. Move this directory into your local Google AppEngine
   install directory.

2. To run in the local development server, use this command
   from within your local AppEngine install:

     % python dev_appserver.py glu/

3. To upload to AppEngine, use this command from within your
   local AppEngine install:

     % python appcfg.py update glu/

