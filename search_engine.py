import requests
from bs4 import BeautifulSoup

def wiki_scrape(query: str, start: int = 0, end: int = 3) -> bool:
    """Scrape Wikipedia for a given query, printing paragraphs from start to end."""
    query = query.replace(" ", "_")
    url = f"https://wikipedia.org/wiki/{query}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("⚠️ Could not retrieve the page.")
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    page = soup.find_all(["p", "h1", "h2", "h3"])

    if not page:
        print("⚠️ No readable content found.")
        return False

    # Limit end to length of paragraphs
    end = min(end, len(page))

    for data in page[start:end]:
        text = p.get_text(strip=True)
        if text:
            print(text)
            print()

    return end < len(paragraphs)  # Return True if there’s more content left


def search_engine():
    """Wikipedia-powered interactive search tool."""
    while True:
        query = input("\n🔍 Enter a Wikipedia topic (or 'exit' to quit): ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Exiting search engine.")
            break

        start, end = 0, 3

        while True:
            has_more = wiki_scrape(query, start, end)
            if not has_more:
                print("✅ End of article.")
                break

            choice = input("Press Enter for 3 more, 'all' for all, or 'back' to new search: ").strip().lower()

            if choice == "":
                start += 3
                end += 3
            elif choice == "all":
                wiki_scrape(query, end, 9999)
                break
            elif choice in ("back", "b"):
                break
            else:
                print("Unknown option — returning to main search.")
                break


if __name__ == "__main__":
    search_engine()
