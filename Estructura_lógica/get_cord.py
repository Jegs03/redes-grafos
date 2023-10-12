import requests
import json
def get_url_contents(url):
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def lon_lat2cord(lon,lat):
    # Example usage:
    url = f"https://epsg.io/trans?x={lon}&y={lat}&z=0&s_srs=4326&t_srs=3116&callback=json"
    contents = get_url_contents(url)
    centro_bogota=(2764610.9415263887, -9152155.70237988)
    if contents:
        x=contents[5:-1]
        cor= json.loads(x)
        return (float(cor['x'])-centro_bogota[0],float(cor['y'])-centro_bogota[1])
    else:
        return None
    




