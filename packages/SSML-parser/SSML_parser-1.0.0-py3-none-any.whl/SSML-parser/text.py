import re
from word import word
import string
from num2words import num2words
from utils import isfloat

class text_processor:
    def compress_whitespace(self, string):
        whitespace = re.compile(r"\s+")
        return whitespace.sub(" ", string)
    
    def handle_text(self,string,mode="Normal"):
        ## calls the required function
        if mode == "Normal":
            return self.handle_text_normal(string)
        elif mode == "Spell-out":
            return self.handle_text_spell_out(string)
        elif mode == "Number":
            return self.handle_text_number(string)
        elif mode == "Ordinal":
            return self.handle_text_ordinal(string)

    def handle_text_normal(self,string):
         string = string.replace("\n"," ") ## removing newlines
         string = self.compress_whitespace(string) ## compressing whitespaces
         tokens = string.split(" ")
         array = []
         for token in tokens:
             if token == "": continue
             array.append(word(token)) ## converting tokens into words
         return array

    def handle_text_spell_out(self,text):
        text = text.replace("\n"," ")
        text = self.compress_whitespace(text)
        tokens = list(text) ## storing character-by-character
        array = []
        for token in tokens:
            if token == "" or token == " ": continue
            array.append(word(token))
        return array

    def handle_text_number(self,text):
        text = text.replace("\n"," ")
        text = self.compress_whitespace(text)
        tokens = text.split(" ") ## tokenizing 
        array = []
        for token in tokens: 
            if token == "": continue
            elif token.isnumeric() or isfloat(token): 
                ## if text is numeric
                array.append(word(num2words(token,to="cardinal")))
            elif token[-1] in string.punctuation and (token[:-1].isnumeric() or isfloat(token[:-1])):
                ## if numeric text ends with a punctuation
                array.append(word(num2words(token[:-1])))
                array.append(word(token[-1]))
            elif len(token) > 2 and (token[-2:] == "th" or token[-2:] == "st" or token[-2:] == "nd" or token[-2:] == "rd"):
                ## if numeric text ends with an ordinal suffix
                if token[:-2].isnumeric():
                    array.append(word(num2words(token[:-2],to="ordinal")))
                else: array.append(word(token))
            elif len(token) > 3 and (token[-3:] == "ths" or token[-3:] == "sts" or token[-3:] == "nds" or token[-3:] == "rds"):
                ## if numeric text ends with a plural ordinal suffix
                if token[:-3].isnumeric():
                    array.append(word(num2words(token[:-3],to="ordinal") + 's'))
                else : array.append(word(token))
            else:
                ## invalid texts therefore ignore  
                array.append(word(token))        
        return array         
    
    def handle_text_ordinal(self,text):
        text = text.replace("\n"," ")
        text = self.compress_whitespace(text)
        tokens = text.split(" ")
        array = []
        for token in tokens:
            if token == "": continue
            elif token.isnumeric():
                ## numeric
                array.append(word(num2words(token,lang="en",to="ordinal_num")))
            elif token[-1] in string.punctuation and (token[:-1].isnumeric() or isfloat(token[:-1])):
                ## numeric and ends with a punctuation 
                array.append(word(num2words(token[:-1],to="ordinal_num")))
                array.append(word(token[-1]))
            else: array.append(word(token))
        return array

