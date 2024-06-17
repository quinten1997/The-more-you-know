
# The More You Know

This project fetches the user's location and provides a fun fact about the area surrounding that location. It uses the Wikipedia API to obtain information about nearby landmarks and a free LLM API to format the facts nicely.

## Project Structure

- `backend/`: Contains the Flask backend application.
- `frontend/`: Contains the frontend application to fetch user's location and display fun facts.

```
The_More_You_Know
├─ README.md
├─ backend
│  ├─ .env
│  ├─ README.md
│  ├─ app.py
│  ├─ fetch_location.py
│  └─ requirements.txt
└─ frontend
   ├─ App.js
   ├─ README.md
   └─ package.json

```

### Backend

The backend is a Flask application that fetches nearby Wikipedia articles and formats the fun facts using a GPT-2 model.

#### Setup

1. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file** with your API keys and environment variables:
    ```
    WIKIPEDIA_API_URL=https://en.wikipedia.org/w/api.php
    ```

4. **Run the application**:
    ```bash
    python app.py
    ```

#### API Endpoint

- **GET /get_fun_fact**: Fetches a fun fact about nearby locations.
    - **Parameters**:
        - `lat` (required): Latitude of the user's location.
        - `lon` (required): Longitude of the user's location.
    - **Response**: A JSON object containing the fun fact.
        ```json
        {
            "fun_fact": "Did you know? 'Place Name' is located nearby at a distance of X meters."
        }
        ```

### Frontend

The frontend is a simple HTML file with JavaScript to fetch the user's location and display fun facts.

#### Setup

1. **Open http://127.0.0.1:5000/get_fun_fact?lat=52.302694&lon=4.567598 (you can change the lon and lat variables to adjust the location) in a web browser**.

2. **Click the "Get Fun Fact" button** to fetch a fun fact based on your location.
