import json
import requests
from typing import Dict, Any, List
from dataclasses import dataclass
import os

@dataclass
class TravelDestination:
    """Data class for travel destination information"""
    name: str
    description: str
    recommended_duration: str
    best_time_to_visit: str
    highlights: List[str]

class TravelPlannerWorkflow:
    """
    Travel Planner Workflow using Qianwen AI
    
    This class handles the process of analyzing user questions
    to generate personalized travel destination recommendations.
    """
    
    def __init__(self, api_key: str, api_endpoint: str = None):
        """
        Initialize the workflow with API credentials
        
        Args:
            api_key: Qianwen AI API key
            api_endpoint: Optional custom API endpoint
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint or "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_prompt(self, user_question: str) -> str:
        """
        Create the prompt for Qianwen AI
        
        Args:
            user_question: User's travel-related question
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
        You are VISTA, an expert travel planner. Based on the following question, suggest 3-5 specific locations/buildings that would be perfect for the user's needs.

        User Question: {user_question}

        Keep it simple - I only need the location names with minimal information. For each location, provide:
        1. Name of the location/building
        2. A very brief description (1 sentence only)
        3. Duration (keep it simple like "30 minutes")
        4. When to visit (keep it simple like "anytime" or "weekdays")
        5. Just 2-3 brief highlights

        Format the response as a JSON array with the following structure:
        [
            {{
                "name": "Location Name",
                "description": "One brief sentence",
                "recommended_duration": "30 minutes",
                "best_time_to_visit": "anytime",
                "highlights": ["Brief point 1", "Brief point 2"]
            }}
        ]

        Keep everything concise - I mainly just need the location names.
        """
        return prompt.strip()

    def call_qianwen_api(self, prompt: str) -> Dict[str, Any]:
        """
        Make API call to Qianwen AI
        
        Args:
            prompt: Text prompt for the AI
            
        Returns:
            API response as dictionary
        """
        payload = {
            "model": "qwen-max",
            "input": {
                "prompt": prompt,
                "parameters": {
                    "max_tokens": 1500,
                    "temperature": 0.7,
                    "result_format": "json"
                }
            }
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Debug logging
            print("API Response:", json.dumps(response_data, indent=2))
            
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            raise Exception(f"API request failed: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse API response: {str(e)}")
            print(f"Raw response: {response.text}")
            raise Exception(f"Failed to parse API response: {str(e)}")

    def extract_destinations(self, api_response: Dict[str, Any]) -> List[TravelDestination]:
        """
        Extract the travel destinations from API response
        
        Args:
            api_response: Response from Qianwen AI API
            
        Returns:
            List of TravelDestination objects
        """
        try:
            # Debug logging
            print("Extracting from response:", json.dumps(api_response, indent=2))
            
            # Check different possible response structures
            content = None
            if "output" in api_response:
                content = api_response.get("output", {}).get("text", "")
            elif "response" in api_response:
                content = api_response.get("response", "")
            elif "choices" in api_response:
                choices = api_response.get("choices", [])
                if choices:
                    content = choices[0].get("text", "")
            
            if not content:
                raise Exception("No content found in API response")

            # Try to parse the content as JSON
            try:
                destinations_data = json.loads(content)
            except json.JSONDecodeError:
                # If parsing fails, try to extract JSON from the text
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    destinations_data = json.loads(json_match.group(0))
                else:
                    raise Exception("Could not extract JSON from response")
            
            # Convert to TravelDestination objects
            destinations = []
            for data in destinations_data:
                destination = TravelDestination(
                    name=data["name"],
                    description=data["description"],
                    recommended_duration=data["recommended_duration"],
                    best_time_to_visit=data["best_time_to_visit"],
                    highlights=data["highlights"]
                )
                destinations.append(destination)
            
            return destinations
            
        except Exception as e:
            print("Error processing API response:", str(e))
            print("Raw API response:", json.dumps(api_response, indent=2))
            raise Exception(f"Failed to extract destinations from response: {str(e)}")

    def plan_travel(self, user_question: str) -> List[TravelDestination]:
        """
        Main workflow function to process user's travel question
        
        Args:
            user_question: User's travel-related question
            
        Returns:
            List of recommended travel destinations
        """
        try:
            # Step 1: Create prompt
            print("Creating prompt...")
            prompt = self.create_prompt(user_question)
            
            # Step 2: Call Qianwen AI API
            print("Calling Qianwen AI API...")
            api_response = self.call_qianwen_api(prompt)
            
            # Step 3: Extract and return destinations
            print("Extracting destinations...")
            destinations = self.extract_destinations(api_response)
            
            return destinations
            
        except Exception as e:
            print(f"Error in workflow: {str(e)}")
            raise

def main():
    """
    Example usage of the TravelPlannerWorkflow
    """
    # Initialize workflow (replace with your actual API key)
    api_key = os.getenv("QIANWEN_API_KEY", '')
    workflow = TravelPlannerWorkflow(api_key)
    
    # Example question
    question = "Plan me a trip to tour inside Upenn, exploring the different buildings. It should be 2 hours long."
    
    try:
        # Get travel recommendations
        destinations = workflow.plan_travel(question)
        
        # Create and print only the list of location names
        location_list = [dest.name for dest in destinations]
        print(location_list)
        
    except Exception as e:
        print(f"Workflow failed: {str(e)}")

if __name__ == "__main__":
    main() 