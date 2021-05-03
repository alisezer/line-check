# line-check
Line Check Call Scheduler

This project can be used for scheduling calls(tasks) to the line disruption endpoint of the TFL API.

### Set-Up

- Uses Python 3.7
- Pipenv is used, but can also be used with virtual envs (req.txt included)
- Docker compose is provided for an easy set up
- Uses Postgre 12 for DB

To start with a basic set up, you can either install the environment using pipenv or the classic virtual envs way.

```
pipenv install
pipenv shell
```

or

```
virtualenv venv
source venv bin activate
pip install -r requirements.txt
```


### Launching the Full System with Docker Compose

This should be the easiest way to get everything started at the same time. The tasks it will carry out for you are:

- Launching a Postgre DB
- Migrating to the DB
- Launching the API
- Setting up the cron job within the API's container for the scheduler
- Exposing the API on localhost port 8000.
- Exposing the DB on port 5442 for manual inspection. (Left the 5432 untouched to avoid clashing with a local PSQL intance)

To do all these steps, you can run the following command:

```
docker compose up --build
```

### Running Tests

Tests are handled through pytest. You can run both in regular or coverage mode.

You will need a running instance of the database before you can run the tests. Some of the tests are actually testing how the API interracts with the DB (read/writes).

For this, first you will need to run:

```
docker compose up database
```

and then the pytest command

```
pytest tests
```

or for with coverage

```
pytest tests --cov
```

### Running the Application without using Docker

If you would like to run the application without using docker, you will need to follow a few more steps to take care of some of the requirements.

Basically, when you spin up a fresh DB, it wont have the necessary tables. So you will need to run the migration scripts.

Also, if you want the scheduler to work, you will need to set up a crontab on your computer. This step might be a bit cumbersome locally, so using the docker container is advised, but you can do it non the less. However, if you choose not to, the only component that won't be functioning properly will be the scheduler bit (checking task's times and making a request accordingly.) You can test whether if the scheduler function is working (not the scheduler it self) using the Flaks's CLI.

If you are going to be using the docker compose generated DB, before you proceed, you should create a .env file on the project directory, and set the DB PORT to 5442:

```
DB_PORT=5442
```

This step is necessary since docker compose will be exposing the DB on port 5442 rather than the standard 5432.

If you are going to be using a totally external DB, you can adjust the env vars by using the `.env.template`

Steps to be followed: (This part assumes that you have the venv activated)

```
export FLASK_APP=line_check.py
flask deploy
gunicorn -c gunicorn.py line_check:app

# To run the scheduler function
flask scheduled
```

For setting up the crontab, you can check out to crontab file and add it to your local system by adjusting the paths. However, once again, leaving that to the docker container might be the better option.

### Tweaking the Application Configurations
All of the configuration changes that you can do to the application can be set by via env vars. To see the list of configurable vars, please see the `.env.template`

The first group is related to configuring the DB: if you wanted to point to a real one you would need to change those..

The second group is related to Gunicorn. Workers and Threads can be changed with ease, depending on the node/machine you are planning on deploying the app to.

Port might be a bit more complicated, and will require and update on the dockerfile.


### Configuring Application for Production Like Environment
The environment variables that will be injected to the docker container will be picked up by the application. You can use this functionality while deploying your containers.

### Endpoints

Endpoints are formed inline with the description:

To get all tasks:

```
GET REQUEST: {{host}}/v1/tasks
curl -X GET http://localhost:8000/v1/tasks
```

To get a single task:

```
GET REQUEST: {{host}}/v1/tasks/task-id-as-int
curl -X GET http://localhost:8000/v1/tasks/1
```

To create a task:

```
POST REQUEST {{host}}/v1/tasks
curl -X POST \
  http://localhost:8000/v1/tasks/ \
  -d 'schedule_time=2021-05-03T13%3A20%3A00&lines=central'
```

To update/edit a task:

```
PUT REQUEST {{host}}/v1/tasks/task-id-as-int
curl -X PUT \
  http://localhost:8000/v1/tasks/1 \
  -d 'lines=bakerlo&schedule_time=2021-06-05T18%3A00%3A00'
```

### The Scheduler

While building this up, I did a fair bit of research since there are many ways to build such a thing. The options I have considered were:

1. Homegrown background thread running every x seconds and sleeping afterwards
2. APScheduler: Python scheduling library
3. Cronjob: Building a basic CLI interface and attaching it to the cron functionality.

Other more complex options could have been using something like Celery or Airflow, but I think that would have been an over kill.

I chose to use the Cronjob option after my research. This method was suggested by Miguel Grinberg in one his blogs. I like his pragmatic and minimalist solutions to problems, and what he explained made sense to me so I thought I would try it out. I combined his solution with dockerized crontab solutions to build what we have here. Some references I used:

- https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron
- https://github.com/Ekito/docker-cron/blob/master/Dockerfile
- https://stackoverflow.com/questions/27771781/how-can-i-access-docker-set-environment-variables-from-a-cron-job
- https://stackoverflow.com/questions/61629731/how-can-i-run-a-python-code-with-cron-in-a-docker-container

Previously, in an commercial environment I created my own thread (something like option 1). It was an interesting usecase and I learnt a lot about schedulers by doing that, however to create a robust one takes some time becasue you have to be very careful about the way you form your threads, how they enter and exit with respect to the application and how they handle errors.

I have also researched about the APScheduler, it seemed quite straightforward but I wasn't sure how it would have behaved in a multiple worker/thread environment, and using that also meant managing the flask context continously..

Some drawbacks of the cronjob based scheduler:

- The most frequent timing you can have is every minute. For an application as such, it shouldn't be a huge problem, but in other cases you might want to have a scheduler that can check more often (maybe every second)
- Monitoring is not very straight forward, to monitor it, I created a schedule.log file which is can be used with a tail command, but you need to ssh into the docker container first.
- It handles errors well, it wont crash the application in any way possible since it relies on a CLI to run, however, it also hides the errors very well :D.. If you dont check the logs, you cannot figure out whether if the scheduler is running or not.
- You need to export the env variables through an extra step
- Forming the dockerfile is not as easy, you need extra steps to install cron, configure and then run it. Also installing cron increases your container size, might not be preferable in a multi container scenario..
- You cannot have multiple containers running at the same time, pointing towards the same DB since they will start getting into race conditions.

Some steps you can follow to monitor the scheduler once you have the docker compose runing:

```
docker exec -it [container-id] /bin/bash
tail -f scheduled.log
```

### Improvments Needed

I couldn't get to do everything I wanted to do within the given timeframe, however I'm aware of some points which can be improved:

1. Need to add authentication - as specified in the description
2. Need much better argument parsing/checking: At the moment, there is close to none argument checking in the API endpoints. This needs improvment and can be done using a module like webargs.
3. Endpoint status code returns: Right now, the status code returned from the endpoints do not really match with the messages all the time. Sometimes, if a resource cannot be found or created for some reason, the API might still return a 200 OK. This needs changing..
4. Tests: Some negative cases are not tested as well as bad argument passing. For example, passing on an incorrect line name and how it will be returned as a response is not tested, as well as well incorrect data types.


### Final Words

Many thanks for taking the time to go over this project, had quite fun while building it up and hope it does a well job living up to your standards!
