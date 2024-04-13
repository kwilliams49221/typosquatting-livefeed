# Python backend - refreshes the feed

This container only needs to be run each time the feed needs to be refreshed

To build and run:
' docker build -t typosquatting-livefeed-backend .
' docker run -it -d --name typosquatting-livefeed-backend -v <path-to-feed>:/root/feed/ typosquatting-livefeed-backend