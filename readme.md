# SkyNexus: Comprehensive Weather and Geolocation API

SkyNexus is a robust, Django-based API providing comprehensive weather data, including real-time conditions, forecasts, and historical weather insights, along with geolocation services. Designed specifically for developers, SkyNexus allows seamless integration of weather and location-based functionalities into web and mobile applications.

## Features

- **Real-Time Weather**: Obtain current weather information based on city names or geographic coordinates.
- **Weather Forecasts**: Access short-term weather predictions for targeted planning.
- **Historical Weather Data**: Retrieve past weather records, useful for trend analysis and data science applications.
- **Geolocation Services**: Convert city names into geographic coordinates and vice versa.
- **Developer-Friendly Endpoints**: Clean, JSON-formatted responses designed for smooth integration.
- **Secure Access Controls**: Token-based authentication and rate limiting for secure and controlled API usage.

## Getting Started

### Prerequisites

To use SkyNexus, you’ll need the following:

- **Python** (version 3.8 or higher)
- **Django** (version 3.2 or higher)
- **Django REST Framework**
- An external weather API key (e.g., from [OpenWeatherMap](https://openweathermap.org/))

### Installation

1. Clone the repository and navigate into the project directory:

   ```bash
   git clone https://github.com/Elabs-llc/capstone.git
   cd skynexus

2.  Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Django environment and migrate the database:

   ```bash
   python manage.py migrate
   
5. Run the development server to test the API locally:

    ```bash
   python manage.py runserver
   

## Usage

To interact with the API, use the endpoints listed below. Note that some endpoints may require an authentication token.

### Example Endpoints

- **Home Page**: Displays the main form and weather data.
  - **URL**: `/`
  - **Method**: `GET`
  - **Purpose**: Loads the homepage where users can view and interact with the main weather form.

- **Weather Details**: View detailed weather information for a specific entry.
  - **URL**: `/weather/<int:skydata_id>/info/`
  - **Method**: `GET`
  - **Parameters**: `skydata_id` (integer) — Unique identifier for the specific weather data entry.
  - **Purpose**: Displays detailed information for a particular weather data record.

- **Weather Information View**: Render the weather information based on session data.
  - **URL**: `/weather/view/`
  - **Method**: `GET`
  - **Purpose**: Loads weather data from the session for viewing.

- **Save Weather Data**: Save new weather data.
  - **URL**: `/weather/save/`
  - **Method**: `POST`
  - **Purpose**: Saves new weather data to the database, typically through a POST request with form data.

- **Fetch Weather Data**: Retrieve weather data from an external API.
  - **URL**: `/weather/fetch/`
  - **Method**: `GET`
  - **Purpose**: Fetches weather data from an external source and displays it.

- **API Endpoints**: SkyNexus API endpoints for weather and location services.
  - **URL Prefix**: `/api/`
  - **Included Routes**: The `skydata.api_urls` file will contain the full list of API endpoints for real-time, forecast, and historical weather data as well as geolocation.

### Sample Requests

To fetch real-time weather data:
```bash
curl -X GET "http://localhost:8000/weather/fetch/" -H "Authorization: Bearer <YOUR_TOKEN>"
```


## Project Structure

``` bash
skynexus/
├── skynexus/
│   ├── settings.py        # Project configuration, including API keys and other settings
│   ├── urls.py            # Main URL routing
│   ├── ...
├── static/
│   ├── css/
│   │   └── style.css      # Styling for the weather app
├── skydata/
│   ├── templates/         # Contains template files for weather views
│   ├── __init__.py        # Package initializer
│   ├── admin.py           # Weather app admin configuration
│   ├── api.py             # Core API logic and integrations for weather data
│   ├── api_urls.py        # URL routing for API endpoints
│   ├── apps.py            # App configuration
│   ├── cities.txt         # Data file with city information for geolocation
│   ├── models.py          # Models for caching and storing weather data
│   ├── serializers.py     # Serializes data into JSON format
│   ├── tests.py           # Unit tests for weather app functionality
│   ├── urls.py            # URL routing for weather and geolocation endpoints
│   ├── views.py           # Handles API requests for weather and location data
│   └── weather_<other_files> # Additional weather-related files
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation


