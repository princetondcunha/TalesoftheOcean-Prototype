import pandas as pd
import numpy as np
from pydub.generators import Sine
from pydub import AudioSegment

columns = ['Time UTC', 'Temperature', 'Temperature QC Flag', 'Latitude', 'Latitude QC Flag', 
           'Longitude', 'Longitude QC Flag', 'Pitch', 'Pitch QC Flag', 'Roll', 'Roll QC Flag', 
           'True Heading', 'True Heading QC Flag']
data = pd.read_csv("output/BritishColumbiaFerries_HorseshoeBay-DepartureBayFerryRoute_Thermosalinograph_Temperature_20220623T173743Z_20220623T175959Z-NaN_clean.csv", skiprows=54, names=columns)

temp = data['Temperature'].dropna().values


C_MAJOR_SCALE = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88] 
mapped_frequencies = np.interp(temp, (temp.min(), temp.max()), (0, len(C_MAJOR_SCALE) - 1))
musical_notes = [C_MAJOR_SCALE[int(round(f))] for f in mapped_frequencies]


audio = AudioSegment.silent(duration=0)
durations = [250, 500, 750] 

for i, freq in enumerate(musical_notes):
    duration = np.random.choice(durations) 
    tone = Sine(freq).to_audio_segment(duration=duration).fade_in(50).fade_out(50)
    
    if i % 4 == 0: 
        lower_tone = Sine(freq / 2).to_audio_segment(duration=duration).fade_in(50).fade_out(50)
        tone = tone.overlay(lower_tone - 6) 
    audio += tone

audio.export("seawatertemp_musical.wav", format="wav")
