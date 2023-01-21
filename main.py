import openai
import urllib.request
from PIL import Image
import json


def settings():
    try:
        with open('settings.json') as json_file:
            data = json.load(json_file)
            return data['settings'][0]["API_KEY"], data['settings'][0]["IMAGE_DIRECTORY"]
    except:
        directory = input("Where should images be stored? (full directory)\n> ")
        api = input("Your openai api key (stored locally)\n> ")

        data = {'settings': [{'API_KEY': api, 'IMAGE_DIRECTORY': directory}]}

        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile)

        return api, directory


def genImage(imageDirectory, prompt, size):  # gens an image using openai dalle and then downloads it.
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    image_url = response['data'][0]['url']

    # print(image_url)
    # print(prompt)

    urllib.request.urlretrieve(image_url, imageDirectory)
    print("> Generated image.")
    image = Image.open(imageDirectory)
    if size == "p":
        cropped_img = image.crop((0, 0, 576, 1024))
        cropped_img.show()
    else:
        image.show()
        print("> Shown Image")


apikey, directory = settings()

openai.api_key = apikey

option = input(
    "---- AI Desktop Wallpaper Generator ---- \nBy Gwyd\nCurrently this can generate (C)itys, (N)ature and cursed ("
    "A)nime or (CU)stom.\nPlease input an option\n> ").lower()

if option == "c":
    finalPrompt = "City digital art realistic photo desktop wallpaper detailed portrait"
elif option == "n":
    finalPrompt = "Nature forest  desktop wallpaper detailed portrait"
elif option == "a":
    finalPrompt = "anime digital art photo desktop wallpaper detailed portrait"
elif option == "cu":
    finalPrompt = input("Input your custom dall-e prompt\n> ")
else:
    print("> That is not an option.")
    exit()

option1 = input("Sizes (l)andscape, (p)ortrait or (N)one - this will keep the original size.\nPlease input an "
                "option\n> ").lower()
if not option1 == "l" and not option1 == "p" and not option1 == "n":
    print("> That is not an option.")
    exit()
else:
    print("> Please wait . . .")
    genImage(directory, finalPrompt, option1)
