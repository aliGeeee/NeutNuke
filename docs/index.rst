.. NeutNuke documentation master file, created by
   sphinx-quickstart on Fri Jul 27 16:13:47 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation for NeutNuke
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Installation
==================

Clone this repository by running
``git clone https://github.com/aliGeeee/NeutNuke.git``
Alternatively, visit 'this repository on GitHub <https://github.com/aliGeeee/NeutNuke>' and download a .zip file.


Use
==================

1. Run ``main/firstRun.sh`` to create an Anaconda environment.
2. For each microscope image, create a directory with the name of the sample within ``main/images``. Place the image in this directory. For example, for a sample entitled *Sample1*, the image should be located in ``main/images/Sample1/anyImageName.tiff``
3. Run ``main/job.sh``.
4. Output graphs and CSVs are located in ``main/summaries/graphs`` and ``main/summaries/csvs`` respectively.


Support
==================

Email gu.a@wehi.edu.au
