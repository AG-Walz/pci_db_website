# pull official base image
FROM python:3.10.5

# set work directory
WORKDIR /usr/src/immuno_db_app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install net-tools
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    netcat \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/immuno_db_app/entrypoint.sh
RUN chmod +x /usr/src/immuno_db_app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/immuno_db_app/entrypoint.sh"]
