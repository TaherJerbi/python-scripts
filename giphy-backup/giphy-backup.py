import requests
import json
import os

def main():
    username = input("Please provide your Giphy username: ")
    res = requests.get("https://giphy.com/channel/%s"%username)
    content = str(res.content)
    index = content.find("channelId")
    if index > 0:
        # Find the Channel id to make the api call.
        id = int(content[index+11:].split("}")[0])
        print("User Found. ID : %d"%id)

        # Set max downloads
        max = int(input("How many GIFs would you like to download? (Enter 0 to download all) : "))

        # Set File extension
        print("Choose a file extention\n1/ .gif\n2/ .mp4")
        ext_r = ""
        while not ext_r in ["1","2"]:
            ext_r = input(": ")
        extension = "gif" if ext_r is "1" else "mp4"
        print("Extension : %s"%extension)


        LINK = "https://giphy.com/api/v3/channels/%d/gifs"%id
        current_link = LINK 
        part = 1
        count = 0
        if not "GIFS" in os.listdir("./"):
            os.mkdir("GIFS")
        # Go through all the pages to get all the gifs
        while current_link:
            res = requests.get(current_link)
            data = res.json()
            results = data["results"]
            current_link = data["next"]
            print("Downloading part %d : %d GIFS"%(part,len(results)))
            for r in results:
                if (count>max-1 and max!=0):
                    return
                with open("./GIFS/%s.%s"%(r["slug"],extension),"wb") as g:
                    res_gif = requests.get(r["images"]["original"][extension if extension=="mp4" else "url"])
                    count+=1
                    print("%d/%s Downloading GIF with id : %s"%(count,max if max != 0 else ".",r["slug"]))
                    g.write(res_gif.content)
            part+=1
    else :
        print("user not found")


if __name__ == "__main__":
    main()