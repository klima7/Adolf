import app.util.schedule as schedule
from app import client
import fbchat as fb
from app.policy import *


@schedule.periodically('0 0:0:5')
def miau():
    client.sendMessage('Miau', thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
