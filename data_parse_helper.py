import numpy as np
import spacy
from spacy.attrs import LOWER, LIKE_URL, LIKE_EMAIL, IS_OOV
import dateparser
import pandas as pd
import re
import operator

##Testing this library for reverse name lookups
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

nickname_lookup= {"George Eastman Hall": ["EAS", "Eastman"],
"George H. Clark Gymnasium": ["CLK", "Clark Gym","Gym"],
"Student Alumni Union": ["SAU", "Campus Center", "Student Center", "Davis Room", "Fireside Lounge"],
"Wallace Library": ["WAL", "Wallace Center", "Library"],
"Liberal Arts Hall": ["LBR", "COLA"],
"James E. Booth Hall": ["BOO", "Booth"],
"James E. Gleason Hall": ["GLE", "KGCOE", "Gleason"],
"Golisano Hall": ["GOL", "Golisano", "GCCIS"],
"Frank E. Gannett Hall": ["GAN", "Gannett"],
"Thomas Gosnell Hall": ["GOS", "Gosnell", "Gosnell Atrium", "College of Science Atrium"],
"Lewis P. Ross Hall": ["ROS", "Ross"],
"Max Lowenthal Hall": ["LOW", "Saunders", "College of Business", "COB", "Lowenthal"],
"Simone Center for Innovation and Entrepreneurship": ["SIH", "Simone Center", "Fish Bowl", "Toilet Bowl", "Innovation Hall", "Entrepreneurship Hall"]}



def make_lookup_table():
    df = pd.read_csv("RIT_Buildings_Rooms4.csv", header=None,
                     names=["building", "room",
                            "c","d","e","f","g","h"],
                     usecols=["building", "room"],
                     error_bad_lines=False,
                     encoding='latin'
                     )
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
        if type(r) == float:
            continue
        if re.search(re.compile("[a-zA-Z]{3,}"), r):
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
                print(ent.text)
                dates.append([ent.text, ent.start_char, ent.end_char])
#                print("Entity @", ent.start_char, ent.end_char, ent.label_, ent.text)
            if ent.label =="TIME":
                time.append([ent.text, ent.start_char, ent.end_char])

    return pizza_loc, dates, time, buildings

def building_room_pair_search(df, building_room_pair):
    ##TODO this is only going to get one room...very dirty :(
    building = building_room_pair[0][0]
    room = building_room_pair[0][2]
    ##Going to lookup using nickname lookup
    for k, v in nickname_lookup.items():
        if v[0] == building:
            return k
    


def get_datelocation(text):
    pizza_loc, dates, time, phrases = get_info(text)
    df = make_lookup_table()

    #Try regex search to see if there is a simple building room pair
    building_room_pair = re.findall(re.compile("([A-Z]{3})(\-|\s)(\w\d{3}|\d{4})"),text)
    
    if len(building_room_pair) != 0:
        #Do something to get which building/room combo it is, or at least the building...
        building_name = building_room_pair_search(df, building_room_pair)
        room_search = df[df.building == building_name]
        all_rooms = room_search.values.tolist()

        for r in all_rooms:
            if building_room_pair[0][2] in r:
                room_name = building_room_pair[0][2]
                print("WE FOUND DAT ROOM NUMBER", room_name)
        print("WE FOUND DAT NAME BOIIII", building_name)
    else:
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

text2 = """CS1 Exam Review
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

text3 = """
The Simone Center for Innovation and Entrepreneurship invites you to join us tomorrow, Friday, January 19th from 12PM-1PM for Scott A. Snyder, PH.D.’s talk on Technology and Entrepreneurship in LOW-1225. All students, faculty and alumni are welcome.\n

Dr. Snyder is currently the Senior Vice President, Managing Director and Chief Technology and Innovation officer for Safeguard Scientifics, Inc. He has vast experience in the growth of technology related businesses with a particular focus on IoT, AI and enhanced security. He is also an accomplished author and a Senior Fellow at the Warton School as well as adjunct faculty at the Moore School of Engineering at the University of Pennsylvania.

Pizza will be provided. Please email Stephen Burke at srbvpr@rit.edu in the Simone Center for Innovation and Entrepreneurship with any questions.

In addition, requests for interpreters can be submitted to myaccess.rit.edu. Interpreters can be provided upon request and are subject to availability.    
"""

##for date in dates:
##    date_text = date[0]
##    distance = min(abs(date[1]-pizza_loc[0]),
##                   abs(date[2]-pizza_loc[0]))
