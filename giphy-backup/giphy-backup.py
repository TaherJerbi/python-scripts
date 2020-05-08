import requests
import json
import os
from giphy_api_v3 import GIPHY_API

def main():
    username = input("Please provide your Giphy username: ")
    api = GIPHY_API(username)
    RAW_GIFS = api.getGifsRawLinks()
    
    for gif in RAW_GIFS:
        with open("%s.%s"%(gif["id"],gif["link"][-3:]),"wb") as gif_file:
            gif_binary = requests.get(gif["link"]).content
            gif_file.write(gif_binary)


if __name__ == "__main__":
    main()