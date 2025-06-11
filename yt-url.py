#!/usr/bin/env python3
"""
YouTube URL Search Tool

A command-line utility that searches YouTube for videos and returns
the URL of the top search result.

Usage:
    python yt_url.py "search query"

"""

import argparse
import sys
import urllib.parse
import urllib.request
import re


class YouTubeSearchError(Exception):
    """Custom exception for YouTube search errors."""

    pass


class YouTubeSearcher:
    """Handles YouTube search operations."""

    BASE_SEARCH_URL = "https://www.youtube.com/results"
    BASE_VIDEO_URL = "https://www.youtube.com/watch"

    def __init__(self) -> None:
        """Initialize the YouTube searcher."""
        self.session_headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )
        }

    def search(self, query: str) -> str:
        """
        Search YouTube for a video and return the top result URL.

        Args:
            query: The search string for the YouTube video

        Returns:
            The full YouTube URL of the top search result

        Raises:
            YouTubeSearchError: If the search fails or no results are found
        """
        if not query.strip():
            raise YouTubeSearchError("Search query cannot be empty")

        try:
            # Construct search URL
            search_url = self._build_search_url(query)

            # Fetch search results page
            html_content = self._fetch_page(search_url)

            # Extract first video ID from results
            video_id = self._extract_first_video_id(html_content)

            # Build and return full video URL
            return self._build_video_url(video_id)

        except Exception as e:
            raise YouTubeSearchError(f"Search failed: {str(e)}") from e

    def _build_search_url(self, query: str) -> str:
        """Build the YouTube search URL with encoded query parameters."""
        params = urllib.parse.urlencode({'search_query': query})
        return f"{self.BASE_SEARCH_URL}?{params}"

    def _fetch_page(self, url: str) -> str:
        """Fetch the HTML content of a web page."""
        request = urllib.request.Request(url, headers=self.session_headers)

        with urllib.request.urlopen(request, timeout=10) as response:
            return response.read().decode('utf-8')

    def _extract_first_video_id(self, html_content: str) -> str:
        """
        Extract the first video ID from YouTube search results HTML.

        Args:
            html_content: The HTML content of the search results page

        Returns:
            The video ID of the first search result

        Raises:
            YouTubeSearchError: If no video ID is found
        """
        # Pattern to match video IDs in YouTube search results
        # This looks for the videoId in the JavaScript data
        patterns = [
            r'"videoId":"([a-zA-Z0-9_-]{11})"',
            r'watch\?v=([a-zA-Z0-9_-]{11})',
            r'/watch\?v=([a-zA-Z0-9_-]{11})',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                return matches[0]

        raise YouTubeSearchError("No video results found for the given search query")

    def _build_video_url(self, video_id: str) -> str:
        """Build the full YouTube video URL from a video ID."""
        return f"{self.BASE_VIDEO_URL}?v={video_id}"


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Search YouTube and return the URL of the top result", prog="yt-url"
    )

    parser.add_argument("query", help="Search string for the YouTube video")

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    return parser


def main() -> int:
    """
    Main entry point for the command-line tool.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        searcher = YouTubeSearcher()

        if args.verbose:
            print(f"Searching for: {args.query}", file=sys.stderr)

        video_url = searcher.search(args.query)
        print(video_url)

        return 0

    except YouTubeSearchError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\nSearch cancelled by user", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
