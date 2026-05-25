import requests
import json

def get_latest_midi_methods():
    """
    Queries the GitHub Search API for trending codebase patches 
    and optimizations related to FL Studio's script variables.
    """
    # Load configuration parameters
    with open('config.json', 'r') as f:
        config = json.load(f)
        
    query_terms = "+".join(config["github_pipeline"]["search_queries"])
    url = f"https://api.github.com/search/repositories?q={query_terms}&sort=updated"
    
    try:
        res = requests.get(url, headers={"User-Agent": "EPIC-STUDIOS-Scraper"})
        if res.status_code == 200:
            items = res.json().get('items', [])
            context_payload = []
            for item in items[:config["github_pipeline"]["results_limit"]]:
                context_payload.append({
                    "name": item["name"],
                    "url": item["html_url"],
                    "description": item["description"]
                })
            return json.dumps(context_payload, indent=2)
    except Exception as e:
        return f"Error updating scraper context: {e}"
    
    return "[]"
