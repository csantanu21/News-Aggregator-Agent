from youtube_transcript_api import YouTubeTranscriptApi 

def get_transcript(video_id, languages=['en']):
    """
    Extract transcript text from a YouTube video.
    
    :param video_id: YouTube video ID
    :param languages: List of language codes to try (default: ['en'])
    :return: Transcript text or None if unavailable
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id, languages=languages)
        transcript_text = ' '.join([item.text for item in transcript_list])
        return transcript_text
    except Exception as e:
        print(f"Error getting transcript for {video_id}: {e}")
        return None

def get_transcript_with_timestamps(video_id, languages=['en']):
    """
    Extract transcript with timestamps from a YouTube video.
    
    :param video_id: YouTube video ID
    :param languages: List of language codes to try
    :return: List of dicts with 'text' and 'start' or None
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id, languages=languages)
        return transcript_list
    except Exception as e:
        print(f"Error getting transcript for {video_id}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Example video ID
    video_id = '8JXwrVQQ4jw'  # Rick Roll
    transcript = get_transcript(video_id)
    if transcript:
        print(transcript[:200] + '...')
    else:
        print("No transcript available.")

    transcript_with_timestamps = get_transcript_with_timestamps(video_id)
    if transcript_with_timestamps:
        print(transcript_with_timestamps[:5])
    else: 
        print("No transcript with timestamps available.")

    