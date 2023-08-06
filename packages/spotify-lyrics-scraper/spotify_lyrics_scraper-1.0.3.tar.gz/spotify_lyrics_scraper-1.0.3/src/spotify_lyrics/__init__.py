import requests, time

def getToken(sp_dc: str) -> dict:
    """
    Generates a Spotify Auth Token for searching lyrics/track IDs.\n
    To obtain the sp_dc, please check out https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc. This is required to have access to the lyrics API.

    Returns:
        dict - {"token": "x", "expiry": 0}\n
        dict - {"status": False, "message": "error message", "data": "data"}
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "App-Platform": "WebPlayer",
        "content-type": "text/html; charset=utf-8",
        "cookie": f"sp_dc={sp_dc}"
    }
    
    r = requests.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player", headers=headers)
    
    if r.json()["isAnonymous"] == False: return {"token": r.json()["accessToken"], "expiry": r.json()["accessTokenExpirationTimestampMs"]}
    else: return {"status": False, "message": "Error while trying to grab Spotify token.", "data": r.text}

def checkExpiry(info: dict) -> dict:
    """
    Check the expiry of your token.

    Arguments:
        info {dict} - Information (contains token and expiry)\n
    """
    if info["expiry"] > round(time.time()-3*1000): return {"expired": False}
    return {"expired": True}

def getLyrics(info: dict, trackId: str = None, songName: str = None, proxies: dict = {}) -> dict:
    """
    Search up lyrics of any given song. Uses trackId first over songName.

    Arguments:
        info {dict} - Information (contains token and expiry)\n
        trackId {string} - The track ID for the Spotify song to search up.\n
        songName {string} - The song name to search up.\n
        proxies {dict} - Supports Socks5 and HTTP/S, example: {"http": "http://1.1.1.1:80", "https": "https://1.1.1.1:443", "http": "socks5://1.1.1.1:443"}

    Returns:
        dict - {"status": False if error, True if success, "message": "Reason why/lyrics"}
    """

    if not trackId and not songName: return {"status": False, "message": "No data was provided to search up."}
    
    if "expiry" and "token" not in info: return {"status": False, "message": "The key 'expiry' or 'value' was not found in the info dict."}

    tempCheck = checkExpiry(info)
    if tempCheck["expired"] == True: return {"status": False, "message": "Cookie has expired."}

    if trackId:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
            "App-Platform": "WebPlayer",
            "Authorization": f"Bearer {info['token']}"
        }

        try: r = requests.get(f"https://spclient.wg.spotify.com/color-lyrics/v2/track/{trackId}?format=json&market=from_token", headers=headers, proxies=proxies)
        except Exception as e: return {"status": False, "message": f"Error occured: {e}"}

        if '"lines"' in r.text: return {"status": True, "message": r.json()}
        else: return {"status": False, "message": f"Could not find track/{r.text}"}

    if songName:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
            "App-Platform": "WebPlayer",
            "Authorization": f"Bearer {info['token']}"
        }

        try: r = requests.get(f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=searchDesktop&variables=%7B%22searchTerm%22%3A%22{songName.replace(' ', '+')}%22%2C%22offset%22%3A0%2C%22limit%22%3A10%2C%22numberOfTopResults%22%3A5%2C%22includeAudiobooks%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22130115162add6f3499d2f88ead8a37a7cad1d4d2314f3a206377035e7d26b74c%22%7D%7D", headers=headers, proxies=proxies)
        except Exception as e: return {"status": False, "message": f"Error occured: {e}"}

        try: trackId = r.json()["data"]["searchV2"]["tracksV2"]["items"][0]["item"]["data"]["id"]
        except Exception as e: return {"status": False, "message": f"Error occured: {e} - song doesn't exist?"}

        try: r = requests.get(f"https://spclient.wg.spotify.com/color-lyrics/v2/track/{trackId}?format=json&market=from_token", headers=headers, proxies=proxies)
        except Exception as e: return {"status": False, "message": f"Error occured: {e}"}
        if '"lines"' in r.text: return {"status": True, "message": r.json()}
        else: return {"status": False, "message": f"Could not find track/{r.text}"}