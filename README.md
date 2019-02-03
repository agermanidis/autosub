# pyTranscriber

pyTranscriber is an application that can be used to generate <b>automatic transcription / automatic subtitles </b> for audio/video files through a friendly graphical user interface. The hard work of speech recognition is made by the <a href="https://cloud.google.com/speech/">Google Speech Recognition API</a>.
<br>
<br>
This app consists basically of a friendly pyQt5 graphical interface for a customized version of <a href="https://github.com/agermanidis/autosub">Autosub 0.4.0</a>. All the hard work of processing the audio and generating the subtitles is done by Autosub.
<br>
<br>
pyTranscriber is a improved version of my previous project JAutosub (Java), created because of the limitations, issues, and overhead of mixing this 2 different languages on a single project.
<br>
<br>
The app by default outputs the subtitles as .srt and the transcribed audio on the user interface as well  as .txt files.
Internet connection is REQUIRED because it uses the <a href="https://cloud.google.com/speech/">Google Cloud Speech Server</a> for the job, in the same way as the <a href="https://support.google.com/youtube/answer/6373554?hl=en">Youtube Automatic Subtitles</a>.
<br>
<br>
IMPORTANT: As speech recognition technology is still not fully accurate, the <b>accuracy</b> of the result can vary a lot, depending on many factors, mainly the <b>quality/clarity</b> of the audio. Ideally the audio input should not have background noise, sound effects or music. If there is a single speaker and he speaks in a clear and slow speed seems that the recognition is much more accurate. Sometimes, under ideal/lucky conditions it is possible to get a <a href="https://medium.com/@mlockrey/youtube-s-incredible-95-accuracy-rate-on-auto-generated-captions-b059924765d5">accuracy result close to 95%</a>.
<br>
<br>
<h1>For Users - Download the Linux app</h1>
Coming  soon

<h1>For Developers - Technical Details</h1>
Check at <a href="https://github.com/raryelcostasouza/pyTranscriber/blob/master/pytranscriber/doc/technical_details.txt">technical_details.txt<a>

### License

GPL v3
