FROM python:3.7

COPY . nesi
WORKDIR nesi
RUN python3 -m pip install -r requirements.txt

RUN chmod +x ./bootup/restapi.sh

ENTRYPOINT ["./bootup/restapi.sh", "--keep-running", "--recreate-db"]