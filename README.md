# SETUP
## Project Setup

Install the python virtual environment
```bash
$ python3 -m pip install --user virtualenv
```

Create and run virtual environment.

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

To generate database tables run:
```bash
$ python manage.py migrate
```

## Run Tests

I used pytest library to write tests. 
To run the test run the following command on the terminal

```bash
$ pytest
```

# Running the application
To run the application, type the following command in the terminal
```bash
$ python manage.py runserver
```

## API Urls
I have used the django-extension library that provides helpful methods for debugging/development purposes.

To see API URLS
```bash
$ python manage.py show_urls | grep /api
```
***NB:- The urls shown will not include query params: For these endpoints please see the api test files for its implementation***

***Endpoints that use query params are :***
```python
/api/car_registry/car_price_mileage_range, query_params: name, start_price, max_price, start_mileage, max_mileage

/api/car_registry/search_car, query_params: make_name, model_name, submodel_name
```
