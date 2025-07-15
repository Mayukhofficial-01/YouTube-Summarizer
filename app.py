# To run this code, you need to install the following dependencies:
# pip install youtube-transcript-api google-genai python-dotenv

import os
import json
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from google import genai
from google.genai import types
from fastapi import FastAPI

app=FastAPI()
# Load environment variables from .env file
load_dotenv()

def fetch_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Format transcript as a single string with spaces
        text_formatted = " ".join(segment['text'] for segment in transcript)
        return text_formatted
    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video ID {video_id}.")
        return None
    except NoTranscriptFound:
        print(f"Error: No transcript found for video ID {video_id} in the requested language.")
        return None
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def generate_summary(transcript, video_id):
    """
    Generates a summary of the transcript using the Gemini API in the specified JSON format.
    
    Args:
        transcript (str): The YouTube video transcript.
        video_id (str): The YouTube video ID for context.
    
    Returns:
        dict: A dictionary containing topic_name and topic_summary, or None if an error occurs.
    """
    if not transcript:
        print("No transcript provided for summarization.")
        return None

    try:
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        model = "gemini-2.5-pro"

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"""Based on the following YouTube transcription, return a brief summary of the topic in the JSON format below:
{{
  "topic_name": "name of topic",
  "topic_summary": "summary of topic"
}}

Transcription:
{transcript}
"""
                    ),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=0.5,
            thinking_config=types.ThinkingConfig(thinking_budget=-1),
            response_mime_type="application/json",
        )

        # Call Gemini API without streaming
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        # Parse the response as JSON
        summary = json.loads(response.text)
        return summary

    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return None

def extract_youtube_id(url):
    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL format")


def main():
    """
    Main function to fetch a YouTube transcript and generate a summary.
    """
    video_id = extract_youtube_id("https://www.youtube.com/watch?v=1xue6AgPOyM")  # Replace with your YouTube video URL
    transcript = fetch_youtube_transcript(video_id)
    
    if transcript:
        summary = generate_summary(transcript, video_id)
        if summary:
            print("Generated Summary:")
            print(json.dumps(summary, indent=2))
            # Save to a file
            with open("summary.json", "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
        else:
            print("Failed to generate summary.")
    else:
        print("Failed to fetch transcript.")

@app.get("/summarize")
def summarize(url: str):
    video_id = extract_youtube_id(url)
    transcript = fetch_youtube_transcript(video_id)
    if transcript:
        summary = generate_summary(transcript, video_id)
        print("Summary:", summary)
        return summary
    else:
        return {"error": "Transcript not found."}
        

if __name__ == "__main__":
    # Ensure the GEMINI_API_KEY environment variable is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
    else:
        main()