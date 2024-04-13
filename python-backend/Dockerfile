FROM ubuntu:latest
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip install dnstwist
RUN pip install dnspython
COPY app.py /root/app.py
CMD [ "python3",  "/root/app.py" ]