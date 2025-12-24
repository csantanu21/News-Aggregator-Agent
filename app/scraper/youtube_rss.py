import feedparser
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def get_channel_id(channel_input):
    """
    Get YouTube channel ID from various inputs: @handle, URL, or direct ID.
    
    :param channel_input: @Handle, full URL, or channel ID
    :return: Channel ID string
    """
    if channel_input.startswith('UC') and len(channel_input) == 24:  # Typical channel ID length
        return channel_input
    elif channel_input.startswith('@'):
        return get_channel_id_from_handle(channel_input[1:])  # Remove @
    elif 'youtube.com' in channel_input:
        return get_channel_id_from_url(channel_input)
    else:
        raise ValueError("Invalid channel input. Use @handle, URL, or channel ID.")

def get_channel_id_from_handle(handle):
    """
    Resolve @handle to channel ID by scraping the YouTube page.
    """
    url = f"https://www.youtube.com/@{handle}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Could not fetch page for @{handle}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    # Look for meta tag
    meta = soup.find('meta', property='og:url')
    if meta and 'channel/' in meta['content']:
        return meta['content'].split('/channel/')[1]
    # Alternative: look in scripts or other tags
    # For now, assume meta works
    raise ValueError(f"Could not find channel ID for @{handle}")

def get_channel_id_from_url(channel_url):
    """
    Extract channel ID from YouTube channel URL.
    """
    parsed = urlparse(channel_url)
    path = parsed.path
    if '/channel/' in path:
        return path.split('/channel/')[1]
    elif path.startswith('/@'):
        handle = path[2:]
        return get_channel_id_from_handle(handle)
    else:
        raise ValueError("Unsupported URL format.")

def get_latest_videos(channel_input, max_videos=5):
    """
    Fetch the latest videos from a YouTube channel using RSS feed.
    
    :param channel_input: @Handle, URL, or channel ID
    :param max_videos: Number of latest videos to fetch
    :return: List of dicts with video details
    """
    channel_id = get_channel_id(channel_input)
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(rss_url)
    
    videos = []
    for entry in feed.entries[:max_videos]:
        video = {
            'video_id': entry.yt_videoid if 'yt_videoid' in entry else entry.id.split(':')[-1],
            'title': entry.title,
            'url': entry.link,
            'published': entry.published,
            'description': getattr(entry, 'summary', ''),
            'author': getattr(entry, 'author', '')
        }
        videos.append(video)
    
    return videos

# Example usage
if __name__ == "__main__":
    # Example for OpenAI
    videos = get_latest_videos('@OpenAI', 3)
    for v in videos:
        print(v)

