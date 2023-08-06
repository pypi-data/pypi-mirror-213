# Spotify Lyrics Grabber
This basic Python Module allows you to grab Spotify Lyrics from their API. You can input Song Names or input a Track ID and it will return with the pure lyrics JSON (including timings).

Code Example:
```
import spotify-lyrics-scraper as scraper

token = scraper.getToken("SP_DC Here")
#To obtain the sp_dc, please check out https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc. This is required to have access to the lyrics API.

print(scraper.getLyrics(token, songName="Never Gonna Give You Up"))
```