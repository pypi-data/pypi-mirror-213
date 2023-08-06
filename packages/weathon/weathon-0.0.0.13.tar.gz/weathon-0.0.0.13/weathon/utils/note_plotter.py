# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 15:51
# @Author  : LiZhen
# @FileName: note_plotter.py
# @github  : https://github.com/Lizhen0628
# @Description:
import os
import numpy as np
from weathon.utils import MIDIDetector, number2melody
from pathlib import Path


class NotePlotter:
    """
        Class used for plotting sheet notes given MIDI note numbers.
    """

    def __init__(self, wav_file, onset_frames_directory, melody_title=None, melody_composer=None):
        print('Inside Note Plotter constructor')

        self.wav_file = wav_file
        self.onset_frames_directory = onset_frames_directory
        self.output_file = wav_file[:-3] + 'ly'
        self.number2note = number2melody

        self.melody_title = melody_title if melody_title else wav_file.split("/")[-1].split(".")[0]
        self.melody_composer = melody_composer if melody_composer else "___"

        # lilypond
        self.lilypond_version = '\\version \"2.25.1\"' + '\n'
        self.lilypond_language = '\\language english' + '\n\n'
        self.lilypond_header = '\\header { ' + '\n' \
                               + '\ttitle = \"' + self.melody_title + '\"' + '\n' \
                               + '\tcomposer = \"' + self.melody_composer + '\"' + '\n' \
                               + '\ttagline = ##f' + '\n' \
                               + '}\n\n'

        self.lilypond_layout = '\t\\layout {  %控制乐谱的显示\n' \
                               + '\t\t\\context {\n' \
                               + '\t\t\t\\Score\n' \
                               + '\t\t\tproportionalNotationDuration = #(ly:make-moment 1/4)\n' \
                               + '\t\t}\n' \
                               + '\t}\n'

        self.lilypond_midi = '\t\\midi { }\n'

    def plot_notes_violin_stuff(self):
        """
            Given .wav file detect MIDI notes, convert them into corresponding
            character names. Afterwards plot and save into an output file.
            The class uses lilypond library for drawing sheet notes.
        """

        # detector = MIDI_Detector(self.wav_file)
        detector = MIDIDetector(self.wav_file)
        midi_numbers = detector.detect_midi_notes()
        lilypond_text = '\\version \"2.14.2\" \n{ \n  \\clef treble \n'
        for n in midi_numbers:
            if n in self.number2note.keys():
                lilypond_text += self.number2note[n] + ' '
        lilypond_text += '\n}'
        with open(self.output_file, 'w') as f:
            f.write(lilypond_text)
        command = "lilypond/bin/lilypond "
        command += self.output_file
        print(command)
        os.system(command)

    def plot_notes(self):
        detector = MIDIDetector(self.wav_file)
        # detector = Highest_Peaks_MIDI_Detector(self.wav_file)
        midi_numbers = detector.detect_midi_notes()
        lilypond_text = '\\version \"2.14.2\" \n'
        lilypond_text += '  \\new PianoStaff { \n'
        lilypond_text += '    \\autochange { \n <'
        for n in midi_numbers:
            if n in self.number2note.keys():
                lilypond_text += self.number2note[n] + ' '
        lilypond_text += '>    \n}  \n}'
        with open(self.output_file, 'w') as f:
            f.write(lilypond_text)
        command = "lilyPond/bin/lilypond "
        command += self.output_file
        print(command)
        os.system(command)

    def plot_multiple_notes(self):
        """
            Plots notes using LilyPond library. The notes are on a left and righ
            hand staff (piano) and may be plotted as chords (multiple notes
            played simultaneously). The generated sheet notes are named after
            the music file.
        """

        lilypond_text = self.lilypond_version + self.lilypond_language + self.lilypond_header
        lilypond_text += '\\score { \n'
        lilypond_text += self.lilypond_layout
        lilypond_text += '  \\new Staff { \n'
        lilypond_text += '    \\fixed c\' { \n'

        n_files = len(os.listdir(self.onset_frames_directory))
        # for file_path in sorted(os.listdir(directory)):
        durations = []  # 每个音符的时长
        midi_notes = []  # 每个音符midi值
        max_duration = 0
        for i in range(n_files):
            file_path = os.path.join(self.onset_frames_directory, f"note{str(i)}.wav")
            detector = MIDIDetector(file_path)
            midi_numbers, du = detector.detect_midi_notes()
            print('File: ' + str(file_path) + ' MIDI: ' + str(midi_numbers))
            if len(midi_numbers) > 0:
                for n in midi_numbers:
                    if n in self.number2note.keys():
                        midi_notes.append(n)
                        durations.append(du)
                        if du > max_duration:
                            max_duration = du
        durations = np.array(durations)
        durations /= max_duration

        for i in range(len(midi_notes)):
            # lilypond_text += ' < '
            lilypond_text += self.number2note[midi_notes[i]] + " "
            # lilypond_text += ' >'
        lilypond_text += '\n\t\t}  \n\t}\n}'

        with open(self.output_file, 'w', encoding='utf8') as f:
            f.write(lilypond_text)

        os.system(f"lilypond {self.output_file}")

        # name = self.output_file.split('/')[-1].split('.')[0]
        # # command = "move " + name + '.pdf examples\\' + name + '.pdf'
        # command = "mv " + os.getcwd() + '/' + name + '.pdf ' + os.getcwd() + '/melody_note/work/note_pdf/' + name + '.pdf'
        # os.system(command)
        # print("## mv commond : " + command)
        # # command = "move " + name + '.mid examples\\' + name + '.mid'
        # command = "mv " + os.getcwd() + '/' + name + '.mid ' + os.getcwd() + '/melody_note/work/note_pdf/' + name + '.mid'
        # os.system(command)
        # print(command)

        # midi_notes 时间顺序的音符
        # durations 对应音符的持续时长, 最长为1
        return midi_notes, durations


if __name__ == '__main__':
    wave_file = "/Users/lizhen/data/weathon/record_wav/111.wav"
    onset_frames_directory = "/Users/lizhen/data/weathon/record_wav/frame_temp"
    note_plotter = NotePlotter(wave_file, onset_frames_directory)
    note_plotter.plot_multiple_notes()
