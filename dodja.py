import logging.config
import playsound
import threading
import argparse
import requests
import warnings
import pyaudio
import wave
import time
import os
from datetime import datetime


FS = 44100
CHANNELS = 2
CHUNK = 1024
TIME_FRAME = 3
TEMPDIR = '__wavtemp__'
TOKEN = None    # TODO: Put your token here
DESCRIPTION = '''
Listens to system audio output and notify the occurence 
of given Thai phrases, (not) useful for dodging classes.
'''

_alarm = False


def main():
    warnings.filterwarnings('ignore')
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '--v', dest='verbose', action='store_true', default=False,
        help='Logs found contents if this flag is specified'
    )
    parser.add_argument(
        'phrases', metavar='ph', type=str, nargs='+',
        help='Thai phrases to detect'
    )
    args = parser.parse_args()

    from pythaiasr import asr

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True
    })
    os.system(f"mkdir {TEMPDIR}")
    path = os.path.join(TEMPDIR, 'temp.wav')
    frames = []
    num_frames = int((FS/CHUNK)*TIME_FRAME)

    def callback(in_data, frame_count, time_info, status):
        nonlocal frames
        frames.append(in_data)
        time_stamp = datetime.now().strftime('%H:%M:%S')
        if len(frames) >= num_frames:
            latency = time.time()
            with wave.open(path, 'wb') as wf:
                wf.setsampwidth(2)
                wf.setnchannels(CHANNELS)
                wf.setframerate(FS)
                wf.writeframes(b''.join(frames))
                frames = []
            texts = asr(path)
            latency = time.time() - latency
            for phrase in args.phrases:
                if phrase in texts:
                    message = f"Hurry up! Someone just said {phrase} at {time_stamp}."
                    if not _alarm:
                        thread = threading.Thread(target=report, args=(message,))
                        thread.start()
                    if args.verbose:
                        print(f"{phrase}\t\t{time_stamp}\t\t{latency:.4f}\t\t{texts}")
        return (in_data, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    device = p.get_default_input_device_info()['index']
    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)['name'] == 'CABLE Output (VB-Audio Virtual Cable)':
            device = i
            break
    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=FS,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device,
        stream_callback=callback
    )
    print(f"Listening for {', '.join(args.phrases)} within {TIME_FRAME}-second time frames...")
    if args.verbose:
        print("phrase\t\ttime_stamp\t\tlatency\t\tsentence")
    stream.start_stream()
    while stream.is_active():
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
    print("Terminating...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    os.system(f"rmdir {TEMPDIR} /s /q")
    print("Terminated Successfully")


def report(message):
    global _alarm
    _alarm = True
    playsound.playsound('assets/siren.wav')
    r = requests.post(
        url='https://notify-api.line.me/api/notify',
        headers={'Authorization': f"Bearer {TOKEN}"},
        data={'message': message}
    )
    _alarm = False
    return


if __name__ == '__main__':
    main()
