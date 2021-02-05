FROM python:3.7

COPY . nesi
WORKDIR nesi
RUN python -m pip install requirements.txt

ENTRYPOINT ["./restapi.sh", "--keep-running", "--recreate-db"]