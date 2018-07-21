# Night Stalker
Webapp to analyse performance and progress by crawling the profile of users on different coding platfrom.

## Getting Started
### Prerequisites
Clone the project to local machine:
```
git clone https://github.com/singhsourabh/assessment.git
```
### Installing
Cd to the project directory and fulfil the requirements by:
```
pip install -r requirements.txt
```
Get RabbitMQ:
```
sudo apt-get install rabbitmq-server
```
## Usage

*Note two bash/terminals will be required to run the app.*

### BASH 1: ###

**Starting RabbitMQ and Celery tasks:**

Cd to the project directory.

```
sudo service rabbitmq-server start

celery -A assessment worker --loglevel=info
```

### BASH 2: ###

**Running django app:**

Cd to project directory and run the main app.

```
python manage.py runserver
```

**For login use the following details:**

*username : sourabh*

*password : qwerty123*
