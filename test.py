from transformers import pipeline

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
)

sentences = [
    'This is a movie.',
    'Movies are awesome.',
    "Eat at Valerie's Diner",
    "remember the alamo",
    'CONNKKT BIT.LY/H43242njnk99 >>>>><><<<<< CRUUUUWN',
    'olha que coisa mais linda',
    '我每天吃好吃的牛'
]

for sentence in sentences:
    response = distilled_student_sentiment_classifier(sentence)
    print(response)