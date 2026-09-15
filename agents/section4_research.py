import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SECTION_4_AGENTS = [
    {"name": "Literature Scout", "job": "search for relevant scientific information on a biology topic"},
    {"name": "Summarizer", "job": "summarize research findings in plain, non-technical language"}
]

def literature_search(question):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=f"You are {SECTION_4_AGENTS[0]['name']}, a BioInsight agent whose job is to {SECTION_4_AGENTS[0]['job']}.",
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": question}]
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    return None

def summarize_findings(raw_text):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=f"You are {SECTION_4_AGENTS[1]['name']}, a BioInsight agent whose job is to {SECTION_4_AGENTS[1]['job']}. Summarize in 3 sentences maximum.",
        messages=[{"role": "user", "content": raw_text}]
    )
    return response.content[0].text

import requests
import xml.etree.ElementTree as ET

def search_pubmed(query, max_results=5):
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    search_response = requests.get(search_url, params=search_params)
    id_list = search_response.json()["esearchresult"]["idlist"]

    if not id_list:
        return []

    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "rettype": "abstract",
        "retmode": "xml"
    }
    fetch_response = requests.get(fetch_url, params=fetch_params)

    root = ET.fromstring(fetch_response.content)
    articles = []
    for article in root.findall(".//PubmedArticle"):
        title_elem = article.find(".//ArticleTitle")
        abstract_elem = article.find(".//AbstractText")
        title = title_elem.text if title_elem is not None else "No title"
        abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
        articles.append({"title": title, "abstract": abstract})

    return articles

def pubmed_literature_search(query):
    articles = search_pubmed(query)

    if not articles:
        return "No relevant PubMed articles found."

    combined_text = "\n\n".join(
        f"Title: {a['title']}\nAbstract: {a['abstract']}" for a in articles
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=f"You are {SECTION_4_AGENTS[0]['name']}, a BioInsight agent whose job is to {SECTION_4_AGENTS[0]['job']}. Base your answer only on the provided PubMed abstracts.",
        messages=[{"role": "user", "content": f"Question: {query}\n\nPubMed findings:\n{combined_text}"}]
    )
    return response.content[0].text

if __name__ == "__main__":
    research_result = literature_search("What is known about GC content and DNA thermal stability?")
    print("--- Full research ---")
    print(research_result)

    summary = summarize_findings(research_result)
    print("--- Summary ---")
    print(summary)

    print("--- PubMed results ---")
    results = search_pubmed("GC content DNA stability")
    for r in results:
        print(r["title"])
        print(r["abstract"][:200])
        print("---")

    print("--- PubMed-grounded answer ---")
    grounded_answer = pubmed_literature_search("GC content DNA stability")
    print(grounded_answer)