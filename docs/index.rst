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
	``git clone https://github.com/aliGeeee/NeutNuke.git``.
Alternatively, visit `this repository on GitHub <https://github.com/aliGeeee/NeutNuke>`_ and download a .zip file.


Basic use on a local machine
==================

1. Install `GNU Parallel <https://www.gnu.org/software/parallel/>`_. For machines with Homebrew installed, this may be accomplished by running ``brew install parallel`` in the console.
2. Install NeutNuke as specified above in a directory of your choice. This creates a directory named `NeutNuke`.
3. If this is the first use of NeutNuke, navigate to `main/scripts` in the console. Run the shell script file `firstRun.sh` by entering ``./firstRun.sh``, which creates an Anaconda environment named `neutScriptsEnv`.  
4. For each microscope image, create a directory with the name of the sample within `main/images`. Place the image in this directory. For example, for a sample entitled *Sample1*, the image should be located in `main/images/Sample1/anyImageName.tiff`
5. Navigate to `main/scripts`.
6. Run `pipe.sh` using the command ``./pipe.sh``.
7. Output graphs and CSVs are located in `main/summaries/graphs` and `main/summaries/csvs` respectively.


Use with Milton
==================

1. Install NeutNuke as specified above in a directory of your choice within your `unix500` home area. This creates a directory named `NeutNuke`.
2. Follow steps 3-6 as for local machine use.
3. While within `main/scripts`, submit a job to torquelord using the command ``qsub -d . -l walltime=48:00:00,nodes=1:ppn=20,mem=256gb pipe.sh``. Change the walltime as required; 50 images averaging 500MB each requires around 48hrs.
4. Output graphs and CSVs are located in `main/summaries/graphs` and `main/summaries/csvs` respectively.


Individual module use
==================

The `main/scripts/pipe.sh` script is actually just four independent scripts running together. They are located in `main/scripts`, and are, in order:

* `cellIsolation.sh` (isolates individual cells from input .TIFF files)
* `nucAnalysis.sh` (analyses nuclei and cells isolated from .TIFF cells)
* `makeCSVS.sh` (generates summary statistics from nuclear and cell analysis)
* `makeGraphs.sh` (generates graphs from summary statistics)

These scripts may be run independently, but must be run in order.



Support
==================

Email gu.a@wehi.edu.au
