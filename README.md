# YouTube Video Summary

This is a Python program that provides a written summary of a YouTube video. The program extracts relevant noun phrases from the video subtitles and considers additional factors such as video duration and keywords in the video title and tags.

Requirements
Python 3.x
Google API Client Library for Python (google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client)
spaCy (spacy, en_core_web_lg)
You can install the required Python libraries using pip:

bash
Copy code
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client spacy
python -m spacy download en_core_web_lg
Usage
Obtain a Google API key and enable the YouTube Data API v3 in the Google Cloud Console.

Clone this repository and navigate to the project directory in your terminal.

Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your Google API key JSON file:

bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google/api/key.json
Run the program and enter the URL of the YouTube video you want to summarize:

bash
Copy code
python summarize.py
The program will extract relevant noun phrases from the video subtitles and consider additional factors such as video duration and keywords in the video title and tags to provide a written summary of the video.

License
This project is licensed under the MIT License. See the LICENSE file for details.
