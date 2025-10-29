# 🧠 Wikipedia-Powered Search Engine (Python)

A simple terminal-based Wikipedia search engine built in Python using **Requests** and **BeautifulSoup**.  
It lets you search for any topic, read the first few paragraphs, and load more content incrementally — just like scrolling through an article.

---

## 🚀 Features

- 🔍 Search for any topic on Wikipedia  
- 📄 View results 3 paragraphs at a time  
- ↩️ Load 3 more paragraphs with a single keypress  
- 🧾 Read the entire article with the `all` option  
- ❌ Stop anytime with `break`, `quit`, or `exit`  
- 🧠 Automatically skips if no content is found  
- 🌐 Lightweight — uses only `requests` + `bs4`

---

## 🧩 How It Works

1. The script sends a request to the Wikipedia page for your search term.  
2. It parses the HTML content using **BeautifulSoup**.  
3. It extracts all `<p>`, `<h1>`, `<h2>`, and `<h3>` elements.  
4. The user can view the content chunk by chunk (3 paragraphs at a time).  
5. You can:
   - Press **Enter** → view 3 more paragraphs  
   - Type **all** → view the full article  
   - Type **break / quit / exit** → stop the program  

---

## ⚙️ Requirements

Install the required packages before running:

```bash
pip install requests beautifulsoup4
```

---

## 🖥️ Usage

Run the script in your terminal:

```bash
python wiki_search.py
```

Then follow the prompts:

```
Enter what you want to search:
> Python programming

--Press Enter for 3 more paragraphs, 'all' for all, 'break' to stop--
```

---

## 🧠 Example Output

```
Python is a high-level, interpreted programming language...
It emphasizes readability and productivity...

--Press Enter to see more--
```

⚙️ Installation

Make sure you have Python 3.8+ installed.

pip install requests beautifulsoup4


Then run:
``` bash
python wiki_search.py
```
🧱 File Structure
```
.
├── wiki_search.py     # Main script
├── README.md          # Documentation
└── requirements.txt   # Dependencies
```

⚖️ Legal & Ethical Use

This project uses Wikipedia’s public web pages for educational and non-commercial purposes.
It respects Wikipedia’s robots.txt and makes a limited number of polite requests (no spamming).
Always follow site terms of use when scraping.

🧩 Requirements
Library	Purpose
requests	Fetch webpage HTML
beautifulsoup4	Parse and extract text from HTML
