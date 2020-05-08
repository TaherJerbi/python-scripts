import requests

class GIPHY_API:
    API_LINK = "https://giphy.com/api/v3/"
    def __init__(self,username=None):
        if username:
            self.username = username
            self.id = self.findUserID(username)
        else:
            self.username=None
            self.id=None

    def findUserID(self,username):
        res = requests.get("https://giphy.com/channel/%s"%username)
        content = str(res.content)
        index = content.find("channelId")
        if index > 0:
            # Find the Channel id to make the api call.
            id = int(content[index+11:].split("}")[0])
            print("Found user %s. id:%d"%(username,id))
            return id
        else:
            print("USER NOT FOUND")
            return -1
    
    def getGifsPages(self,username=None):
        id=-1
        if not username:
            if not self.username:
                print("Please provide a username")
                return None
            else:
                username=self.username
                id = self.id
        else:
            if username==self.username:
                id = self.id
            else:
                id = self.findUserID(username)

        if id>0:
            GIFS_PAGES = []
            current_link = "https://giphy.com/api/v3/channels/%d/gifs"%id
            GIFS_PAGES.append(current_link)
            while current_link:
                response = requests.get(current_link)
                data = response.json()
                next_link = data["next"]
                if next_link:
                    GIFS_PAGES.append(next_link)
                current_link = data["next"]
            return GIFS_PAGES
        else:
            return None

    def getGifs(self,username=None,max_pages=1):
        id=-1
        if not username:
            if not self.username:
                print("Please provide a username")
                return None
            else:
                username=self.username
                id = self.id
        else:
            if username==self.username:
                id = self.id
            else:
                id = self.findUserID(username)
                
        if id<0:
            return None

        count = 0
        page_link = "https://giphy.com/api/v3/channels/%d/gifs"%id
        api_data = []
        while page_link and (count<max_pages or max_pages == 0):
            response = requests.get(page_link)
            data = response.json()

            api_data.append(data)

            page_link = data["next"]
            count+=1
        return api_data

    def getGifsRawLinks(self,username=None,max_pages=1,extension="gif"):
        id=-1
        if not username:
            if not self.username:
                print("Please provide a username")
                return None
            else:
                username=self.username
                id = self.id
        else:
            if username==self.username:
                id = self.id
            else:
                id = self.findUserID(username)
                
        if id<0:
            return None
        if extension not in ["mp4","gif"]:
            raise ValueError("%s is not a valid extension\nYou can choose 'mp4' or 'gif'"%extension)
        if extension == "gif":
            extension="url"
        
        api_data = self.getGifs(username=username,max_pages=max_pages)
        
        GIFS_RAW_LINKS = []
        for page in api_data:
            results = page["results"]
            for result in results:
                gif_link = result["images"]["original"][extension]
                gif_id = result["slug"]
                gif_object = {"link":gif_link,"id":gif_id}
                GIFS_RAW_LINKS.append(gif_object)
        
        return GIFS_RAW_LINKS





