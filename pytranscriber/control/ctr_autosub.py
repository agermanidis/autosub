from autosub import FLACConverter
from autosub import SpeechRecognizer
from autosub import extract_audio
from autosub import find_speech_regions
from autosub import DEFAULT_CONCURRENCY
from autosub import DEFAULT_SUBTITLE_FORMAT
from autosub import GOOGLE_SPEECH_API_KEY
from autosub.formatters import FORMATTERS

import multiprocessing
import time
import os

from pytranscriber.util.util import MyUtil


class Ctr_Autosub():

    cancel = False

    @staticmethod
    def init():
        Ctr_Autosub.cancel = False

    @staticmethod
    def is_operation_canceled():
        return Ctr_Autosub.cancel


    @staticmethod
    def output_progress(listener_progress, str_task, progress_percent):
        # only update progress if not requested to cancel
        if not Ctr_Autosub.cancel:
            listener_progress(str_task, progress_percent)

    @staticmethod
    def cancel_operation():
        Ctr_Autosub.cancel = True

        while Ctr_Autosub.step == 0:
            time.sleep(0.1)

        # the first step involves ffmpeg and cannot be stopped safely
        if Ctr_Autosub.step == 1:
            # close wait for threads to finish their work first
            Ctr_Autosub.pool.close()
            Ctr_Autosub.pool.join()

        else:
            # terminates the threads immediately
            Ctr_Autosub.pool.terminate()
            Ctr_Autosub.pool.join()

    @staticmethod
    def generate_subtitles(# pylint: disable=too-many-locals,too-many-arguments
            source_path,
            src_language,
            listener_progress,
            output=None,
            concurrency=DEFAULT_CONCURRENCY,
            subtitle_file_format=DEFAULT_SUBTITLE_FORMAT
        ):

        # windows not support forkserver... only spawn
        if os.name != "nt" and "Darwin" in os.uname():
            # necessary for running on MacOS
            # method can be set only once, otherwise crash
            if 'forkserver' != multiprocessing.get_start_method(allow_none=True):
                multiprocessing.set_start_method('forkserver')
        Ctr_Autosub.cancel = False
        Ctr_Autosub.step = 0
        """
        Given an input audio/video file, generate subtitles in the specified language and format.
        """
        audio_filename, audio_rate = extract_audio(source_path)

        regions = find_speech_regions(audio_filename)

        converter = FLACConverter(source_path=audio_filename)
        recognizer = SpeechRecognizer(language=src_language, rate=audio_rate,
                                      api_key=GOOGLE_SPEECH_API_KEY)
        transcripts = []
        if regions:
            try:
                if Ctr_Autosub.cancel:
                    return -1

                str_task_1 = "Step 1 of 2: Converting speech regions to FLAC files "
                len_regions = len(regions)
                extracted_regions = []
                Ctr_Autosub.pool = multiprocessing.Pool(concurrency)
                for i, extracted_region in enumerate(Ctr_Autosub.pool.imap(converter, regions)):
                    Ctr_Autosub.step = 1
                    extracted_regions.append(extracted_region)
                    progress_percent = MyUtil.percentage(i, len_regions)
                    Ctr_Autosub.output_progress(listener_progress, str_task_1, progress_percent)
                if Ctr_Autosub.cancel:
                    return -1
                else:
                    Ctr_Autosub.pool.close()
                    Ctr_Autosub.pool.join()

                str_task_2 = "Step 2 of 2: Performing speech recognition "
                Ctr_Autosub.pool = multiprocessing.Pool(concurrency)
                for i, transcript in enumerate(Ctr_Autosub.pool.imap(recognizer, extracted_regions)):
                    Ctr_Autosub.step = 2
                    transcripts.append(transcript)
                    progress_percent = MyUtil.percentage(i, len_regions)
                    Ctr_Autosub.output_progress(listener_progress, str_task_2, progress_percent)

                if Ctr_Autosub.cancel:
                    return -1
                else:
                    Ctr_Autosub.pool.close()
                    Ctr_Autosub.pool.join()

            except KeyboardInterrupt:
                Ctr_Autosub.pbar.finish()
                Ctr_Autosub.pool.terminate()
                Ctr_Autosub.pool.join()
                raise

        timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]
        formatter = FORMATTERS.get(subtitle_file_format)
        formatted_subtitles = formatter(timed_subtitles)

        dest = output

        if not dest:
            base = os.path.splitext(source_path)[0]
            dest = "{base}.{format}".format(base=base, format=subtitle_file_format)

        with open(dest, 'wb') as output_file:
            output_file.write(formatted_subtitles.encode("utf-8"))

        os.remove(audio_filename)

        if Ctr_Autosub.cancel:
            return -1
        else:
            Ctr_Autosub.pool.close()
            Ctr_Autosub.pool.join()

        return dest
