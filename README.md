# Weather API with AI Integration

   Flask API for weather data with AI-powered recommendations.

   ## Setup

   1. Install dependencies:
```bash
   pip install flask requests groq python-dotenv
```

   2. Create `.env` file with your credentials:
```
   API_KEY=your_visualcrossing_key
   VALID_TOKEN=your_security_token
   API_AI=your_groq_api_key
```

   3. Run:
```bash
   python weather.py
```

   ## Endpoints

   - `POST /weather` - Get weather data
   - `POST /weather-advice` - Get weather + AI recommendations