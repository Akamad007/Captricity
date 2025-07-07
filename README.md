# Captricity

This project now requires **Python 3.12**.
 
Current System
 
1. A user can create an account and login. 
2. A user can create, update and delete images. 
3. A user can see thumbnails and a detailed image. A user can browse through the 
images 
4. A user can add text for each image. The text does not allow any scripting or html 
content to be added. Django's csrf protection mechanism does not allow cross site 
forging to occur.  
5. Every user can see only their own images. 
6. A user can upload images to Captricity and the system keeps a record of the batch as 
well as the images uploaded to the batch.  
7. A user can see all the previous batches created and the images in each batch. 
8. A user can see the data derived from the digitization of each image uploaded to a 
particular batch. 
9. There is a celery task which uploads each active image in the system to Captricity 
every 30 min. 
10. The system queries for the digitized data and displays it to the user. This data is 
stored in the system for future reference. 
11. The system queries Captricity every 30 min for completed digitized data and informs 
the user via Email.  
 
Installation
 
The following tools are needed for the installation and working of this application.  
Install Python 3.12 and pip (the Python package manager).
Using pip3 install the following packages or run `pip3 install -r requirements.txt`.
Django==5.2.1
celery==5.5.3
django-celery-email==3.0.0
django-debug-toolbar==5.2.0
django-redis==5.4.0
django-reset==0.2.0
redis==6.2.0
 
Make sure you have the latest redis server instance running on the default port. We are using 
redis as the messaging queue. Celery is being used to run asynchronous tasks.  
 
 
 Working

To start the application open terminal. 
Make sure all the packages are installed using pip3.
Go in the application folder. Run the command “python3 manage.py runserver “
This will start the application.  
Start a new terminal tab. Run the command “python3 manage.py celery beat”
This command will start the celery periodic scheduler. This command queues all the 
celery periodic tasks. 
7. Start a new terminal tab. Run the command “ python3 manage.py celery worker”
8. This command starts the celery worker and will start executing the tasks queued in the 
celery scheduler. 
9. You can start using the application by going to the link localhost:8000.

## Running Tests

To run the test suite with code coverage enabled execute:

```bash
coverage run manage.py test
coverage report
```
