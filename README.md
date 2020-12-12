# SETUP
## Project Setup

install python virtual environment
```bash
$ python3 -m pip install --user virtualenv
```

Create and run virtual environment

```bash
$ python3 -m venv registry_venv
$ source registry_venv/bin/activate
```

Install the dependencies
```bash
$ pip install -r requirements.txt
```

## Database and Environment Variables Setup
Create a database on your machine
Rename the `.env.example` to `.env`
Fill in the blank enviroment variables
```js
SECRET_KEY='8dfg+^o4nm4q=5ppj=3!ui+#3o7h-2=0@af*fj&rxaiwu)+%1f'
DATABASE_HOST=''
DATABASE_USER=''
DATABASE_PASSWORD=''
DATABASE_NAME=''
```
*SECRET_KEY has been provided for testing purposes only, Feel free to generate your own.*

To generate database tables run
```bash
$ python manage.py migrate
```

## Run Tests

I used pytest library to write tests. 
To run the test run the following command on the terminal

```bash
$ pytest
```