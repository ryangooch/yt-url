# yt-url
python utility for searching youtube from the terminal

I find that sometimes I want to share a video URL that I happen to have watched on another device,
or perhaps that I have recently watched but which isn't on an active tab.

Enter `yt-url`!

Simply run this from the terminal and get your URL for your search string!

Caveats:
* this is a for-fun project that handles a random and specific need that I've had
* it probably won't be actively maintained or updated
* it YOLO's your search; you only get the first result which may or may not be correct!
    * "I'm feeling lucky"

Usage:

```bash
$ python yt-url.py "the burnout society | unsolicited advice"

> https://www.youtube.com/watch?v=vBmc40_-vo0
```

I tend to use this by piping it to `pbcopy` to get it into my clipboard, like this:

```bash
$ python yt-url.py "the burnout society | unsolicited advice" | pbcopy

```

