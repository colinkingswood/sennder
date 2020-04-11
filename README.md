# sennder
technical test

Developed using Linux Mint, with Python 3.6

Create a virtual environment with python 3.6 
There are different options for this, command I used was: 

> python3 -m venv sender_venv

activate the vitural environment
> . sender_venv/bin/activate

Download the repository. 
'cd'  to the top level sennder folder, the same place where manage.py is located
> cd sennder

install the dependencies into our virtual environment
> pip install -r requirements.txt

Optionally set the django setting moudle with (the default settings module should work): 
> export DJANGO_SETTINGS_MODULE=sennder.settings 

start the development server
> python manaye.py runserver

Then you should be able to see the move list at:
http://127.0.0.1:8000/movies/
