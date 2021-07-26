# edziekanat

Deployment

run pip install -r requirements.txt

To start local server use command: heroku local web 

To compile scss files use command:

sass --watch djangoProject/assets/scss/style.scss:djangoProject/assets/css/style.min.css --style compressed

To collect static files use command: python manage.py collectstatic