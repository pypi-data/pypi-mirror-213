# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 14:33
# @Author  : LiZhen
# @FileName: onset_frames_split.py
# @github  : https://github.com/Lizhen0628
# @Description:

import wave
import os
from pathlib import Path

import librosa
import shutil

from weathon.utils import NoiseReduction, FileUtils


class OnsetFrameSplitter:
    """
        A class for splitting a file into onset frames.
    """

    def __init__(self, music_file, output_directory=None):
        self.music_file = Path(music_file)
        self.music_file_noise_reduction = music_file.split(".")[0] + "_noise_reduction.wav"
        self.output_directory = Path(output_directory) if output_directory else self.music_file.parent / "frame_temp"
        self.verbose = False
        self.nr = NoiseReduction(self.music_file, self.music_file_noise_reduction)

    def onset_frames_split(self):
        """
            Splits a music file into onset frames.
        """

        # noise reduction
        self.nr.noise_reduction()
        print('Executed noice reduction')

        # onset_detect
        y, sr = librosa.load(self.music_file_noise_reduction)
        onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")
        if self.verbose:
            print("onsets: ")
            for o in onsets:
                print(o)

        print('Executed librosa function to split the file into onsets')
        input_music_wave = wave.open(str(self.music_file), "rb")
        nframes = input_music_wave.getnframes()
        params = input_music_wave.getparams()
        framerate = input_music_wave.getframerate()
        duration = nframes / float(framerate)

        if self.verbose:
            print("nframes: %d" % (nframes,))
            print("frame rate: %d " % (framerate,))
            print("duration: %f seconds" % (duration,))

        onsets = list(onsets)
        onsets.append(duration)
        onsets[0] = 0.0

        # clear the directory
        FileUtils.clear_directory(self.output_directory)

        print('Just about to split the file into onset frames')

        # Splitting the music file into onset frames.
        for i in range(len(onsets) - 1):
            frame = int(framerate * (onsets[i + 1] - onsets[i]))
            sound = input_music_wave.readframes(frame)
            music_wave = wave.open(os.path.join(self.output_directory, "note%d.wav" % (i,)), "wb")
            music_wave.setparams(params)
            music_wave.setnframes(frame)
            music_wave.writeframes(sound)
            music_wave.close()
        print('Split the file into onset frames')


if __name__ == '__main__':
    music_file = "/Users/lizhen/data/weathon/record_wav/111.wav"
    splitter = OnsetFrameSplitter(music_file)
    splitter.onset_frames_split()
