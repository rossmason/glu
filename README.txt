
This is Glu.

Specifically, this is the pure Python version of Glu.



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


Development of mixed Jython/Java project in Eclipse
===================================================
This describes the necessary steps to be taken in Eclipse in order to
develop Glu as a mixed Jython/Java project.

0. The following pre-requisites are assumed:
    - You have checked out the Glu project somewhere. Hereafter, we will
      refer to the directory which was created during the checkout as "$GLU".
    - You have installed PyDev and Jython as described here:
      http://corp.wiki.mulesource.com/display/MULEDEV/Working+with+Python

1. Start a PyDev project and call it 'Glu_Python' (switch to the PyDev perspective for this).

2. Set the 'src' folder for this project to be $GLU/src/python. There is
   probably a neat way to do this in Eclipse (creating folder resources and
   referencing this somehow?), but it seems that PyDev is a bit more limited
   than a normal Java project. So, instead I just created a symbolic link to that
   external source directory in the $GLU folder:

        a. Go to the $WORKSPACE/Glu_Python directory.
        b. % rmdir src
        c. % ln -s $GLU/src/python src
        d. Refresh the project in Eclipse.

3. Start a Java project and call it 'Glu_Java' (switch to the Java perspective for this).

4. Set the 'src' folder for this project to be $GLU/src/java. For Java Eclipse
   offers other ways to include external folders. However, to keep things uniform
   I have simply used the symbolic link approach that I used for Python:

        a. Go to the $WORKSPACE/Glu_Java directory.
        b. % rmdir src
        c. % ln -s $GLU/src/java src
        d. Refresh the project in Eclipse.

   You should see the 'org.mulesource.glu' package and the sample FooBar.java file.

5. Right click on the 'Glu_Java' project, find the 'PyDev' menu item and select
   'Set as PyDev Project'.

6. Right click on the 'Glu_Python' project and select 'New->SourceFolder'.
   Chose to add the 'bin' folder from the 'Test_Java' project by specifying 'Test_Java'
   as the project name and 'bin' as the folder name.

7. Set 'Glu_Java' as a project reference for 'Glu_Python'.

8. Tell the system where to find your resources folder. For this, edit the file
   $GLU/src/python/glu/platform_specifics.py

   Locate the definition of STORAGE_OBJECT. Specifically the line:

        STORAGE_OBJECT = FileStorage("resourceDB")

   Edit the 'resourceDB' to be the absolute path for your resource directory.
   When you check out Glu you find a 'resourceDB' directory created within $GLU.
   You could therefore edit this to read "$GLU/resourceDB" (unless you set $GLU
   as a variable for the project, you'd have to expand that part of the path
   name manually).

   Alternatively, we can just use a link again. Since we start the server
   by running '$GLU/src/python/starter.py' we can create a symbolic link in
   $GLU/src/python to point to the actual location of the 'resourceDB' directory:

        % ln -s $GLU/resourceDB $GLU/src/python/resourceDB

   The advantage of this approach is that you don't have to edit the source
   file at all.

9. Use the same approach to tell Glu where to find the static_file folder.
   Either edit the $GLU/settings.py file and modify the STATIC_LOCATION variable,
   or create another symbolic link without editing any source:

        % ln -s $GLU/static_files $GLU/src/python/static_files

10. Test that your project works by right-clicking on 'starter.py' in your
    'Glu_Python' project (in the src/glu folder) and selecting 'Run As -> Jython Run'.

    After a short while you should see the server's startup message appear, informing
    you that it listens on port 8001. You should then be able to take your web browser
    to http://localhost:8001 and connect to the Glu server.








