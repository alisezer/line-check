FROM python:3.7
RUN apt-get update && apt-get -y install cron

WORKDIR /usr/src/linecheck
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=line_check.py
COPY . ./
RUN chmod +x ./boot.sh

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]