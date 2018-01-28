import numpy as np
import spacy
from spacy.attrs import LOWER, LIKE_URL, LIKE_EMAIL, IS_OOV
import dateparser




def get_info(texts, skip=-2, attr=LOWER, merge=False, nlp=None,
             **kwargs):
    if nlp is None:
        print("loading spacy model")
        #Load english tokenizer, tagger, parser, NER and word vectors
        nlp = spacy.load('en_core_web_lg')
    #texts = texts.split('\n')
    texts = [texts]

    pizza_loc = []
    dates  = []
    time = []

    ##TODO - USE CSV FILE FOR LOOKUP TABLE ON LOCATION NAMES

    for row, doc in enumerate(nlp.pipe(texts, **kwargs)):
        temp_pizza  = []
        temp_dates = []
        temp_time = []
        print("DOC NUMBER:", row)

        for token in doc:
            if token.lower_ in ["pizza"]:
                print("PIZZA FOUND @", token.text, token.idx)
                pizza_loc.append(token.idx)
                
        for ent in doc.ents:
            if ent.label_ == "DATE":
                dates.append([ent.text, ent.start_char, ent.end_char])
                print("Entity @", ent.start_char, ent.end_char, ent.label_, ent.text)
            if ent.label =="TIME":
                time.append([ent.text, ent.start_char, ent.end_char])
##        pizza_loc.append(temp_pizza)
##        dates.append(temp_dates)
##        time.append(temp_time)
    print("pizza", pizza_loc)
    print("dates", dates)
    print("time", time)
    return pizza_loc, dates, time


#def get_datelocation(text):
text = open("pizza_test.txt").read()
pizza_loc, dates, time = get_info(text)
'''
The following commented out code is the begining of
the logic of how we will get dates closest to eachother
in text by a naive/simple method of just idx distance.

Leave it for now. 
'''
##for date in dates:
##    date_text = date[0]
##    distance = min(abs(date[1]-pizza_loc[0]),
##                   abs(date[2]-pizza_loc[0]))
dates_as_text = [d[0] for d in dates]
date_to_return = max(dates_as_text, key=len)
parsed_date = dateparser.parse(date_to_return)
