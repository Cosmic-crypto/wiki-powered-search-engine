import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ───────────────────────────────
# 🧠 Initialize the Gemini model
# ───────────────────────────────
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt template for summarization
prompt = PromptTemplate(
    input_variables=["content"],
    template="Summarize the following Wikipedia text in 3 concise bullet points:\n\n{content}",
)

summarizer_chain = LLMChain(llm=llm, prompt=prompt)


def wiki_scrape(query: str, start: int = 0, end: int = 3, summarize: bool = True) -> bool:
    """Scrape Wikipedia for a given query and optionally summarize."""
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
    page = soup.find_all("p")

    if not page:
        print("⚠️ No readable content found.")
        return False

    # Limit to available paragraphs
    end = min(end, len(page))
    extracted_text = "\n\n".join(p.get_text(strip=True) for p in page[start:end] if p.get_text(strip=True))

    print("\n📖 --- Extracted Wikipedia Text ---\n")
    print(extracted_text)

    # Summarize with Gemini
    if summarize:
        print("\n🧠 --- Gemini Summary ---\n")
        summary = summarizer_chain.run(content=extracted_text)
        print(summary)

    return end < len(page)  # True if there’s more to show


def search_engine():
    """Interactive Wikipedia-powered search tool with Gemini summarization."""
    while True:
        query = input("\n🔍 Enter a Wikipedia topic (or 'exit' to quit): ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Exiting search engine.")
            break

        start, end = 0, 3

        while True:
            has_more = wiki_scrape(query, start, end, summarize=True)
            if not has_more:
                print("\n✅ End of article.")
                break

            choice = input("\nPress Enter for 3 more, 'all' for all, or 'back' to new search: ").strip().lower()

            if choice == "":
                start += 3
                end += 3
            elif choice == "all":
                wiki_scrape(query, end, 9999, summarize=True)
                break
            elif choice in ("back", "b"):
                break
            else:
                print("Unknown option — returning to main search.")
                break


if __name__ == "__main__":
    search_engine()
