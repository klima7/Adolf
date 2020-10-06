# 🥓🥩🍗🍖🍣🍤🥛🍼🐟🐁🐀

happy_cat_sound = ['meow', 'mrow', 'mrrr', 'mrrrawr', 'miau', 'wrrrau']
start_petting = ['Oo, głaskanie 😻', 'Taak, pogłaskaj 😻', 'Taak, trzeba mnie głaskać 😻']
stop_petting = ['Dlaczego przestałeś głaskać? 😿', 'Głaskaj! 😿', 'Jeszcze troszkę 😿']
thanks_petting = ['Dziękuje, już wystarczy 😽', 'Doskonale 😻']
dont_change_emoji = ['Nie zmieniaj emoji, drap, drap 😾', 'Nie zmieniaj, bo cię podrapię 😾', 'Wolałem tamto emoji! 😾', 'Wrau, chce tamto! 😾']

meal_good = ['To było pyszcze jedzonko 😻', 'Przepyszne 😻', 'Mraaał, dobre 😻 Dziękuje 😽']
meal_need = ['Jestem głodny 😿', 'Daj mi coś do jedzenia 😿', 'Potrzebuje jedzonko 😿']
meal_enough = ['Jestem już najedzony 😸', 'Nie, dziękuje, objadłem się 😸', 'Już mi wystarczy jedzonka 😸']

drink_good = ['Dziękuje, chciało mi się pić 😽', 'Pyszne pićko 😽']
drink_need = ['Chce mi się pić 😿', 'Potrzebuje pićko 😿']
drink_enough = ['Nie chce mi się już pić 😸', 'Wystarczy mi już picia 😸']

toy_good = ['Miau, ale fajna zabawa 😻', 'Uwielbiam się z Tobą bawić 😻']
toy_need = ['Chce się pobawić, Mrau 😿', 'Pobaw się ze mną, potrzebuje atencji 😿', 'Nudzi mi się, pobawmy się 😿']
toy_enough = ['Mam na razie dość zabawy 😸', 'Wystarczy zabawy na razie 😸', 'Nie mam już siły na dalszą zabawę 😸']

poopy_good = ['Miał, w końcu się załatwiłem 😺', 'W końcu mi ulżyło 😺']
poopy_need = ['Muszę zrobić kupkę 😿', 'Bardzo chce mi się siusiu 😿']
poopy_enough = ['Na razie nie potrzebuje robić kupkę 😸', 'Dopiero co robiłem kupkę 😸']

dont_want = ['Nie mam teraz ochoty na {} 😾 Chcę coś innego', 'Nie mam chęci na {}, chcę coś innego 😾']


class Texts:
    def __getattr__(self, item):
        import sys
        from random import choice
        try:
            module = sys.modules[__name__]
            return choice(getattr(module, item))
        except Exception:
            return '💀 Błąd - niepoprawny tekst 💀'


texts = Texts()
