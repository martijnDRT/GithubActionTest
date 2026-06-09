import requests, os, pathlib

USERNAME =  os.environ["CB_USERNAME"]
WEBHOOK  = os.environ["DISCORD_WEBHOOK"]
# STATE    = pathlib.Path("last_state.txt")

# def is_online():
API_URL = "https://chaturbate.com/affiliates/api/onlinerooms/"
AFFILIATE_ID = "Z8Sv6"  # your wm code

def is_online(username):
    params = {
        "format": "json",
        "wm": AFFILIATE_ID
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    data = response.json()
    rooms = data.get("rooms", [])

    for room in rooms:
        if room.get("username", "").lower() == username.lower():
            return True

    return False
def notify():
    requests.post(WEBHOOK, json={
        "content": f"🟢 **{USERNAME}** is live on Chaturbate!\nhttps://chaturbate.com/{USERNAME}/"
    })

# was_online = STATE.exists() and STATE.read_text().strip() == "online"
was_online = False
online_now = is_online()

if online_now and not was_online:
    notify()
    print("Notification sent")
    was_online = online_now
else:
    was_online = online_now
    print("Online" if online_now else "Offline — no notification sent")

STATE.write_text("online" if online_now else "offline")
