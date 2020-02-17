# Django API Template

**Building project**

`docker-compose build`

**Running Tests**

`docker-compose run app sh -c 'python manage.py test && flake8'`

**Create SuperUser**

`docker-compose run app sh -c 'python manage.py createsuperuser'`

**Run Local Server**

`docker-compose up`