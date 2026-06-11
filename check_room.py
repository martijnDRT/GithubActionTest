import requests
from pathlib import Path
 
API_URL = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=Z8Sv6"
TARGET_USERNAME = "mayaforyou247"  # <-- Change this to the username you want to check
DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1514040203319185418/tRnqUPcKNjOsT0YFiw3UGlgRAKt960-_WPoxUA8gpZQn6TbgR7xl1Vqz8uDwPxrHnyai"
 
# File to persist online/offline state between runs
STATE_FILE = Path("state.txt")  # contains "online" or "offline"
 
 
def get_online_usernames(url: str) -> list[str]:
    """Fetch the API and return a list of all online usernames."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
 
    # The API returns either a list directly or a dict with a 'results' key
    rooms = data if isinstance(data, list) else data.get("results", [])
 
    usernames = [room["username"] for room in rooms if "username" in room]
    return usernames
 
 
def check_user_online(username: str, usernames: list[str]) -> bool:
    """Check if a specific username is in the list of online users."""
    return username.lower() in [u.lower() for u in usernames]
 
 
def send_discord_notification(username: str):
    """Send a Discord message via webhook when the room goes online."""
    payload = {
        "content": f"🟢 **{username}** is now ONLINE on Chaturbate!\nhttps://chaturbate.com/{username}/"
    }
    response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
    response.raise_for_status()
    print(f"Discord notification sent for '{username}'.")
 
 
def get_previous_state() -> str:
    """Read the last known state from file. Defaults to 'offline'."""
    if STATE_FILE.exists():
        return STATE_FILE.read_text().strip()
    return "offline"
 
 
def save_state(state: str):
    """Persist the current state ('online' or 'offline') to file."""
    STATE_FILE.write_text(state)
 
 
def check():
    """Main logic: check room, compare with last state, notify if newly online."""
    usernames = get_online_usernames(API_URL)
    is_online = check_user_online(TARGET_USERNAME, usernames)
    previous_state = get_previous_state()
 
    print(f"Username   : {TARGET_USERNAME}")
    print(f"Currently  : {'ONLINE' if is_online else 'OFFLINE'}")
    print(f"Last state : {previous_state.upper()}")
 
    if is_online:
        if previous_state == "offline":
            # Was offline before → just came online → send notification
            print("State changed offline → online. Sending Discord notification...")
            send_discord_notification(TARGET_USERNAME)
        else:
            print("Already notified. Skipping Discord message.")
        save_state("online")
    else:
        print("Room is offline. No notification needed.")
        save_state("offline")
 
 
if __name__ == "__main__":
    check()
