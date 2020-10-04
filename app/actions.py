from app.bot import client
from app.jbzd import fetch_memes_page


def send_memes(uid):
    memes = fetch_memes_page(1)
    client.sendRemoteFiles(memes, thread_id=uid)
