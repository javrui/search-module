.. search module documentation master file, created by
   sphinx-quickstart on Mon Dec  9 10:29:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###############################
*search* module documentation
###############################

Welcome to *search* documentation!

.. toctree::
   :maxdepth: 2
   :caption: INTRODUCTION:
   :hidden:

   AI_intro

.. toctree::
   :maxdepth: 3
   :caption: USER GUIDE:
   :hidden:

   user_guide
   search_api_reference

.. toctree::
   :maxdepth: 4
   :caption: USAGE EXAMPLE:
   :hidden:

   maze/usage_example_maze

.. toctree::
   :maxdepth: 3
   :caption: ALL THE REST:
   :hidden:

   features
   credits_license
   testing


========================
What is *search* module?
========================

Python *search* module is a tool for solving problems involving state-space search, such as pathfinding or any domain requiring intelligent exploration of states.

This module includes implementations of two fundamental search algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS).

======================================
Watch *search* in action: maze solving
======================================

In :doc:`Usage example <maze/usage_example_maze>` you will find a complete Python script that solves mazes using *search* module.
This is just a glance of its outputs:

Static representation:
----------------------
.. image:: maze/maze_static_solution.png


Dynamic representation:
-----------------------
.. raw:: html

   <div align="center">
       <video width="700" controls>
           <source src="maze_dynamic_solution.mp4" type="video/mp4">
           Your browser does not support the video tag.
       </video>
   </div>


