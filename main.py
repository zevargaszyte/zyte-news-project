import pandas as pd
import requests
from base64 import b64decode

API_KEY = "624c725e317e4ce5ba44f4c3813d7fc2"  # Substitui pela tua chave Zyte

def fetch_articles(url):
    response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=(API_KEY, ""),
        json={
            "url": url,
            "articleList": True,
            "articleListOptions": {"extractFrom": "httpResponseBody"},
        },
    )
    return response.json().get("articleList", [])[:3]

def main():
    df = pd.read_csv("Saas.csv")
    rows = []

    for _, row in df.iterrows():
        articles = fetch_articles(row["Links"])
        for art in articles:
            rows.append({
                "Company": row["Company"],
                "CSM name": row["CSM name"],
                "Title": art.get("title"),
                "Date": art.get("datePublished"),
                "Link": art.get("url"),
            })

    result_df = pd.DataFrame(rows)
    result_df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()
