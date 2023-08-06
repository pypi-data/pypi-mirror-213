# Spotify Lyrics Grabber
This Spotify Lyrics Grabber is a tool to grab Spotify Lyrics of any song, not just the one you are listening to.

**Table of Contents**

- [Installation](#installation)
- [Examples](#examples)

### Installation
To install, run `pip install spotify-lyrics-scraper` in your command prompt. To import it, I recommend `import spotify-lyrics-scraper as spotify`

### Examples
- Always using: `import spotify-lyrics-scraper as spotify`
- To obtain the sp_dc, please check out https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc. This is required to have access to the lyrics API.
##### Example 1
```
token = spotify.getToken("SP_DC Here")
print(spotify.getLyrics(token, songName="Song"))
```

##### Example 2 (Proxies)
```
token = spotify.getToken("SP_DC Here")
print(spotify.getLyrics(token, songName="Song", proxies={"https": "https://1.1.1.1:443"}))
```