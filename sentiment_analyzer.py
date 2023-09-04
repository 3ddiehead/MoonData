import json
import os
from transformers import pipeline

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    top_k=4
)

accepted_langs = [
    "ar", #Arabic
    "de", #German (Deutsch)
    "en", #English
    "es", #Spanish (Español)
    "fr", #French
    "hi", #Hindi
    "id", #Indonesian
    "it", #Italian
    "ja", #Japanese
    "ms", #Malay
    "pt", #Portuguese
    "zh"  #Chinese.Mandarin (Zhōngwén - 中文)
    ]

currdir = os.path.dirname(os.path.abspath(__file__))
datadir = currdir+'/compiledData'

output = []

with open(datadir+'/'+os.listdir(datadir)[0],'r') as infile:
    jstring = infile.read()
    jobj = json.loads(jstring)

    for itx, tweet in enumerate(jobj):
        if tweet["lang"] in accepted_langs:
            response = distilled_student_sentiment_classifier(tweet["text"])
            tweet["sentiment"] = response
            output.append(tweet)

infile.close()

with open(datadir+'/'+os.listdir(datadir)[0]+"_mod.json","w") as outfile:
    outfile.write(json.dumps(output))
outfile.close()
