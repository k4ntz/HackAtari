.. HackAtari documentation master file, created by
   sphinx-quickstart on Fri Jun  9 20:50:33 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================================
Welcome to HackAtari's documentation!
=====================================

.. highlight:: python


.. container:: twocol

   .. container:: leftside

      HackAtari is a wrapper around the Atari environments available in gymnasium. 
      It automatically extracts the objects that exists in the state, 
      either via looking up their attribute in the RAM (fast), or using vision processing methods. 
      HackAtari environments also allow for object-centric Reinforcement Learning, as it is built upon (OCAtari)[https://github.com/k4ntz/OC_Atari].

   .. container:: rightside

      |changeram| 

.. |changeram| image:: _static/changeRAM3.png
  :width: 500
  :alt: Illustration of HackAtari on the Freeway game with two variations, on the cars colors and speed.


Cite our work
=============
If you are using HackAtari for your scientific work, please cite us:

.. code:: bibtex
   
   @inproceedings{Delfosse2023HackAtariIV,
      title={HackAtari: Introducing Variations to Atari Reinforcement Learning Environments},
      author={Quentin Delfosse and Jannis Bluml and Bjarne Gregori and Kristian Kersting},
      year={2024}
   }


Requirements
============
This project depends on:

- gymnasium
- numpy
- termcolor (if you want colored Warning error and messages)
- cv2 and torch (if you want to use an automatic wrapper that provides 4x84x84 observations (as used by DQN and many deep algorithms))

Download and install:
You can download from the
`Github <https://github.com/k4ntz/HackAtari>`_ repository or:

::

    pip install hackatari


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API:

   hackatari/core.rst
   hackatari/

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Games:
   :glob:

   hackatari/games/*




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
