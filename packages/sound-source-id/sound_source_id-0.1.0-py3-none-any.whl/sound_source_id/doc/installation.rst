.. _sec-installation:

************
Installation
************

``sound_source_id`` has been successfully installed and used on Linux and Windows. It should also work on Mac platforms, but this has not been tested. ``sound_source_id`` is written in Python and can be installed via pip:

.. code-block:: bash

		pip install sound_source_id


``sound_source_id`` depends on a few Python modules including:

  * PyQt5
  * numpy
  * scipy
  * matplotlib
  * pandas
  * PyAudio https://pypi.org/project/PyAudio/

depending on your Python distribution you may want to install these dependecies before installing ``sound_source_id`` via pip (e.g. through conda if you're using the Anaconda Python distribution or through your Linux distribution package manager if you're using the Python installation that comes with your Linux distribution), otherwise pip will attempt to automatically pull in and install these dependencies. If the program is successfully installed you should be able to start it from a bash/DOS terminal with the command:

.. code-block:: bash

	sound_source_id

You need to ensure that the Python environment you're using when you call the above command matches the one you used when you installed the application.

Sound can be played with either PyAudio, or SoX on Windows. On Linux pyalsaaudio can be also used. Depending on how you want sound to be played, you need to install:


  * pyalsaaudio https://pypi.org/project/pyalsaaudio/

or SoX:

  * https://sox.sourceforge.net/





