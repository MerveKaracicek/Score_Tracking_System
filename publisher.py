import pika
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures?league=39&season=2020"
HEADERS = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

def get_last_matches():
    url = f"{BASE_URL}"
    response = requests.get(url, headers=HEADERS)
    data = response.json().get("response", [])


    matches = []
    for match in data:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        score = f'{match["goals"]["home"]}-{match["goals"]["away"]}'

        raw_date = match["fixture"]["date"]
        dt = datetime.fromisoformat(raw_date)
        formatted = dt.strftime("%d.%m.%Y %H:%M")

        matches.append({
            "home": home,
            "away": away,
            "score": score,
            "date": formatted
        })
    return matches


def publish():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange="teams", exchange_type="topic")

    matches = get_last_matches()

    for match in matches:
        message = f"{match['date']} | {match['home']} vs {match['away']} => {match['score']}"
        for team in [match["home"], match["away"]]:
            routing_key = f"team.{team.lower().replace(' ', '_')}"
            channel.basic_publish(
                exchange="teams",
                routing_key=routing_key,
                body=message.encode()
            )
            print(f"[→] Gönderildi: {routing_key} → {message}")

    connection.close()


if __name__ == "__main__":
    publish()
