FROM python:3.8

#maintainer
LABEL Author="abdoufermat"

RUN apt-get update -y
RUN apt-get upgrade -y
# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
#switch to /app directory so that everything runs from here
RUN apt install -y netcat \
    && apt-get update
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip
RUN pip3 install ez_setup
WORKDIR /usr/src/test_backend
COPY requirements.txt .

RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/test_backend/entrypoint.sh
RUN chmod +x /usr/src/test_backend/entrypoint.sh
#copy the app code to image working directory
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/test_backend/entrypoint.sh"]

