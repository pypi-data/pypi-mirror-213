# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 17:12
# @Author  : LiZhen
# @FileName: sound_plot_utils.py
# @github  : https://github.com/Lizhen0628
# @Description:

import scipy
import pylab


class SoundPlotUtils:

    @staticmethod
    def plotSoundWave(rate, sample):
        """
            Plots a given sound wave.
        """

        t = scipy.linspace(0, 2, 2 * rate, endpoint=False)
        pylab.figure('Sound wave')
        T = int(0.0001 * rate)
        pylab.plot(t[:T], sample[:T], )
        pylab.show()

    @staticmethod
    def plotPartials(binFrequencies, maxFreq, magnitudes):
        """
            Calculates and plots the power spectrum of a given sound wave.
        """

        T = int(maxFreq)
        pylab.figure('Power spectrum')
        pylab.plot(binFrequencies[:T], magnitudes[:T], )
        pylab.xlabel('Frequency (Hz)')
        pylab.ylabel('Power spectrum (|X[k]|^2)')
        pylab.show()

    @staticmethod
    def plotPowerSpectrum(FFT, binFrequencies, maxFreq):
        """
            Calculates and plots the power spectrum of a given sound wave.
        """

        T = int(maxFreq)
        pylab.figure('Power spectrum')
        pylab.plot(binFrequencies[:T], scipy.absolute(FFT[:T]) * scipy.absolute(FFT[:T]), )
        pylab.xlabel('Frequency (Hz)')
        pylab.ylabel('Power spectrum (|X[k]|^2)')
        pylab.show()

    @staticmethod
    def get_frequencies_axis(framerate, fft_length):
        binResolution = float(framerate) / float(fft_length)
        binFreqs = []
        for k in range(fft_length):
            binFreq = k * binResolution
            binFreqs.append(binFreq)
        return binFreqs