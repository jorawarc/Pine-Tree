FROM python:3.9

COPY ./src /discord
WORKDIR /discord

RUN python -m pip install -r requirements.txt
CMD ["python", "main.py"]