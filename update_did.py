import os
import requests

API_KEY = os.getenv("DID_API_KEY")
KNOWLEDGE_ID = os.getenv("KNOWLEDGE_ID")
AGENT_ID = os.getenv("AGENT_ID")
REPO = os.getenv("GITHUB_REPOSITORY")

HEADERS = {
    "Authorization": f"Basic {API_KEY}",
    "Content-Type": "application/json"
}

DID_BASE = "https://api.d-id.com"


def upload_document(filename):
    raw_url = f"https://raw.githubusercontent.com/{REPO}/main/{filename}"

    document_data = {
        "documentType": "text",
        "title": filename,
        "source_url": raw_url
    }

    print(f"Uploading: {filename}")
    print(f"URL: {raw_url}")

    res = requests.post(
        f"{DID_BASE}/knowledge/{KNOWLEDGE_ID}/documents",
        headers=HEADERS,
        json=document_data
    )

    print("Status:", res.status_code, res.text)


def connect_knowledge_to_agent():
    if not AGENT_ID:
        print("AGENT_ID not provided. Skipping agent update.")
        return

    res = requests.patch(
        f"{DID_BASE}/agents/{AGENT_ID}",
        headers=HEADERS,
        json={"knowledge": {"id": KNOWLEDGE_ID}}
    )

    print("Agent update:", res.status_code, res.text)


def main():
    print("Searching for text and markdown files...")

    targets = []

    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".txt") or f.endswith(".md"):
                path = os.path.relpath(os.path.join(root, f), ".")
                targets.append(path)

    if not targets:
        print("No text files found.")
        return

    print(f"{len(targets)} documents found:")
    for t in targets:
        print(" -", t)

    for t in targets:
        upload_document(t)

    connect_knowledge_to_agent()
    print("Sync completed.")


if __name__ == "__main__":
    main()
