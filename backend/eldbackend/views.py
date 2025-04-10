import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

def geocode_location(location, api_key):
    """Helper function to geocode a single location"""
    try:
        response = requests.get(
            'https://api.openrouteservice.org/geocode/search',
            params={
                'api_key': api_key,
                'text': location,
                'size': 1  # Only return the top result
            },
            timeout=10  # Add timeout to prevent hanging
        )
        response.raise_for_status()
        feature = response.json()['features'][0]
        return {
            'coordinates': feature['geometry']['coordinates'],
            'address': feature['properties']['label']
        }
    except Exception as e:
        logger.error(f"Geocoding failed for {location}: {str(e)}")
        raise

def get_route_directions(coordinates, api_key):
    """Helper function to get route directions"""
    try:
        response = requests.post(
            'https://api.openrouteservice.org/v2/directions/driving-car',
            headers={
                'Authorization': api_key,
                'Content-Type': 'application/json'
            },
            json={
                'coordinates': coordinates,
                'geometry': True,
                'instructions': False,
                'format': 'geojson'  # Standard format
            },
            timeout=15  # Longer timeout for route calculation
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Route calculation failed: {str(e)}")
        raise

@api_view(['POST'])
def calculate_route(request):
    try:
        # Validate input data
        required_fields = ['current', 'pickup', 'dropoff']
        if not all(field in request.data for field in required_fields):
            return Response(
                {'error': 'Missing required location data'}, 
                status=400
            )

        locations = [
            request.data['current'],
            request.data['pickup'],
            request.data['dropoff']
        ]
        
        # Geocode all locations
        geocoded = []
        for location in locations:
            result = geocode_location(location, settings.ORS_API_KEY)
            geocoded.append(result)
        
        coordinates = [loc['coordinates'] for loc in geocoded]
        
        # Get route
        route_data = get_route_directions(coordinates, settings.ORS_API_KEY)
        
        # Process results
        summary = route_data['features'][0]['properties']['summary']
        distance_km = summary['distance'] / 1000
        duration_hours = summary['duration'] / 3600
        
        return Response({
            'route': route_data,
            'waypoints': geocoded,
            'distance_km': round(distance_km, 2),
            'distance_miles': round(distance_km * 0.621371, 2),
            'duration_hours': round(duration_hours, 2),
            'duration_minutes': round(duration_hours * 60, 1),
            'raw_data': {
                'distance_meters': summary['distance'],
                'duration_seconds': summary['duration']
            }
        })
        
    except requests.exceptions.RequestException as e:
        logger.exception("API request failed")
        return Response(
            {'error': 'Routing service unavailable'}, 
            status=503
        )
    except Exception as e:
        logger.exception("Unexpected error in route calculation")
        return Response(
            {'error': 'Failed to calculate route'}, 
            status=500
        )