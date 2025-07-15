# YouTube Transcript Summarizer

## Overview
This project is a FastAPI-based application that fetches YouTube video transcripts using the `youtube-transcript-api` and generates concise summaries using the Gemini AI model from Google. The summarized output is returned in JSON format and saved to a file (`summary.json`).

## Demo Video
Watch a demonstration of the YouTube Transcript Summarizer in action:  
[Demo Video]: https://drive.google.com/file/d/1nt-KYJHoBMWUfHPqrJqJ2XiJb8-KWgxT/view?usp=drive_link 


## Features
- Extracts YouTube video IDs from URLs
- Fetches video transcripts using `youtube-transcript-api`
- Generates summaries using the Gemini AI model
- Provides a REST API endpoint for summarization
- Saves summaries to a JSON file
- Robust error handling for invalid URLs, disabled transcripts, and API errors

## Prerequisites
- Python 3.8+
- A valid Gemini API key (set as `GEMINI_API_KEY` in a `.env` file)
- Internet connection for API requests

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd youtube-transcript-summarizer
   ```

2. Install dependencies:
   ```bash
   pip install youtube-transcript-api google-genai python-dotenv fastapi uvicorn pydantic
   ```

3. Create a `.env` file in the project root and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your-api-key-here
   ```

## Usage
### Running the Application
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The server will run at `http://localhost:8000`.

2. Access the summarization endpoint:
   - **Endpoint**: `GET /summarize?url=<YouTube-video-URL>`
   - **Example**: `http://localhost:8000/summarize?url=https://www.youtube.com/watch?v=1xue6AgPOyM`
   - **Response**: JSON object with `topic_name` and `topic_summary`, or an error message.

3. Run the script directly (for testing):
   ```bash
   python youtube_summarizer.py
   ```
   This uses the default video URL defined in the `main` function and saves the summary to `summary.json`.

### Example Output
```json
{
  "topic_name": "Introduction to Python",
  "topic_summary": "The video covers the basics of Python programming, including variables, data types, and control structures."
}
```




## Project Structure
```
youtube-transcript-summarizer/
├── youtube_summarizer.py  # Main application code
├── .env                   # Environment variables (not tracked)
├── summary.json           # Generated summary output
└── README.md              # This file
```

## Dependencies
- `youtube-transcript-api`: Fetches YouTube video transcripts
- `google-genai`: Interacts with the Gemini AI model
- `python-dotenv`: Loads environment variables from `.env`
- `fastapi`: Web framework for the API
- `uvicorn`: ASGI server for running FastAPI
- `pydantic`: Data validation for URL inputs

## Error Handling
The application handles:
- Invalid YouTube URLs
- Videos with disabled or unavailable transcripts
- Missing or invalid Gemini API keys
- General API errors with appropriate HTTP status codes

## Notes
- Ensure the YouTube video has transcripts enabled.
- The Gemini API key must be valid and have sufficient quota.
- The application supports both `youtube.com` and `youtu.be` URL formats.
- Summaries are saved to `summary.json` in the project root when running the script directly.

## License
This project is licensed under the MIT License.
