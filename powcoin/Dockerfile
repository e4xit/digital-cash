FROM python:3.7.0
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD mypowp2pcoin.py ./
ADD utils.py ./
ADD identities.py ./
<<<<<<< HEAD

CMD ["python", "-u", "mypowp2pcoin.py", "serve"]
=======
ADD mypowcoin.py ./

CMD ["python", "-u", "mypowcoin.py", "serve"]
>>>>>>> 4cfc12c17d01bd8ef0f1007d3ae141302aec6d19
