.. _sec-calibration:

************************
Sound Level Calibration
************************

Figure :ref:`fig-edit_transducers` shows a screenshot of the ``Transducers`` dialog which is used for setting calibration values.

.. _fig-edit_transducers:

.. figure:: Figures/edit_transducers.png
   :scale: 75%
   :alt: Edit transducers dialog

   Edit transducers dialog

Most of the fields should be pretty much self-explanatory. Using this
dialog you can add headphones/speakers models to the transducers database. In `sound_source_id` levels are referenced to the level that would be output by a full amplitude sinusoid (a sinusoid with a peak amplitude of 1). In the ``Max Level`` field you should enter the level in dB SPL that is output by the transducer for a full amplitude sinusoid . However, getting reliable readings for a pure tone with a SPL meter is difficult, therefore, typically a noise is used for calibrating loudspeakers.

The procedure I normally use for calibrating loudspeakers is to save on disk a noise stimulus as a wav file. I filter the noise within the operating range of the SPL meter (usually around 0.05 to 8 kHz). The noise level needs to be reasonably loud as to avoid signal-to-noise ratio issues, but not too loud as to cause distortions or damage your hearing in the measurement process. Once I've found a reasonable level, by trial and error, I measure the actual level with an SPL meter held at the position where the listener head would be located relative to the loudspeaker during the experiment and note it down.

We can measure the RMS level of the WAV file with the noise used for calibration, let's call it :math:`rmsnoise`. A full amplitude sinusoid has a root-mean-square amplitude of 1/sqrt(2) = 0.707. The difference in dB between the level of a sinusoid at max amplitude and our calibration noise will be equal to:

.. math::

   dbdiff = 20*log10((1/sqrt(2))/rmsnoise)

Therefore, if our calibration noise had a level (measured with the SPL meter) or :math:`x` dB SPL, a sinusoid at max amplitude would have a level of:

.. math::

   maxlev = x + dbdiff

this is the value that you need to enter in the ``Max Level`` field of the transducers calibration table for the loudspeakers in question.
