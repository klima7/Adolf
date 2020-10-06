import fbchat as fb
import time

import app.util.jbzd as jbzd
import app.util.schedule as schedule
from app.memory import memory
from app.policy import *
from app import client
import app.util.cats as cats


@schedule.daily('22:00:00')
def event_send_best_memes():
    memes = jbzd.get_best_memes(9, memory.memes_last_day_url, 20)
    memory.memes_page = 2
    memes_url = [meme.url for meme in memes]
    memes_pluses = [meme.pluses for meme in memes]
    print(memes_pluses)
    client.sendMessage('Memy, memy, memy 😻', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    client.sendMessage('Mam dla was dzisiajsze najlepsze memy 😺', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    client.sendRemoteFiles(memes_url, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)


@schedule.daily('23:00:00')
def event_goodnight():
    client.sendMessage('Dobranoc, ja lecę spać 😽💤', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    time.sleep(2)
    client.sendMessage('Kocham was całym serduszkiem 😻', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    time.sleep(3)
    client.send(fb.Message(text="❤", emoji_size=fb.EmojiSize.LARGE), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)


@schedule.daily('5:00:00')
def event_goodmorning():
    client.sendMessage('Miał, miał, dzieńdobry 😺', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)


@schedule.daily('5:20:00')
def event_start_job():
    client.sendMessage('Powodzenia w pracy króliczku 😽', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)


@schedule.daily('10:00:00')
def event_start_job():
    client.sendMessage('Chyba masz przerwę w pracy 😽', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    cats_url = cats.get_random_cats(6, type=cats.CatType.STATIC)
    client.sendRemoteFiles(cats_url, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    client.sendMessage('Masz tu kotki na dobry humor 😽', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
