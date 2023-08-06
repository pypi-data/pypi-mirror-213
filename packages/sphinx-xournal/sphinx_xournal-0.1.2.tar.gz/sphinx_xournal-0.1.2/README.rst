==============
Sphinx Xournal
==============

.. image:: https://img.shields.io/pypi/v/sphinx-xournal.svg
   :target: https://pypi.python.org/pypi/sphinx-xournal

Sphinx extension to render images of Xournal files.

Usage
-----

You will need to start by installing the extension.

.. code-block:: bash

   pip install sphinx-xournal

Your sphinx conf.py file will need a few changes.
To enable this extension it needs to be added to the extensions list.

.. code-block:: python

   extensions = [
       "sphinx_xournal",
   ]

If xournalpp is not installed in the default location you need to specify one:

.. code-block:: python

   xournal_binary_path = "/a/different/place/xournalpp"


You are now ready to include your .xopp files in your marvelous documentation.

We provide you with 3 options:

Option 1:
~~~~~~~~~

You can generate a restructured image from any Xournal files.
This block inherits all the restructured image tags, like :align:.

.. code-block:: rst

   .. xournal-image:: ./example.xopp
      :format: svg
      :align: center

      Sketch of an example.

Option 2:
~~~~~~~~~

Same applies for the figure block.

.. code-block:: rst

   .. xournal-figure:: ./example.xopp
      :format: svg
      :align: center

      Sketch of an example.

Option 3 (Experimental):
~~~~~~~~~~~~~~~~~~~~~~~~

The last option allows you to embed the raw svg.

.. code-block:: rst

   .. xournal-raw:: ./example.xopp
      :format: svg
      :align: center

      Sketch of an example.
