"""CricketData current-matches client; never log API credentials."""
import os
import requests
from dotenv import load_dotenv

ENDPOINT = 'https://api.cricapi.com/v1/currentMatches'

class CricketAPIError(RuntimeError):
    pass

def get_current_matches():
    load_dotenv()
    key = os.getenv('CRICKET_API_KEY', '').strip()
    if not key:
        raise CricketAPIError('CRICKET_API_KEY is missing from .env')
    try:
        response = requests.get(ENDPOINT, params={'apikey': key, 'offset': 0}, timeout=12)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise CricketAPIError('Unable to retrieve cricket scores. Check connectivity and try again.') from exc
    if not isinstance(payload, dict) or payload.get('status') != 'success':
        raise CricketAPIError('Cricket provider did not return a successful response. Check key, quota, and account access.')
    data = payload.get('data')
    if not isinstance(data, list):
        raise CricketAPIError('Unexpected match data from cricket provider.')
    return data

def format_scores(match):
    scores = match.get('score') or []
    if not isinstance(scores, list):
        return 'Score not available'
    result = []
    for entry in scores:
        if not isinstance(entry, dict):
            continue
        inning = str(entry.get('inning') or 'Innings')
        runs = entry.get('r', '–')
        wickets = entry.get('w', '–')
        overs = entry.get('o', '–')
        result.append(f'{inning}: {runs}/{wickets} ({overs} overs)')
    return ' | '.join(result) if result else 'Score not available'
