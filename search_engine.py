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

    # Handle disambiguation or “may refer to” pages
    if "may refer to" in response.text or "disambiguation" in response.text.lower():
        print(f"\n⚠️ The term '{query}' refers to multiple topics.\n")

        disambig_links = []
        for li in soup.select("div.mw-parser-output ul li a[href]"):
            href = li["href"]
            if href.startswith("/wiki/") and not ":" in href:  # Skip meta links
                title = li.get_text(strip=True)
                disambig_links.append((title, "https://wikipedia.org" + href))

        if not disambig_links:
            print("No links found on this disambiguation page.")
            return False

        for i, (title, _) in enumerate(disambig_links[:15], start=1):
            print(f"{i}. {title}")

        choice = input("\nEnter number to open that topic (default 1): ").strip()
        if not choice.isdigit():
            choice = 1
        else:
            choice = int(choice)

        choice = max(1, min(choice, len(disambig_links)))
        url = disambig_links[choice - 1][1]

        # Re-fetch the chosen article
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

    # Extract readable content
    page = soup.find_all(["p", "h1", "h2", "h3"])
    if not page:
        print("⚠️ No readable content found.")
        return False

    end = min(end, len(page))
    for data in page[start:end]:
        text = data.get_text(strip=True)
        if text:
            print(text)
            print()

    return end < len(page)  # True if there’s more content left


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
