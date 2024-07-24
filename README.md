# Meteo Weather Application

Meteo is a web application where users can enter the name of a city and get the current weather forecast in that city.

## Features

- Get the weather forecast for any city.
- Autocomplete when entering the city name.
- Save search history for each user.
- On revisiting the site, users are prompted to view the weather in previously searched cities.
- API to show how many times each city has been searched.
- Tests written for key functionalities.
- Dockerized for easy deployment.

## Technologies

- **Framework:** Django
- **Weather API:** Open Meteo API
- **Autocomplete:** Geonames API
- **Containerization:** Docker

## Installation and Usage

**Clone the repository**

   ```sh
   git clone https://github.com/mcstao/weather.git
   ```

### Using Docker

1. Build and run the containers:

    ```sh
    docker-compose up --build -d
    ```

2. The application will be available at `http://127.0.0.1:8000/`.

### Without Docker

1. Ensure you have Python and pip installed.
2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```sh
    python manage.py migrate
    ```

5. Run the server:

    ```sh
    python manage.py runserver
    ```

66. The application will be available at `http://127.0.0.1:8000/`.

## Testing

Run tests with the following command:

```sh
python manage.py test
```


### Author
Adilet Anarbaev
