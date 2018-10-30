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

Clone this repository by running::
	``git clone https://github.com/aliGeeee/NeutNuke.git``.
Alternatively, visit `this repository on GitHub <https://github.com/aliGeeee/NeutNuke>` and download a .zip file.


Basic use
==================

1. Run ``main/scripts/firstRun.sh`` to create an Anaconda environment if this is the first use.
2. For each microscope image, create a directory with the name of the sample within ``main/images``. Place the image in this directory. For example, for a sample entitled *Sample1*, the image should be located in ``main/images/Sample1/anyImageName.tiff``
3. Run ``main/scripts/pipe.sh``.
4. Output graphs and CSVs are located in ``main/summaries/graphs`` and ``main/summaries/csvs`` respectively.


Use with Milton
==================

1. Edit the target unix500 directory in the files ``main/scripts/copyToServer.sh`` and ``main/scripts/copyFromServer.sh``.
2. Run ``main/scripts/copyToServer.sh``. This copies all files in ``main/scripts`` to ``~/main/scripts`` in the unix500.
3. Run ``~main/scripts/firstRun.sh`` to create an Anaconda environment if this is the first use.
4. Navigate to ``~main/scripts``.
5. Submit a job to torquelord using the command ``qsub -d . -l walltime=48:00:00,nodes=1:ppn=20,mem=256gb pipe.sh``. Change the walltime as required; 50 images averaging 500MB each requires around 48hrs.
6. On your local machine, run ``main/scripts/copyFromServer.sh`` to copy over output files from the unix500.


Individual module use
==================

The ``main/scripts/pipe.sh`` script is actually just four independent scripts running together. They are, in order:
* 


Support
==================

Email gu.a@wehi.edu.au
