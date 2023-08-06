from gruut.utils import text_and_elements
from lxml import etree as etree
from gruut.const import EndElement
from word import word
import string
from text import text_processor
class parseSSML:
     def __init__(self,fileName) -> None:
        self.file_name = fileName
        self.stop_parsing = False ## to ignore the text inside the sub tag
        self.s_tag_open = False ## to check if the s tag is open
        self.p_tag_open = False ## to check if the p tag is open
        self.final_array = [] ## to store the final array of words
        self.parser_mode = "Normal" ## to set the mode of the parser
        self.text_processor = text_processor() ## see the text_processor class
        try:
            self.root_element = etree.parse("test.xml").getroot()
            if self.root_element.tag != "speak":
                raise Exception("Not a valid SSML file.")
        except Exception as e:
                raise e
        
     def iter_elements(self):
        ## iterate over the parsed elements in the xml file
        yield from text_and_elements(self.root_element)

     def parse(self):
        self.final_array = []
        for it in self.iter_elements():
            if type(it) is str:
                ## if element is text
                if self.stop_parsing == True:
                    continue
                self.handle_string(it)
            elif type(it) is EndElement:
                ## if element is closing tag
                if self.stop_parsing == True:
                    if it.element.tag == "sub":
                        self.stop_parsing = False
                    continue
                self.handle_tag(it.element,end=True)
            else: 
                ## if element is opening tag
                if self.stop_parsing == True:
                    continue
                self.handle_tag(it[0],end=False)
        ## joining the words to form the final string
        self.final_string = ""
        length = len(self.final_array)
        self.final_string += self.final_array[0].text
        for i in range(1,length):
            if self.final_array[i].text in string.punctuation and self.final_array[i-1].text not in string.punctuation:
                self.final_string += self.final_array[i].text
            else:
                self.final_string += " "
                self.final_string += self.final_array[i].text

     def get_final_string(self):
        ## call it after parsing to get the final string
        return self.final_string
     
     def handle_string(self,string):
         ## handle the text inside the xml file
         self.final_array += self.text_processor.handle_text(string,self.parser_mode)
     
     def handle_tag(self,element,end=True): 
         ## handle the tags inside the xml file
         if element.tag == "speak":
             pass
         elif element.tag == "sub":
             self.handle_sub_tag(element.attrib)
         elif element.tag == "s":
             self.handle_s_tag(end)
        #  elif element.tag == "p":
        #      self.handle_p_tag(end)
         elif element.tag == "say-as":
             self.handle_say_as_tag(element.attrib,end)
         else:
             ## in case of any other random tags
             if end == True:
                 self.final_array += self.text_processor.handle_text(f"</{element.tag}>",self.parser_mode)
             else:
                 options=""
                 attributes = dict(element.attrib)
                 for key,pair in attributes.items():
                     options += " "
                     options += f'{key}="{pair}"'               
                 self.final_array += self.text_processor.handle_text(f"<{element.tag}{options}>",self.parser_mode)
     
     def handle_sub_tag(self,attrib):
         ## for handling the sub tag
         if attrib is None:
             raise Exception("sub tag must have an attribute alias")
         elif 'alias' not in attrib:
             raise Exception("sub tag must have an attribute alias")
         else: 
             self.final_array += self.text_processor.handle_text(f"{attrib['alias']}",self.parser_mode)
             self.stop_parsing = True
     
     def handle_s_tag(self,end):
         ## for handling the s tag
         if end == True:
             ## closing tag
             if len(self.final_array) != 0:
                 finalText = self.final_array[-1].text
                 if finalText[-1] not in string.punctuation:
                     self.final_array.append(word("."))
             self.s_tag_open = False
         else:
             ## opening tag
             if self.s_tag_open == True:
                 raise Exception("<s> tag cannot enclose another <s> tag.")
             self.s_tag_open = True

     def handle_p_tag(self,end):
         ## for handling the p tag
         if end == True:
             ## closing tag
             if len(self.final_array) != 0:
                 finalText = self.final_array[-1].text
                 if finalText[-1] not in string.punctuation:
                     self.final_array.append(word("!"))
                 else: 
                     self.final_array[-1].text = self.final_array[-1].text[:-1] + "!"
             self.p_tag_open = False
         else:
             ## opening tag
             if self.s_tag_open == True:
                 raise Exception("<p> tag cannot enclose another <s> tag.")
             elif self.p_tag_open == True:
                    raise Exception("<p> tag cannot enclose another <p> tag.")
             self.p_tag_open = True

     def handle_say_as_tag(self,attrib,end):
            ## for handling the say-as tag
            if attrib is None:
                raise Exception("say-as tag must have an attribute interpret-as")
            elif 'interpret-as' not in attrib:
                raise Exception("say-as tag must have an attribute interpret-as")
            elif end == True:
                ## closing tag
                self.parser_mode = "Normal"
            else:
                ## opening tag
                if attrib['interpret-as'] == "characters" or attrib['interpret-as'] == "spell-out":
                    self.parser_mode = "Spell-out"
                elif attrib['interpret-as'] == "cardinal" or attrib['interpret-as'] == "number":
                    self.parser_mode = "Number"
                elif attrib['interpret-as'] == "ordinal":
                    self.parser_mode = "Ordinal"
                else: self.parser_mode = "Normal"

if __name__ == '__main__': 
    parseObject = parseSSML("test.xml") ## input file
    parseObject.parse()
    with (open("test.txt","w")) as f:
        ## output file
        f.write(parseObject.final_string)



          

