# FROM gw000/keras:2.1.4-py3-tf-cpu
FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    python-matplotlib \
    python-pillow

RUN mkdir /code



WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/

EXPOSE 8000
CMD ["python", "manage.py", "runserver" , "0.0.0.0:8000"]