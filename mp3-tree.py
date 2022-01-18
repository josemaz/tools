# https://trac.ffmpeg.org/wiki/Encode/MP3
# Works in itunes 11
#! FIX
#! Agregar colores

import os, sys
import subprocess
import pandas as pd
from pathlib import Path

libitunes="Music/Music/Media.localized"

arts = os.listdir(libitunes)
arts = [e for e in arts if not e.startswith('.')]
arts = [e for e in arts if e != 'Automatically Add to Music.localized']

df = pd.DataFrame(columns=['Artist', 'Album'])
for art in arts:
    albums = os.listdir(libitunes + "/" + art)
    albums = [e for e in albums if not e.startswith('.')]
    for album in albums:
        df.loc[len(df)] = [art,album]

print(os.getcwd())
for idx, row in df.iterrows():
    compath = libitunes + '/' + row['Artist'] + '/' + row['Album']
    os.makedirs(row['Artist'] + '/' + row['Album'], exist_ok = True)
    os.chdir(row['Artist'] + '/' + row['Album'])
    print(row['Artist'] + '/' + row['Album'])
    for x in os.listdir(compath):
        if x.endswith(".aif"):
            infile = compath + "/" + x
            outfile = x.replace(".aif", ".mp3")
            print(infile)
            cmd = ["ffmpeg","-y","-i",infile,"-f","mp3", \
                    "-acodec","libmp3lame","-b:a","320k",outfile]
            # https://stackabuse.com/executing-shell-commands-with-python
            exe = subprocess.run(cmd, capture_output=True)
            if exe.returncode != 0:
                print("!!!ERROR: ",exe.returncode)
                sys.exit(15)
    os.chdir("../../")
