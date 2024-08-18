import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

NASA_API_KEY = "DEMO_KEY"  # Replace with your actual NASA API key
NASA_API_URL = "https://api.nasa.gov"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Fetch Astronomy Picture of the Day (APOD)
    apod_response = requests.get(f"{NASA_API_URL}/planetary/apod", params={"api_key": NASA_API_KEY})
    apod_data = apod_response.json()

    # Fetch Mars Rover Photos
    rover_response = requests.get(f"{NASA_API_URL}/mars-photos/api/v1/rovers/curiosity/photos",
                                  params={"api_key": NASA_API_KEY, "sol": 1000})
    rover_data = rover_response.json().get("photos", [])

    # Fetch Images from the NASA Image and Video Library
    library_response = requests.get(f"{NASA_API_URL}/search", params={"q": "moon", "media_type": "image", "api_key": NASA_API_KEY})
    
     # Print the response text for debugging
    print(library_response.text)  # This will show you the raw response content in the console
    
    if library_response.status_code == 200:
        try:
            library_data = library_response.json()
        except requests.exceptions.JSONDecodeError:
            library_data = {"error": "Invalid JSON response"}
    else:
        library_data = {"error": f"Failed to retrieve data, status code: {library_response.status_code}"}

    # Fetch EPIC (Earth Polychromatic Imaging Camera) images
    epic_response = requests.get(f"{NASA_API_URL}/EPIC/api/natural/images", params={"api_key": NASA_API_KEY})
    epic_data = epic_response.json()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "apod_data": apod_data,
        "rover_photos": rover_data,
        "library_data": library_data,
        "epic_data": epic_data,
    })
