import googlemaps
import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import os
from travel_planner import TravelPlannerWorkflow

@dataclass
class RouteInfo:
    """Data class for route information"""
    start_location: str
    end_location: str
    distance: str
    duration: str
    steps: List[str]

class GoogleMapsRoutePlanner:
    """
    Route Planner using Google Maps API
    
    This class handles calculating optimal routes through multiple locations
    using the Google Maps Directions API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the route planner with Google Maps API key
        
        Args:
            api_key: Google Maps API key
        """
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)
    
    def geocode_location(self, location_name: str, context: str = "University of Pennsylvania, Philadelphia, PA") -> Tuple[float, float]:
        """
        Convert location name to coordinates using geocoding
        
        Args:
            location_name: Name of the location
            context: Additional context to help with geocoding
            
        Returns:
            Tuple of (latitude, longitude)
        """
        try:
            # Add context to improve geocoding accuracy
            full_query = f"{location_name}, {context}"
            
            geocode_result = self.gmaps.geocode(full_query)
            
            if not geocode_result:
                # Try without context if first attempt fails
                geocode_result = self.gmaps.geocode(location_name)
            
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                raise Exception(f"Could not geocode location: {location_name}")
                
        except Exception as e:
            print(f"Geocoding error for {location_name}: {str(e)}")
            raise
    
    def calculate_route(self, locations: List[str], optimize_waypoints: bool = True) -> Dict[str, Any]:
        """
        Calculate optimal route through multiple locations
        
        Args:
            locations: List of location names
            optimize_waypoints: Whether to optimize the order of waypoints
            
        Returns:
            Route information dictionary
        """
        try:
            if len(locations) < 2:
                raise Exception("Need at least 2 locations to calculate a route")
            
            # Set origin and destination (can be the same for a loop)
            origin = locations[0]
            destination = locations[-1]
            
            # Set waypoints (intermediate locations)
            waypoints = locations[1:-1] if len(locations) > 2 else []
            
            print(f"Calculating route from {origin} to {destination}")
            if waypoints:
                print(f"Through waypoints: {waypoints}")
            
            # Calculate directions
            directions_result = self.gmaps.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                optimize_waypoints=optimize_waypoints,
                mode="walking",  # Since this is for campus tour
                units="metric"
            )
            
            if not directions_result:
                raise Exception("No route found")
            
            return directions_result[0]  # Return the first (best) route
            
        except Exception as e:
            print(f"Route calculation error: {str(e)}")
            raise
    
    def parse_route_info(self, route_data: Dict[str, Any]) -> RouteInfo:
        """
        Parse route data into RouteInfo object
        
        Args:
            route_data: Raw route data from Google Maps API
            
        Returns:
            RouteInfo object with parsed information
        """
        try:
            # Extract basic route information
            legs = route_data['legs']
            
            # Calculate total distance and duration
            total_distance = sum(leg['distance']['value'] for leg in legs)
            total_duration = sum(leg['duration']['value'] for leg in legs)
            
            # Format distance and duration
            distance_str = f"{total_distance/1000:.2f} km" if total_distance >= 1000 else f"{total_distance} m"
            duration_str = f"{total_duration//60} min {total_duration%60} sec"
            
            # Extract step-by-step directions
            all_steps = []
            for leg in legs:
                for step in leg['steps']:
                    # Clean HTML tags from instructions
                    instruction = step['html_instructions']
                    instruction = instruction.replace('<b>', '').replace('</b>', '')
                    instruction = instruction.replace('<div style="font-size:0.9em">', ' - ')
                    instruction = instruction.replace('</div>', '')
                    all_steps.append(instruction)
            
            return RouteInfo(
                start_location=legs[0]['start_address'],
                end_location=legs[-1]['end_address'],
                distance=distance_str,
                duration=duration_str,
                steps=all_steps
            )
            
        except Exception as e:
            print(f"Error parsing route info: {str(e)}")
            raise
    
    def get_route_url(self, locations: List[str]) -> str:
        """
        Generate a Google Maps URL for the route
        
        Args:
            locations: List of location names
            
        Returns:
            Google Maps URL string
        """
        base_url = "https://www.google.com/maps/dir/"
        
        # URL encode location names and join with '/'
        encoded_locations = []
        for location in locations:
            encoded_location = location.replace(' ', '+').replace(',', '%2C')
            encoded_locations.append(encoded_location)
        
        return base_url + '/'.join(encoded_locations)
    
    def plan_route(self, locations: List[str]) -> Dict[str, Any]:
        """
        Main function to plan a complete route
        
        Args:
            locations: List of location names
            
        Returns:
            Dictionary containing route information and URL
        """
        try:
            print(f"Planning route for {len(locations)} locations...")
            
            # Calculate the route
            route_data = self.calculate_route(locations)
            
            # Parse route information
            route_info = self.parse_route_info(route_data)
            
            # Generate Google Maps URL
            maps_url = self.get_route_url(locations)
            
            return {
                'route_info': route_info,
                'maps_url': maps_url,
                'raw_data': route_data
            }
            
        except Exception as e:
            print(f"Route planning failed: {str(e)}")
            raise

def main():
    """
    Example usage combining travel planner and route planner
    """
    # API keys (replace with your actual keys)
    qianwen_api_key = os.getenv("QIANWEN_API_KEY", 'sk-3ca7afbf217f4f7aa53983cd9544ff24')
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY", 'AIzaSyAR4vxumJy87gaZF25lt8xCTxU500YGJi0')
    
    try:
        # Step 1: Get locations from travel planner
        print("Getting travel recommendations...")
        travel_workflow = TravelPlannerWorkflow(qianwen_api_key)
        question = "Plan me a trip to tour inside Upenn, exploring the different buildings. It should be 2 hours long."
        destinations = travel_workflow.plan_travel(question)
        location_list = [dest.name for dest in destinations]
        
        print(f"Locations to visit: {location_list}")
        
        # Step 2: Plan route through locations
        print("\nPlanning route...")
        route_planner = GoogleMapsRoutePlanner(google_maps_api_key)
        route_result = route_planner.plan_route(location_list)
        
        # Step 3: Display results
        route_info = route_result['route_info']
        print(f"\nRoute Information:")
        print(f"From: {route_info.start_location}")
        print(f"To: {route_info.end_location}")
        print(f"Total Distance: {route_info.distance}")
        print(f"Total Duration: {route_info.duration}")
        
        print(f"\nStep-by-step directions:")
        for i, step in enumerate(route_info.steps, 1):
            print(f"{i}. {step}")
        
        print(f"\nGoogle Maps URL:")
        print(route_result['maps_url'])
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have set your Google Maps API key:")
        print("export GOOGLE_MAPS_API_KEY='your-api-key-here'")

if __name__ == "__main__":
    main() 