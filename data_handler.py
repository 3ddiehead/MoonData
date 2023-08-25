import bz2
import json
import os
import shutil

currdir = os.path.dirname(os.path.abspath(__file__))
datadir = currdir+'/compiledData'
dirpath = r"/Users/eddie/Desktop/Project Related Data/MoonData/01"


user_data = [
    "utc_offset",
    "location",
    "lang"
    ]

def decode_multiple_json(content):
    decoder = json.JSONDecoder()
    pos = 0
    objs = []
    while pos < len(content):
        # Skip whitespaces
        while pos < len(content) and content[pos].isspace():
            pos += 1

        # If we've reached the end of the content, break
        if pos >= len(content):
            break

        try:
            obj, pos = decoder.raw_decode(content, pos)
            objs.append(obj)
        except json.JSONDecodeError:
            # If there's a decode error at this position, it's likely that there's no more valid JSON to parse
            break
    return objs


days = os.listdir(dirpath)
print(days)


for dayitx, daypath in enumerate(days.reverse()):

    if dayitx>10: continue
    if len(daypath) > 2: continue

    with open(datadir+"/"+daypath+".json","w") as compfile:
        print('Working on day',daypath
            )
        output = []

        for walkabout in os.walk(dirpath+"/"+daypath):

            filepaths = [walkabout[0]+"/"+path for path in walkabout[2]]

            for itx, filepath in enumerate(filepaths):
    
                if filepath[-4:] != ".bz2": continue
                if itx%20==0:
                    print(itx)

                with bz2.BZ2File(filepath) as fr, open(filepath[:-4],"wb") as fw:
                    shutil.copyfileobj(fr,fw)
                fr.close()
                fw.close()

                with open(filepath[:-4],"rb") as jfile:
                    content_bin = jfile.read()
                    content = content_bin.decode("utf-8")
                    tweets = decode_multiple_json(content)
                    for tweet in tweets:
                        newtweet = {}

                        try:
                            newtweet["text"] = tweet["text"]
                            newtweet["created_at"] = tweet["created_at"]
                            newtweet["id_str"] = tweet["id_str"]
                        except:
                            continue
                        else:
                            for key in user_data:
                                try:
                                    newtweet[key] = tweet['user'][key]
                                except Exception as err:
                                    print(err)
                                    continue

                            output.append(newtweet)
                jfile.close()
                os.remove(filepath[:-4])

        compfile.write(json.dumps(output))

    compfile.close()



"""
Desired data from json files:
- "created_at":"DOW MON DD HH:MM:SS +???? YYYY"
- "id_str" : str
- "text" : str (often contains unicode and if RT - begins 'RT @XXX: ', if @ - begins '@XXX ')
- utc_offset : int in seconds
- location : str or nonexistent
- "lang" : "en"

RM anything not from the language list
RM anything w/o text

Data to pull from mooncalc.org:
- Length of lunar day from location and time
- Highest altitude from location
- Current altitude from location and time + utc_offset
- Time offset from meridian crossing from location and time + utc_offset
- Moon phase from location and time + utc_offset (OR just utc time for w/o location)

Data to pull from suncalc.org:
- Length of day from location and time
- Highest altitude from location
- Sun alt from location and time + utc_offset
- Time offset from meridian crossing from location and time + utc_offset
- Part of day from location and time + utc_offset
"""