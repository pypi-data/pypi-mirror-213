# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 10:12
# @Author  : LiZhen
# @FileName: sound_recorder.py
# @github  : https://github.com/Lizhen0628
# @Description:
import threading
import time
import logging
import datetime
import os
import wave
from pathlib import Path
from threading import Thread

from weathon.utils.file_utils import FileUtils

from pyaudio import PyAudio, paInt16


class Recorder:

    def __init__(self, chunk=2048, n_channels=1, rate=44100):
        """

        Args:
            chunk: Specifies the number of frames per buffer, pyaudio内置缓冲大小.
            n_channels: 音轨数
            rate: 采样频率，每秒内对声音信号采样样本的总数目，44100Hz采样频率意味着每秒钟信号被分解成44100份。
            format: Sampling size and format,采样点的大小和类型

        """
        self.chunk = chunk
        self.n_channels = n_channels
        self.rate = rate
        self.format = paInt16
        self._running = True
        self.log = logging.getLogger()
        self.record_dir = FileUtils.ensure_dir(Path(os.environ["DATA_DIR"]) / "weathon" / "record_wav")

    def _recording(self):
        self._running = True
        self._frames = []
        pa = PyAudio()

        stream = pa.open(format=self.format,
                         channels=self.n_channels,
                         rate=self.rate,
                         input=True,                    # input : 是否为输入流，默认为否
                         frames_per_buffer=self.chunk)
        while self._running:
            data = stream.read(self.chunk)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        pa.terminate()

    def start(self):
        thread = Thread(target=self._recording, args=())
        thread.start()
        return thread

    def stop(self, thread: Thread = None):
        self._running = False
        if thread:
            thread.join()

    def save(self, filename=None):
        pa = PyAudio()
        if not filename:
            filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f') + ".wav"
        if not filename.endswith(".wav"):
            filename = filename + ".wav"

        filename = str(self.record_dir / filename)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.n_channels)
            wf.setsampwidth(pa.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self._frames))


if __name__ == '__main__':

    a = int(input("1: start, 2: stop . please input(1-2):"))
    if a == 1:
        recorder = Recorder()
        t = recorder.start()
        begin = time.time()
        print("start recording...")
        b = int(input("1: start, 2: stop . please input(1-2):"))
        if b == 2:
            recorder.stop(t)
            fina = time.time()
            t = fina - begin
            print(f'录音时间为{t}s')
            recorder.save()

