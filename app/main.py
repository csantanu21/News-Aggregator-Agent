import argparse
from app.scraper.youtube_rss import get_latest_videos

def main():
    parser = argparse.ArgumentParser(description="YouTube RSS Video Extractor")
    parser.add_argument("channel", help="YouTube channel (@handle, URL, or ID)")
    parser.add_argument("--max", type=int, default=5, help="Max videos to fetch")
    
    args = parser.parse_args()
    
    videos = get_latest_videos(args.channel, args.max)
    for video in videos:
        print(f"Title: {video['title']}")
        print(f"URL: {video['url']}")
        print(f"Published: {video['published']}")
        print("---")

if __name__ == "__main__":
    main()