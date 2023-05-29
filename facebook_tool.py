from facebook_scraper import *
import os


from langchain.tools import BaseTool


from typing import Optional, Type
from langchain.callbacks.manager import AsyncCallbackManager, CallbackManager

# How to make your cookies.json file--> https://superuser.com/questions/1486002/how-do-i-see-request-cookies-in-chrome

os.environ["OPENAI_API_KEY"] = "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"
set_user_agent(
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)

"""
Avoid calling too frequently to avoid temporary blocks
"""


class FacebookScraper(BaseTool):
    name = "facebook_scraper"
    description = "useful when you want to scrape facebok based on unique page name, profile name, or ID."
    # pages: how many most recent pages of posts to request
    def _run(self, string: str, run_manager: Optional[CallbackManager] = None) -> list:
        """Use the tool."""
        all_data = []
        values = string.split(",")
        query = values[0]
        if len(values) > 1:
            num_pages = int(values[1])
        else:
            num_pages = 3
        try:
            for post in get_posts(query, cookies="cookies.json", pages=num_pages):
                all_data.append(post)
            return all_data
        except Exception as e:
            print(e)
            return []

    async def _arun(
        self, query: str, pages: int, run_manager: Optional[AsyncCallbackManager] = None
    ) -> list:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


def main():
    tool = FacebookScraper()
    print(tool.run("1138120323385047,3"))  # US news group- https://web.facebook.com/groups/1138120323385047, 3 pages


if __name__ == main():
    main()
