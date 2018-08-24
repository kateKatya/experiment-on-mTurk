# Website for experiments on mTurk

---
## Intro
An example website that is built to run an experiment on Amazon Mechanical Turk using the Django framework. Includes an example of a quiz and an example of trials generated on-the-go, based on the user's responses. Django is nicely supported by PyCharm (professional version is free for [students](https://www.jetbrains.com/student/)). Django project is in the experimentsite folder.

If deployed locally, you can access the website via http://127.0.0.1:8000/amt/?amt=debug and otherwise - http://yourhost/amt/?amt=debug

---
## Useful Sources
* Django installation: [Version 2.1](https://docs.djangoproject.com/en/2.1/intro/install/)
* A good intro to Django: [First tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/)
* Bootstrap instructions: [W3Schools tutorials](https://www.w3schools.com/bootstrap/default.asp)
* Highcharts demos: [Simple graphs](https://www.highcharts.com/demo)

---
## Useful Commands:
* `python manage.py runserver` - starts the server, you need to be in the experimentsite folder
* `python manage.py startapp newappname` - starts a new app with the name "newappname"
* `python manage.py makemigrations newappname` - activate the models created
* `python manage.py migrate` - create those model tables in your (default - SQLite) database
* `python manage.py shell` - to open a shell for Django API
* `python manage.py createsuperuser` - to create an admin user (see more [here](https://docs.djangoproject.com/en/2.1/intro/tutorial02/#introducing-the-django-admin))

---
## Deploying on pythonanywhere.com
* There is a simple guide on how to [deploy an existing project](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject)
* You will need to [create a virtual environment](https://help.pythonanywhere.com/pages/VirtualEnvForNewerDjango) to have the newer version of Django running (and install all the modules needed)
* There is a trick to make all your [static files sync correctly](https://help.pythonanywhere.com/pages/DjangoStaticFiles) (if doesn't work from the box)
* Finally, don't forget to edit wsgi.py and add your website domain to allowed hosts in settings.py


---
## Good to know
* The example website is set to show 3 chain with 4 steps - that can be edited in code, but note that you have to edit both utils.py, nodels.py and instructions.html, trials.html and completed.html (or implement a centralised settings file)
* Experiment settings can assign the function type (linear, quadratic, exp 2.1 or exp 1.8) and the initial weights for the three chains
* Majority of experiment-related settings are in utils.py
* You can edit settings, add and/or edit questions for the quiz, view and download your participants' data as csv from the admin interface (yourhost/admin)
* Settings are at the website-level (not participant-level). This can be easily changed, as the type of function is stored by the Participant class too
