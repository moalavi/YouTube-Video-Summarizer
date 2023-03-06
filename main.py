import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
import re

# Set up YouTube API connection
credentials, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
youtube = build("youtube", "v3", credentials=credentials)

# Get video ID from user input
video_url = input("Enter YouTube video URL: ")
video_id = video_url.split("=")[1]

# Get video information
try:
    video_response = youtube.videos().list(
        part="snippet, contentDetails",
        id=video_id,
        fields="items(id, snippet(title, tags), contentDetails(duration))"
    ).execute()
    video_info = video_response["items"][0]
    video_title = video_info["snippet"]["title"]
    video_tags = video_info["snippet"]["tags"]
    video_duration = video_info["contentDetails"]["duration"]
except HttpError as error:
    print(f"An error occurred: {error}")
    video_title = ""
    video_tags = []
    video_duration = ""

# Get video subtitles
try:
    caption_response = youtube.captions().list(
        part="snippet",
        videoId=video_id,
        fields="items(id)",
    ).execute()
    caption_id = caption_response["items"][0]["id"]
    subtitle_response = youtube.captions().download(
        id=caption_id,
        tfmt="srt",
    ).execute()
    subtitle_text = subtitle_response.decode("utf-8")
except HttpError as error:
    print(f"An error occurred: {error}")
    subtitle_text = ""

# Use spaCy to process the subtitles and extract relevant noun phrases
nlp = spacy.load("en_core_web_lg")

# Define custom stop words
custom_stop_words = ["youtube", "video", "videos", "watch", "channel", "subscribe", "subscribe to", "like", "comment", "share", "thanks", "thank you", "intro", "outro"]
for word in custom_stop_words:
    STOP_WORDS.add(word)

doc = nlp(subtitle_text)
noun_phrases = [chunk.text for chunk in doc.noun_chunks if not any(stop_word in chunk.text.lower() for stop_word in STOP_WORDS)]

# Extract most common keywords from video title and tags
all_words = re.findall(r'\w+', video_title + " ".join(video_tags).lower())
keywords = [word for word in all_words if word not in STOP_WORDS]
keywords = [word for word in keywords if len(word) > 2]
keyword_counts = Counter(keywords).most_common(3)
top_keywords = [count[0] for count in keyword_counts]

# Print the summary of the video content
print(f"Summary of '{video_title}' (duration: {video_duration}, keywords: {', '.join(top_keywords)})")
print(", ".join(set(noun_phrases)))
