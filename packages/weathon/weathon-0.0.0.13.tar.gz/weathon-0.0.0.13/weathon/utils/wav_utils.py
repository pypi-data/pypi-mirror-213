# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 17:00
# @Author  : LiZhen
# @FileName: wav_utils.py
# @github  : https://github.com/Lizhen0628
# @Description:
import wave


class WaveProperties:

    def __init__(self, sound_file):
        # Read the sound wave from the input.
        wr = wave.open(sound_file, "r")

        # Get parameters of the sound wave.
        self.n_channels, self.sampwidth, self.framerate, self.n_frames, self.comptype, self.compname = wr.getparams()

    @property
    def duration(self):
        """
            Returns the duration of a given sound file.
        """
        return self.n_frames / float(self.framerate)

