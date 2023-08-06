import requests
## not required (just for local testing)
class model:
    def __init__(self,model_url):
        self.model_url = model_url
    
    def text_to_speech(self,text):
        ## sending request to the model
        self.speech_content = requests.post(self.model_url,json={'text':text}).content
    
    def save_speech(self,file_name="result.wav"):
        ## saving the speech content to a file
        with open(file_name,"wb") as f:
            f.write(self.speech_content)


