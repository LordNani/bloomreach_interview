FROM python:buster
COPY ./source /app/source
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python"]
CMD ["./source/main.py"]
