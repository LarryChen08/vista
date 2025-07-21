import base64
import json
import requests
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import io
import os
from dataclasses import dataclass

@dataclass
class LocationData:
    """Data class for location information"""
    latitude: float
    longitude: float
    address: Optional[str] = None
    landmark: Optional[str] = None

class ImageRecognitionWorkflow:
    """
    Image Recognition Workflow using Qianwen AI
    
    This class handles the process of analyzing images with location context
    to generate descriptive text about buildings and landmarks.
    """
    
    def __init__(self, api_key: str, api_endpoint: str = None):
        """
        Initialize the workflow with API credentials
        
        Args:
            api_key: Qianwen AI API key
            api_endpoint: Optional custom API endpoint
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint or "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def preprocess_image(self, image_path: str, max_size: Tuple[int, int] = (1024, 1024)) -> str:
        """
        Preprocess image for API submission
        
        Args:
            image_path: Path to the image file
            max_size: Maximum dimensions for image resizing
            
        Returns:
            Base64 encoded image string
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if image is too large
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                image_bytes = buffer.getvalue()
                
                return base64.b64encode(image_bytes).decode('utf-8')
                
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def get_location_context(self, location: LocationData) -> str:
        """
        Generate location context string for the AI prompt
        
        Args:
            location: LocationData object containing coordinates and optional details
            
        Returns:
            Formatted location context string
        """
        context = f"Location coordinates: {location.latitude}, {location.longitude}"
        
        if location.address:
            context += f"\nAddress: {location.address}"
        
        if location.landmark:
            context += f"\nNearby landmark: {location.landmark}"
            
        return context
    
    def create_prompt(self, location: LocationData) -> str:
        """
        Create the prompt for Qianwen AI
        
        Args:
            location: LocationData object
            
        Returns:
            Formatted prompt string
        """
        location_context = self.get_location_context(location)
        
        prompt = f"""
        You are VISTA, an enthusiastic and knowledgeable tour guide. Analyze this image and provide a detailed, engaging description of the building or landmark shown.
        
        {location_context}
        
        Please provide:
        1. A vivid description of the building/landmark in the image
        4. Any interesting facts or recommendations for visitors
        5. Safety tips or practical advice if relevant (If no then don't mention it)

        Write all of the above in a single paragraph, make it short and concise.

        Do not include the location context provided by the user in your response. The location context will be close but might not be exactly accurate. 
        
        You should first identify what's in the image and then look for the building/landmark in the image. The building/landmark will be very close to the location provided.

        Keep the tone friendly and informative, as if you're speaking to a curious tourist. Focus on what makes this place special and worth visiting.
        """
        
        return prompt.strip()
    
    def call_qianwen_api(self, image_base64: str, prompt: str) -> Dict[str, Any]:
        """
        Make API call to Qianwen AI
        
        Args:
            image_base64: Base64 encoded image
            prompt: Text prompt for the AI
            
        Returns:
            API response as dictionary
        """
        payload = {
            "model": "qwen-vl-max",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "image": f"data:image/jpeg;base64,{image_base64}"
                            },
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            },
            "parameters": {
                "max_tokens": 1000,
                "temperature": 0.7
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
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse API response: {str(e)}")
    
    def extract_description(self, api_response: Dict[str, Any]) -> str:
        """
        Extract the description text from API response
        
        Args:
            api_response: Response from Qianwen AI API
            
        Returns:
            Extracted description text
        """
        try:
            # Navigate the response structure to extract the text
            output = api_response.get("output", {})
            choices = output.get("choices", [])
            
            if not choices:
                raise Exception("No choices found in API response")
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            if not content:
                raise Exception("No content found in API response")
            
            # Handle case where content is a list
            if isinstance(content, list):
                # Join all text content from the list
                text_contents = []
                for item in content:
                    if isinstance(item, dict) and "text" in item:
                        text_contents.append(item["text"])
                    elif isinstance(item, str):
                        text_contents.append(item)
                content = " ".join(text_contents)
            
            return content.strip()
            
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract description from response: {str(e)}")
            
        except Exception as e:
            print("Raw API response:", json.dumps(api_response, indent=2))
            raise Exception(f"Unexpected error processing API response: {str(e)}")
    
    def process_image(self, image_path: str, location: LocationData) -> str:
        """
        Main workflow function to process image and location
        
        Args:
            image_path: Path to the image file
            location: LocationData object with coordinates and optional details
            
        Returns:
            Generated description text
        """
        try:
            # Step 1: Preprocess the image
            print("Preprocessing image...")
            image_base64 = self.preprocess_image(image_path)
            
            # Step 2: Create prompt with location context
            print("Creating prompt...")
            prompt = self.create_prompt(location)
            
            # Step 3: Call Qianwen AI API
            print("Calling Qianwen AI API...")
            api_response = self.call_qianwen_api(image_base64, prompt)
            
            # Step 4: Extract and return description
            print("Extracting description...")
            description = self.extract_description(api_response)
            
            return description
            
        except Exception as e:
            print(f"Error in workflow: {str(e)}")
            raise

def main():
    """
    Example usage of the ImageRecognitionWorkflow
    """
    # Initialize workflow (replace with your actual API key)
    api_key = os.getenv("QIANWEN_API_KEY", '')
    workflow = ImageRecognitionWorkflow(api_key)
    
    # Example location data
    location = LocationData(
        latitude=39.953514, 
        longitude=-75.197903,
        address="Jon M. Huntsman Hall, 3730 Walnut St, Philadelphia, PA 19104",
    )
    
    # Example image path
    image_path = "image_example/example10.jpg"
    
    try:
        # Process the image
        description = workflow.process_image(image_path, location)
        
        print("Generated Description:")
        print("-" * 50)
        print(description)
        
    except Exception as e:
        print(f"Workflow failed: {str(e)}")

if __name__ == "__main__":
    main() 