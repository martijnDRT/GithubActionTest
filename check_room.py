import requests, os, pathlib

USERNAME = "mayaforyou247"
# os.environ["CB_USERNAME"]
WEBHOOK  = "https://discordapp.com/api/webhooks/1514000611513864382/foeBVNhf0m1PmVh_mEcGeWMUHuWZZQMXMMbkT5NNgoYleDVsXSTB0NrDQGoEvfUbkv7u"
# os.environ["DISCORD_WEBHOOK"]
# STATE    = pathlib.Path("last_state.txt")

def is_online():
    r = requests.get(
        "https://chaturbate.com/api/public/affiliates/onlinerooms/",
        params={"wm": "NONE", "limit": 500},
        timeout=10
    )
    rooms = [x["username"].lower() for x in r.json()["results"]]
    return USERNAME.lower() in rooms

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
