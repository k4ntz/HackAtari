=====================================
Welcome to HackAtari's Documentation!
=====================================

.. image:: _static/changeRAM3.png
   :width: 400
   :alt: Illustration of HackAtari on the Freeway game with two variations, on the cars colors and speed.
   :align: center

----

HackAtari is a powerful wrapper around the OCAtari environments available in Gymnasium.  
It enables you to play and research altered versions of classic Atari games by modifying the game RAM, creating novel game dynamics and a wide range of variations.

Built on top of `OC_Atari <https://github.com/k4ntz/OC_Atari>`_, HackAtari also supports object-centric Reinforcement Learning.  
OCAtari automatically extracts objects from the game state, either by RAM lookup (fast) or vision processing.

----

Cite Our Work
=============
If you use HackAtari for your scientific work, please cite us.

----

Requirements
============
HackAtari depends on:

- OCAtari: https://github.com/k4ntz/OC_Atari

**Installation:**

.. code-block:: bash

    pip install hackatari

Or download from the `GitHub repository <https://github.com/k4ntz/HackAtari>`_.

----

Reference
=============

.. toctree::
   :maxdepth: 2
   :caption: HackAtari Wrapper

   hackatari/core.rst

----

.. toctree::
   :maxdepth: 2
   :caption: HackAtari Modifications

   hackatari/modifications.rst

   ----

.. toctree::
   :maxdepth: 2
   :caption: Scripts

   scripts/rem_gui.rst
   eval/eval.rst
   eval/run.rst