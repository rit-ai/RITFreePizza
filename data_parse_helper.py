import numpy as np
import spacy
from spacy.attrs import LOWER, LIKE_URL, LIKE_EMAIL, IS_OOV
import dateparser
import pandas as pd
import re
import operator

##CREATE DICTIONARY FOR NICKNAMES FOR COLLEGES


##Testing this library for reverse name lookups
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def make_lookup_table():
    df = pd.read_csv("RIT_Buildings_Rooms2.csv", header=None,
                     names=["building", "room",
                            "c","d","e","f","g","h"],
                     usecols=["building", "room"],
                     error_bad_lines=False,
                     encoding='latin',
                     sep="\t")
    return df

##Takes our lookup table df and list of noun phrases to run distance measure on
def run_room_lookup(df, phrases):
    building = df.building
    building = building.drop_duplicates()
    building = building.tolist()

    rooms = df.room
    rooms = rooms.drop_duplicates()
    rooms = rooms.tolist()

    lookup_shortened_text = dict()
    for i, r in enumerate(rooms):
        if re.search("[a-zA-Z]{3,}", r):
            no_nums = re.sub(re.compile("[0-9\-]"), "", r)
            rooms[i] = no_nums.strip()
            lookup_shortened_text[no_nums.strip()] = r
            
        
    #re.sub(re.compile("[0-9\-]"), "", test)
    # result.strip()
    building_pairs = []
    room_pairs = []
    for p in phrases:
        building_pairs.append(process.extractOne(p, building))
        room_pairs.append(process.extractOne(p, rooms))
    
    return building_pairs, room_pairs, lookup_shortened_text

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
    buildings = []

    for row, doc in enumerate(nlp.pipe(texts, **kwargs)):
        #This sifts through noun chunks to find locations as "pobj" noun types
        for chunk in doc.noun_chunks:
#            print("CHUNK",chunk.text, chunk.root.text, chunk.root.dep_,
#                  chunk.root.head.text)
            if chunk.root.dep_ == "pobj":
                buildings.append(chunk.text)    
        for token in doc:
            if token.lower_ in ["pizza"]:
#                print("PIZZA FOUND @", token.text, token.idx)
                pizza_loc.append(token.idx)        
        for ent in doc.ents:
            if ent.label_ == "DATE":
                dates.append([ent.text, ent.start_char, ent.end_char])
#                print("Entity @", ent.start_char, ent.end_char, ent.label_, ent.text)
            if ent.label =="TIME":
                time.append([ent.text, ent.start_char, ent.end_char])

    return pizza_loc, dates, time, buildings

def get_datelocation(text):
    pizza_loc, dates, time, phrases = get_info(text)
    df = make_lookup_table()
    b, r, lookup_shortend_text = run_room_lookup(df, phrases)

    ##Adds up results from b and r (building and room)
    sums=[]
    for i in range(len(b)):
        sums.append(r[i][1] + b[i][1])

    index, _ = max(enumerate(sums), key=operator.itemgetter(1))

    if r[index][1] > b[index][1]:
        print("we choose room", r[index][0])
        temp_name = r[index][0]
        full_loc_name = df[df["room"] == '2050 - Reading Room']
    else:
        print("we choose building", b[index][0])
        temp_name = b[index][0]
        full_loc_name = df[df["room"] == '2050 - Reading Room']
        
    building_name, room_name = full_loc_name.values[0]

    ##This is the naive way of getting closest date...take most verbose
    ##and leave the rest...
    dates_as_text = [d[0] for d in dates]
    date_to_return = max(dates_as_text, key=len)
    parsed_date = dateparser.parse(date_to_return)

    return parsed_date, (building_name, room_name)

text = open("pizza_test.txt").read()

text = """CS1 Exam Review
Sunday, November 12th, 11-1pm in GOL-1400

Come review for the second CS1 exam. Pizza will be provided.
date, location = get_datelocation(text)
"""

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
