FROM python:3.8.5

COPY . nesi
WORKDIR nesi
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["python3", "cli.py", "--standalone", "Alcatel", "--box-uuid", "alcatel"]