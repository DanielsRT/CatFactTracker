import requests

FACTS_URL = 'https://catfact.ninja/fact'
FACT_COUNT = 5

def fetch_cat_fact():
    try:
        response = requests.get(FACTS_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('fact')
    except requests.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None
    
def main():
    fetched_facts = set()

    while len(fetched_facts) < FACT_COUNT:
        fact = fetch_cat_fact()
        if fact not in fetched_facts:
            fetched_facts.add(fact)
            print(f"Fetched fact: {fact}")
        else:
            print("Fact already exists, fetching a new one...")

if __name__ == "__main__":
    main()