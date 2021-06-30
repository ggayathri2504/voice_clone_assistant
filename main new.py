# Initializing all the encoder libraries
import os
import sys

from IPython.utils import io
import sounddevice as sd
import time
import wikipedia
import speech_recognition as sr
import datetime
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa
import pywhatkit
import warnings
import pyjokes


warnings.filterwarnings('ignore')

def talk(text):
  encoder_weights = Path("encoder/saved_models/pretrained.pt")
  vocoder_weights = Path("vocoder/saved_models/pretrained/pretrained.pt")
  syn_dir = Path("synthesizer/saved_models/logs-pretrained/taco_pretrained")
  encoder.load_model(encoder_weights)
  synthesizer = Synthesizer(syn_dir)
  vocoder.load_model(vocoder_weights)
  in_fpath = Path("elon.wav")
  reprocessed_wav = encoder.preprocess_wv(in_fpath)
  original_wav, sampling_rate = librosa.load(in_fpath)
  preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
  embed = encoder.embed_utterance(preprocessed_wav)
  with io.capture_output() as captured:
    specs = synthesizer.synthesize_spectrograms([text], [embed])
  generated_wav = vocoder.infer_waveform(specs[0])
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  sd.play(generated_wav, samplerate=synthesizer.sample_rate)

# creating assisant
listener = sr.Recognizer()


#recieving the command
def take_cmd():
  try:
    with sr.Microphone() as source:
      print("listening...")
      voice = listener.listen(source)
      cmd = listener.recognize_google(voice)
      cmd = cmd.lower()
      if 'python' in cmd:
        cmd = cmd.replace('python', '')
        print(cmd)
        return (cmd)

      elif 'exit' in cmd:
        talk('exiting the program....byee!')
        sys.exit()

  except:
    pass

def run_google():
  cmd = take_cmd()

  #playing song in youtube
  if 'play' in cmd:
    song = cmd.replace('play', '')
    talk('playing' + song)
    pywhatkit.playonyt(song)

  #getting current time
  elif 'time' in cmd:
    time = datetime.datetime.now().strftime('%I:%M:%p')
    talk('current time is ' + time)

  #searching in google
  elif 'search' in cmd:
    search =cmd.replace('search','')
    info = wikipedia.summary(search,1)
    talk(info)
    print(info)

  #joke
  elif 'joke' in cmd:
    talk(pyjokes.get_joke())

  #opening notepad
  elif 'open notepad' in cmd:
    talk("hey!  opening  notepad")
    os.system("start notepad")

  #opening excel
  elif 'open excel' in cmd:
    talk("hey!  opening  excel")
    os.system("start excel")

  #opening chrome
  elif 'open chrome' in cmd:
    talk("hey! opening  chrome")
    os.system("start chrome")

  #opening ppt
  elif 'open powerpoint' in cmd:
    talk("hey!  opening  powerpoint")
    os.system("start powerpnt")

  #if wrong command  else:
    talk('Please  say  the  command  again ')

while True:
    run_google()
    time.sleep(30)