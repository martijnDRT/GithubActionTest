import requests, os, pathlib

USERNAME =  os.environ["CB_USERNAME"]
WEBHOOK  = os.environ["DISCORD_WEBHOOK"]
# STATE    = pathlib.Path("last_state.txt")

def is_online():

    url = "https://chaturbate.com/api/public/affiliates/onlinerooms/?format=json"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # The API returns a dict with a key "rooms"
    rooms = data.get("rooms", [])

    for room in rooms:
        if room.get("username", "").lower() == model_username.lower():
            return True

    return False
    # url = "https://chaturbate.com/api/public/affiliates/onlinerooms/?format=json"
    # rooms = requests.get(url).json()

    # for room in rooms:
    #     if room.get("username", "").lower() == model_username.lower():
    #         return True

    # return False
    # # r = requests.get(
    # #     "https://chaturbate.com/api/public/affiliates/onlinerooms/",
    # #     params={"wm": "NONE", "limit": 500},
    # #     timeout=10
    # # )
    # # rooms = [x["username"].lower() for x in r.json()["results"]]
    # # return USERNAME.lower() in rooms

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
