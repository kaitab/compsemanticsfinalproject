import spacy
import re
from nltk.corpus import verbnet


#load pos tagger
nlp = spacy.load("en_core_web_trf")

#get sentence
doc = input("Enter the sentence you'd like to see as lambda calculus:")

#remove punctuation
doc_list = doc.split(" ")
doc = " ".join([re.sub(r'[^\w\s]', '', word) for word in doc_list])

#get the POS tags
nlp_doc = nlp(doc)
tags = []
for word in nlp_doc:
    tags.append(word.pos_)

def lemmatize_verb(verb):
    "uses spacey to lemmatize a verb so verbnet will recognize it"
    verb_doc = nlp(verb)
    #the output of spacey's model has to be iterated thru even when there's only 1 input, that's why this function exists
    for verb in verb_doc:
        return verb.lemma_

def get_valency(verb):
    """uses verbnet to (ideally) return the valency category of a verb"""
    verb = lemmatize_verb(verb)
    frames = verbnet.frames(verbnet.vnclass(verbnet.classids(verb)[0]))[0]
    description = frames["description"]
    valency = description["primary"]
    return valency

class Noun:
    def __init__(self, word):
        self.lamb = "lx." + word + "(x)"

    def __str__(self):
        return self.lamb

    def combine(self, obj):
        self.lamb = word + "(" + obj.lamb + ")"


class Verb:
    def __init__(self, word):
        if get_valency(word) == "Intransitive":
            self.lamb = "lx." + word + "(x)"
            self.intrans = True
        else:
            self.lamb = "lx.ly." + word + "(x,y)"
            self.left = None
            self.right = None
            self.intrans = False

    def __str__(self):
        return self.lamb

    def combine(self, obj):
        if self.intrans == True:
            self.lamb = word + "(" + obj + ")"
            return self.lamb
        else:
            if self.right == None and self.left == None:
                self.lamb = "lx." + word + "(x," + obj + ")"
                self.right = obj
                return self.lamb
            elif self.left == None:
                self.lamb = word + "(" + obj + "," + self.right + ")"
                self.left = obj
                return self.lamb
            elif self.right == None:
                self.lamb = word + "(" + self.left + "," + obj + ")"
                self.right = obj
                return self.lamb
            else:
                raise "Error: too many arguments"

class Aux:
    def __init__(self, word):
        self.lamb = "lx.ly." + word + "(x,y)"
        self.left = None
        self.right = None

    def __str__(self):
        return self.lamb

    def combine(self, obj):
        if self.right == None and self.left == None:
            self.lamb = "lx." + word + "(x," + obj + ")"
            self.right = obj
            return self.lamb
        elif self.left == None:
            self.lamb = word + "(" + obj + "," + self.right + ")"
            self.left = obj
            return self.lamb
        elif self.right == None:
            self.lamb = word + "(" + self.left + "," + obj + ")"
            self.right = obj
            return self.lamb
        else:
            raise "Error: too many arguments"

class Adj:
    def __init__(self, word):
        self.lamb = "lx." + word + "(x)"

    def __str__(self):
        return self.lamb

    def combine(self, obj):
        self.lamb = word + "(" + obj.lamb + ")"
        return self.lamb

class PropN:
    def __init(self, word):
        self.lamb = word

    def __str__(self):
        return self.lamb

class Adv:
    def __int__(self, word):
        self.lamb = "lx." + word + "(x)"

    def __str__(self):
        return self.lamb

class Pron:
    def __init__(self, word):
        self.lamb = word

    def __str__(self):
        return self.lamb

class Prep:
    def __init__(self, word):
        self.lamb = "lx.ly." + word + "(x,y)"
        self.left = None
        self.right = None

    def __str__(self):
        return self.lamb

    def combine(self, obj):
        if self.right is None and self.left is None:
            self.lamb = "lx." + word + "(x," + obj + ")"
            self.right = obj
            return self.lamb
        elif self.left is None:
            self.lamb = word + "(" + obj + "," + self.right + ")"
            self.left = obj
            return self.lamb
        elif self.right is None:
            self.lamb = word + "(" + self.left + "," + obj + ")"
            self.right = obj
            return self.lamb
        else:
            raise "Error: too many arguments"

class Det:
    def __init__(self, word):
        if word == "all" or word == "every":
            self.lamb = "Ax.Y(x)"
        else:
            self.lamb = "Ex.Y(x)"

    def __str__(self):
        return self.lamb

class Conj:
    def __init__(self, word):
        if word == "if" or word == "then":
            self.lamb = "->"
            self.left = None
            self.right = None
        elif word == "or":
            self.lamb = "V"
            self.left = None
            self.right = None
        else:
            self.lamb = "^"
            self.left = None
            self.right = None

    def __str__(self):
        return self.lamb

    def combine(self, obj):
        if self.right is None and self.left is None:
            self.lamb = self.lamb + obj.lamb
            self.right = obj.lamb
            return self.lamb
        elif self.left is None:
            self.lamb = obj.lamb + self.lamb
            self.left = obj.lamb
            return self.lamb
        elif self.right is None:
            self.lamb = self.lamb + obj.lamb
            self.right = obj.lamb
            return self.lamb
        else:
            raise "Error: too many arguments"


pos_dict = {"NOUN": Noun, "PRON" : Pron, "ADP": Prep, "AUX": Aux, "VERB" : Verb, "DET" : Det, "CCONJ": Conj, "SCONJ":Conj, "ADV": Adj, "ADJ": Adj}

lambda_parse = []
for index,tag in enumerate(tags):
    if tag in pos_dict:
        lambda_parse.append(str(pos_dict[tag](doc_list[index])))
    elif tag != "SPACE":
        lambda_parse.append(str(Noun(doc_list[index])))

print(" ".join(lambda_parse))



