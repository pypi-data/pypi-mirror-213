import requests

def id_scrape(username):
    url = f"https://www.instagram.com/{username}"
    try:
    	req = requests.get(url).text
    	if 'props":{"id":"' in req:
    	   user_id = req.split('props":{"id":"')[1].split('"')[0]
    	   return user_id
    	else:
    		return 'Bad UserName'
    except:
    	return 'Bad Request'