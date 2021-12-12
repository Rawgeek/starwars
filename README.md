# Starwars Characters Explorer

App which allows you to collect, resolve and inspect information about characters
in the Star Wars universe from the [SWAPI](https://swapi.co/api/people/)

## Setup
```
node@17.0.1
python@3.9.7
```

### Install:
* [nvm](https://github.com/nvm-sh/nvm)
* [pyenv](https://github.com/pyenv/pyenv)
* [pipenv](https://pipenv.readthedocs.io/en/latest/)

```
$ git clone git@github.com:rawgeek/starwars.git
$ cd starwars
$ nvm install
$ npm install
```

If you wish to only generate a fresh front-end build, run:
```
$ npm run build
$ cd ..
```

To run in front-end in development mode, run (currently isn't working correctly for :8000 port, use port :8080):
```
$ npm start
```
Open new terminal and continue below


### If on Mac OS X Mojave:
```
CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install
```
### Else:
```
$ pyenv install
```

### Next:
```
$ pipenv install --dev
$ pipenv shell
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver

```

Go to http://localhost:8000 for user view and http://localhost:8000/admin/ for admin view

## Unit Tests
```
$ python manage.py test
```

## TODO / Known Issues

