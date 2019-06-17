import requests
import json
import steam.webauth as wa
import time
import re

def ActivateKey(keys):
    for key in keys:
    	r = user.session.post('https://store.steampowered.com/account/ajaxregisterkey/', data={'product_key' : key, 'sessionid' : sessionID})
    	blob = json.loads(r.text)
    
    	# Success
    	if blob["success"] == 1:
    		for item in blob["purchase_receipt_info"]["line_items"]:
    			print("[ Redeemed ]", item["line_item_description"])
    	else:
    		# Error codes from https://steamstore-a.akamaihd.net/public/javascript/registerkey.js?v=qQS85n3B1_Bi&l=english
    		errorCode = blob["purchase_result_details"]
    		sErrorMessage = ""
    		if errorCode == 14:
    			sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'
    
    		elif errorCode == 15:
    			sErrorMessage = 'The product code you\'ve entered has already been activated by a different Steam account. This code cannot be used again. Please contact the retailer or online seller where the code was purchased for assistance.'
    
    		elif errorCode == 53:
    			sErrorMessage = 'There have been too many recent activation attempts from this account or Internet address. Please wait and try your product code again later.'
    
    		elif errorCode == 13:
    			sErrorMessage = 'Sorry, but this product is not available for purchase in this country. Your product key has not been redeemed.'
    
    		elif errorCode == 9:
    			sErrorMessage = 'This Steam account already owns the product(s) contained in this offer. To access them, visit your library in the Steam client.'
    
    		elif errorCode == 24:
    			sErrorMessage = 'The product code you\'ve entered requires ownership of another product before activation.\n\nIf you are trying to activate an expansion pack or downloadable content, please first activate the original game, then activate this additional content.'
    
    		elif errorCode == 36:
    				sErrorMessage = 'The product code you have entered requires that you first play this game on the PlayStation®3 system before it can be registered.\n\nPlease:\n\n- Start this game on your PlayStation®3 system\n\n- Link your Steam account to your PlayStation®3 Network account\n\n- Connect to Steam while playing this game on the PlayStation®3 system\n\n- Register this product code through Steam.'
    
    		elif errorCode == 50: 
    			sErrorMessage = 'The code you have entered is from a Steam Gift Card or Steam Wallet Code. Browse here: https://store.steampowered.com/account/redeemwalletcode to redeem it.'
    
    		else:
    			sErrorMessage = 'An unexpected error has occurred.  Your product code has not been redeemed.  Please wait 30 minutes and try redeeming the code again.  If the problem persists, please contact <a href="https://help.steampowered.com/en/wizard/HelpWithCDKey">Steam Support</a> for further assistance.';
    		
    		print("[ Error ]", sErrorMessage)

def CheckNew(subreddit):
    time.sleep(1) #Reddit api has 1 second request buffer :V
    url = requests.get('https://old.reddit.com/r/'+subreddit+'/new.json?sort=new', headers = {'User-agent': 'MrMeetSteaks'})
    obj = url.json()
    
    texts=[] #selftext
    #images=[] #url, check for .jpg, .jpeg, .png then use text reading lib to check for keys
    #urls=[] #permalink
    
    keychecks = ["[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+","[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+"]
    
    x = []
    
    for ch in obj["data"]["children"]:
        texts.append(ch["data"]["selftext"])
        #images.append(ch["data"]["url"])
        #urls.append(ch["data"]["permalink"])
        
    for text in texts:
        for check in keychecks:
            x.append(re.findall(check,text))
            
    z = x[0] + x[1]
        
    print("Checked: r/"+subreddit)
    print(z)
    ActivateKey(list(filter(None, z)))

def ScrapeForKeys():
    x = ["pcgaming","gaming","steam_giveaway"]
    for sub in x:
        CheckNew(sub)
        
user = wa.WebAuth("USERNAME","PASSWORD")
user.login()
sessionID = user.session.cookies.get_dict()["sessionid"]
        
while True:
    ScrapeForKeys()
    time.sleep(60)