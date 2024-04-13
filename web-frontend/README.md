# Web frontend - based on nginx

This container is required to run at all times that the feed is expected to be accessible.

To build and run:
' docker build -t typosquatting-livefeed-frontend .
' docker run -it -d -p 8000:80 --name typosquatting-livefeed-frontend -v path-to-feed-directory:/usr/share/nginx/html typosquatting-livefeed-frontend