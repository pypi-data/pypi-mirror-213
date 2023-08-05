.. _sec-experiment_setup:

****************
Parameters file
****************

The settings for a test are stored in a parameters file (which is a simple text file). An example parameters file is shown below::

  angles : -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70
  labels : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
  channels : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
  n_chan : 15
  n_blocks : 1
  stim_list_file : stim_list.csv
  randomize : true
  demo_stim : pink_noises/noise1.wav
  demo_stim_lev : 65


The following fields need to be specified in a parameters file:

  - `angles`: the azimuth angles (in degrees) at which the sounds are presented. Note that a 0° angle indicates straight ahead, a 90° angle is to the right, and a -90° angle to the left.
  - `labels`: a label for each of the angles, this can be a number or a letter (e.g., a, b, c, ecc.)
  - `channels`: the channel of the soundcard that will be used to present a sound at the corresponding angle
  - `n_chan`: the total number of channels for the setup
  - `n_blocks`: the number of blocks, that is how many times the test will be repeated
  - `stim_list_file`: the path (absolute or relative) to the file containing the stimulation list (see below)
  - `randomize`: if `true` the stim_list_file will be shuffled before each block repetition
  - `demo_stim`: the path to the WAV file to be used for the demo
  - `demo_stim_lev`: the sound level (in dB SPL) to be used for the demo

    
**************************
Stimulation file
**************************

Stimulation files specify the stimuli that will be played on each trial of the test. Figure :ref:`fig-stim_file` shows an example stimulation file.

.. _fig-stim_file:

.. figure:: Figures/stim_file.png
   :scale: 50%
   :alt: Example stimulation file

   Example stimulation file.

Each row of the file represents a trial. Stimulation files contain the following columns:

  - `angle`: the angle at which the sound will be presented (stimuli will be sent to the corresponding soundcard channel as specified in the parameters file)
  - `sound_file`: the path (relative or absolute) to the WAV file to be played
  - `condition`: an optional label specifying the experimental condition
  - `level`: the `base` sound level (in dB SPL) at which the sound will be presented (this assumes that `sound_source_id` has been correctly calibrated)
  - `roving`: a level rove, actual sound level will be euqual to the base level plus a value drawn from a random uniform distribution between +/- the roving level
  - `feedback`: if `true`, feedback will be given to the listener at the end of each trial
