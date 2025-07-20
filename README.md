# VISTA (Vision-Integrated Smart Tour Assistant)

## Overview
VISTA is an intelligent, AI-powered automated tour guide application designed to offer a dynamic, personalized, and context-aware experience as an alternative to traditional, static tour guides. The application acts as a "local companion," providing real-time information, practical tips, and interactive guidance based on a user's current environment, specifically targeting locations within the United States.

## Project Goal
The goal is to develop a Minimum Viable Product (MVP) demonstrating core functionalities, focusing on UPenn tours. The MVP will include:
- Live Image Capture & Interpretation
- AI-Driven Contextualization
- Conversational AI Guidance
- Basic Real-Time Enrichment
- Personal Route Planning

## Technologies and Frameworks
- **Backend**: FastAPI, Uvicorn, Pydantic, Asyncio, httpx, Pillow, python-mimeparse
- **AI Models**: torch, transformers (BLIP-2 weights)
- **Mobile/Web**: Expo SDK 50, react-navigation 7, react-native-maps, expo-camera
- **State Management**: Zustand, axios
- **Styling**: tailwind-rn or NativeWind
- **DevOps**: Docker, GitHub Actions, Render/Railway, Sentry, PostHog

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.8+
- Docker
- Expo CLI

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vista/server
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Mobile/Web Setup
1. Navigate to the mobile directory:
   ```bash
   cd vista/mobile
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Expo development server:
   ```bash
   expo start
   ```

### Deployment
- The backend can be containerized using Docker and deployed on platforms like Render or Railway.
- Ensure environment variables for API keys are set in the deployment platform.

## Contribution
- Fork the repository and create a new branch for your feature or bug fix.
- Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please contact the project team:
- Tony Yang (Project Architect & Route Planning Lead)
- Larry Chen (Backend & Core AI Integration Lead)
- Felix Mao (Image-to-Text & Frontend AI Integration)
- Kaden Yeung (UI/UX Design & Deployment Lead) 