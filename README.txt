Run App.py with commandline arguments of path to csv file

ex. $ python App.py 'resources/A.csv'


For Web:

env:
    - python ver: 3.7.2
    - pip ver: 18.1
    - package: django-webpack-loader (pip install django-webpack-loader) 

    - node ver: 10.15.1
    - npm ver: 670

to run (in '/webapp' directory):
    - npm install
    - npm run build
    - python manage.py collectstatic
    - python manage.py runserver

input file in '~/webapp/webapp/backend/resources/toWeb.csv' dir. (replace and rename)
output file in '~/webapp/webapp/backend/resources/toWeb.json' dir.