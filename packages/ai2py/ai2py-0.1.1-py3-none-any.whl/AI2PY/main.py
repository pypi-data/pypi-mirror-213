import openai
import datetime
import urllib.request
from PIL import Image

class ai2py:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_text(self, data, word_count):
        def clean_text(data):
            clean_text = str(data).strip()
            return clean_text
        
        openai.api_key = self.api_key
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= data,
                temperature=0,
                max_tokens=word_count,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0
            )

            text = response["choices"][0]["text"]
            text = clean_text(text)
            return text
        
        except openai.error.OpenAIError as e:
            print(e.error)

    def create_text_command(self, command, data, word_count):
        def clean_text(data):
            clean_text = str(data).strip()
            return clean_text

        command = command + ": "
        combined_data = command + data       
        openai.api_key = self.api_key

        try: 
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= combined_data,
                temperature=0,
                max_tokens=word_count,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0
            )

            text = response["choices"][0]["text"]
            text = clean_text(text)
            return text
        
        except openai.error.OpenAIError as e:
            print(e.error)
    
    def create_image(self, prompt_text,image_size):
        now = datetime.datetime.now()
        filename = 'ai_image_' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        openai.api_key = self.api_key
        try: 
            response = openai.Image.create(
                prompt= prompt_text,
                n=1,
                size=image_size
            )
            print(response)
            image_url = response['data'][0]['url']
            print("Generating A.i. Image")
            url = image_url
            print(url)
            urllib.request.urlretrieve(url, filename)
            img = Image.open(filename)
            img.show()
            return(filename)
        
        except openai.error.OpenAIError as e:
            print(e.error)
    
    def create_image_variation(self, data, image_size):
        now = datetime.datetime.now()
        filename = 'ai_image_variation_' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        openai.api_key = self.api_key
        try:
            response = openai.Image.create_variation(
                image=open(data, "rb"),
                n=1,
                size=image_size
            )
            image_url = response['data'][0]['url']
            url = image_url
            urllib.request.urlretrieve(url, filename)
        
        except openai.error.OpenAIError as e:
            print(e.error)

    class options:
        def display_imagesizes():
            print("Required image_size: 256x256, 512x512, or 1024x1024 pixels")

        def image_resize(file_path, w_int, h_int):
            png_name = file_path[:-4]
            im = Image.open(file_path)
            img_resized = im.resize((w_int, h_int))
            img_resized.save(png_name + ".png")
            return img_resized




