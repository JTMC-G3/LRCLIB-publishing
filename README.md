# LRCLIB-publishing
A repo to demonstrate publishing lyrics to lrclib synced 

the following is copied from my private repo about publishing to LRCLIB

# Start

as of feb 27 LRCLIB is faster now and so much cool and fun to publish lyrics and such
publish.py is my full publishing code, simply get a synced.json and a lyrics.txt and it will auto format
lyrics.txt should be just a normal txt file with each new lyric being on a new line
synced.json is special, it should be formatted as so
```
{
  "type": "synced",
  "lines": [
    {
      "time_ms": 7066,
      "text": "Ayy, uh"
    },
  ]
}
```
full demonstration of a proper synced.json in the repo 
you can also just use sync.py and go to localhost:5000 and upload the song and lyrics and manually sync it (by clicking space and such)


P.S. all code is practically claude, coding at school when i just want to listen to music sucks, so im lazy.


# Step by step for syncing lyrics
If you already have a valid lyrics.txt and a valid synced.json (generated from sync.py) Skip straight to step by step for publishing lyrics

1. get a lyrics.txt file, each new line is a new lyric. simple
2. get the song mp3, i dont care how you get it just retrieve it, dont use music videos or lyric videos, usually just download it from soundcloud or the youtube "Topic" thing
3. run the python file "sync.py" and open http://localhost:5000 in your browser 
4. Upload the mp3 and lyrics.txt
5. Start syncing, hit space whenever a lyric occurs, pretty simple
6. After all lyrics are synced, click export json and then a synced.json will be saved to your file system (it will also be downloaded, simply rename it if you cant find the synced.json)
7. You are ready to continue to publishing

# Step by step for Publishing lyrics
1. With your valid lyrics.txt and synced.json place it in the same folder with publish.py, getchallenge.py, and getpublishtoken.py
2. Fill out all the field in publish.py at the top, duration in seconds
3. Run publish.py and wait,
4. Now retrieve your lyrics in whatever means necessary, i have provided a search.py to check if its published correctly, though since im lazy the synced lyrics dont get retrieved but "Has Synced Lyrics" will be true


# Be a good person

Dont use this to publish fake lyrics or slurs or bad things onto random songs, be nice, i dont want to have to take this repo down
I've published a total of like 6 or 7 (hilarious) songs onto lrclib and its fun. so be nice



# Original LRCLIB 
lrclib created and contributed to by:
@tranxuanthing
@DataM0del
@jodacame
@MJWcodr

[lrclib](https://github.com/tranxuanthang/lrclib)

Thanks
