import re
import inspect
import fbchat as fb
from app.policy import *


registered_regex = {}


def repeal(fun):
    def do_nothing(*args, **kwargs):
        pass
    return do_nothing


def elite_group_only(fun):
    def fake_fun(*args, **kwargs):
        matched_args = inspect.getcallargs(fun, *args, **kwargs)
        self = matched_args['self']
        thread_id = matched_args['thread_id']
        thread_type = matched_args.get('thread_type', fb.ThreadType.GROUP)
        author_id = matched_args['author_id']

        if author_id == self.uid:
            return
        if thread_id == ELITE_GROUP_ID:
            fun(*args, **kwargs)
        elif thread_type == fb.ThreadType.USER:
            self.meow_stranger(thread_id, thread_type)
    return fake_fun


def register_regex(regex):
    def real_decorator(fun):
        compiled_re = re.compile(regex, re.IGNORECASE)
        registered_regex[compiled_re] = fun
        return fun
    return real_decorator
