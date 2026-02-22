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
     
   ## Setup Postman

   1. Import `Weather_API.postman_collection.json`
   2. Import `Weather_API.postman_environment.json`
   3. Edit environment variables with YOUR values:
      - `base_url`: `http://your-server-ip:8000`
      - `token`: Your security token
      - `requester_name`: Your full name
   4. Select "Weather API" environment
   5. Run requests!
