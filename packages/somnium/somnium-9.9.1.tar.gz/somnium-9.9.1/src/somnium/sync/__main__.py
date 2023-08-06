import time
import requests
import json as jsons
from aiohttp import ClientSession, ClientTimeout
from html_telegraph_poster import TelegraphPoster

"""
Function
"""
#Get aiohttp
async def aioGet(url:str, headers=None, json=None, data=None, timeout=100):
	time_out = ClientTimeout(total=timeout)
	async with ClientSession(timeout=time_out) as session:
		async with session.get(url, headers=headers, json=json, data=data) as resp:
			return jsons.loads(await resp.text())

#Post aiohttp
async def aioPost(url:str, headers=None, json=None, data=None, timeout=100):
	time_out = ClientTimeout(total=timeout)
	async with ClientSession(timeout=time_out) as session:
		async with session.post(url, headers=headers, json=json, data=data) as resp:
			return jsons.loads(await resp.text())

#Post To Telegraph
async def PostTelegraph(title: str, html: str):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "Somnium"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=title,
        author=auth_name,
        author_url=f"https://pypi.org/project/somnium",
        text=html,
    )
    return post_page["url"]

#Custom Styles
async def CustomStyles():
    return await aioGet('https://raw.githubusercontent.com/Vauth/custom/main/styles.json')

"""
Class
"""
#Main class
class Somnium():
    """"Somnium class
    
    Somnium objects are responsible of Generating artworks & getting artstyles.
    
    Available options:
        - Styles(): --> list                 Get all art-styles list.
        - StylesGraph() --> url              Get all art-styles as UI.
        - Generate(prompt, style): --> url   Generate Artwork using prompt.
    Example:
        - Somnium.Generate('Girl', 2000) #Futurepunk V3
    """
    
    #Get All Styles
    @classmethod
    async def Styles(cls):
        r = await aioGet("https://paint.api.wombo.ai/api/styles")
        alls = {key:value['id'] for key, value in (await CustomStyles()).items()}
        alls.update({style["name"]: style["id"] for style in r if not style["is_premium"]})
        return alls

    #Get Styles UI As Telegraph
    @classmethod
    async def StylesGraph(cls):
        html = ''
        for i, b in (await CustomStyles()).items():
            html += f'<h2>{i}:</h2> <pre>{b["id"]}</pre><br/><img src="{b["image"]}">⁪⁬⁮⁮⁮⁮'
        for i in await aioGet("https://paint.api.wombo.ai/api/styles"):
            if i['is_premium'] == False:
                html += f'<h2>{i["name"]}:</h2> <pre>{i["id"]}</pre><br/><img src="{i["photo_url"]}">⁪⁬⁮⁮⁮⁮' 
        return await PostTelegraph('List Of ArtStyles', html)

    #Generate Art
    @classmethod
    async def Generate(cls, text: str, style: int):
        #FireBase
        s = requests.Session()
        API = "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"
        api_header = {"Content-Type": "application/json", "x-goog-api-key": API}
        api_json = {"appId": "1:181681569359:web:277133b57fecf57af0f43a", "authVersion": "FIS_v2", "sdkVersion": "w:0.5.1"}
        r = await aioPost("https://firebaseinstallations.googleapis.com/v1/projects/paint-prod/installations", headers=api_header, json=api_json)
        r2 = await aioPost(f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API}")
        Token = r2['idToken']
        
        #Headers
        headers = {
            'authority': 'paint.api.wombo.ai',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization': f'bearer {Token}',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://dream.ai',
            'referer': 'https://dream.ai/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
            'x-app-version': 'WEB-1.90.1',
        }
        
        # !! CustomStyles
        CuSt = await CustomStyles()
        
        #Custom Ids
        CustomIds = {value['id']:key for key, value in CuSt.items()}
        
        #Custom Ifs
        if int(style) in CustomIds.keys():
            textQ = (CuSt[CustomIds[int(style)]]['prompt']).replace('{PROMPT}', text)
            styleQ = int(CuSt[CustomIds[int(style)]]['style']) #Poster Art (Changable)
        else:
            textQ = text
            styleQ = style
        
        data = {
            "is_premium": False,
            "input_spec": {
                "prompt": textQ,
                "style": styleQ,
                "display_freq": 10
            }
        }
        
        gen_response = await aioPost('https://paint.api.wombo.ai/api/v2/tasks', headers=headers, data=jsons.dumps(data))

        try: 
            image_id = gen_response["id"]
            for i in range(10):
                response = await aioGet(f'https://paint.api.wombo.ai/api/v2/tasks/{image_id}', headers=headers)
                if response['state'] == "failed":
                    return None
                    break
                time.sleep(3)
                try:
                    img = response["result"]["final"]
                    return img
                    break
                except:
                    continue
        except Exception as e:
            return None
