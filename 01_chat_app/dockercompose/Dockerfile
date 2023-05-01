FROM python:3.11.3-alpine
ADD ./flask/ /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
