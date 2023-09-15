FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# add an 'app' user
ENV HOME=/home/app
RUN addgroup app && adduser --home $HOME --ingroup app --disabled-password app

# create directories
ENV APP_HOME=/home/app/web/
RUN mkdir $APP_HOME
RUN chgrp -R app $APP_HOME
RUN chmod -R 770 $APP_HOME
WORKDIR $APP_HOME
# entrypoint needs 'nc' command.. install it
RUN apt-get update && apt-get install -y netcat cron

# copy the app and install dependencies
COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt
COPY src $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app


ENTRYPOINT ["/home/app/web/entrypoint.sh"]
