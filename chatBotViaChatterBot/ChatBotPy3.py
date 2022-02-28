from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

READ_ONLY = True


def get_default_training_data() -> list:
    """all default datasets will exist here to help the bot."""
    small_talk = [
        "hi there!",
        "hi!",
        "how do you do?",
        "how are you?",
        "i'm cool.",
        "fine, you?",
        "always cool.",
        "i'm ok",
        "glad to hear that.",
        "i'm fine",
        "glad to hear that.",
        "i feel awesome",
        "excellent, glad to hear that.",
        "not so good",
        "sorry to hear that.",
        "what's your name?",
        "i'm pybot. ask me a math question, please.",
    ]
    math_talk_1 = [
        "pythagorean theorem",
        "a squared plus b squared equals c squared.",
    ]
    math_talk_2 = [
        "law of cosines",
        "c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)",
    ]
    return [small_talk, math_talk_1, math_talk_2]


class ChatterRobot:
    """Chat bot class vars so far only have chat_bot which is the bot object
    for this class. It takes in a name, a read only variable and a adapter
    for logic.
    """

    def __init__(self, name: str, perms: bool, adapters: list):
        self.chat_bot = ChatBot(
            name=name, read_only=perms, logic_adapters=adapters
        )

    def add_corpus_training(self):
        corpus_trainer = ChatterBotCorpusTrainer(self.chat_bot)
        corpus_trainer.train("chatterbot.corpus.english")

    def add_list_training(self, training_data: list):
        bot_trainer = ListTrainer(self.chat_bot)
        for data_set in training_data:
            bot_trainer.train(data_set)

    def talk_to_bot(self, talk_in_text: str) -> str:
        return self.chat_bot.get_response(talk_in_text)


def test_responses(my_bot: ChatterRobot):
    print(my_bot.talk_to_bot("hi"))
    print(my_bot.talk_to_bot("i feel awesome today"))
    print(my_bot.talk_to_bot("what's your name?"))
    print(my_bot.talk_to_bot("show me the pythagorean theorem"))
    print(my_bot.talk_to_bot("do you know the law of cosines?"))
    print(my_bot.talk_to_bot("what is the most common english letter?"))


def interactive_talk(my_bot):
    while True:
        text_said: str = input("say something to me\n").strip()
        if "quit proc" == text_said:
            return
        print(my_bot.talk_to_bot(text_said))


def main():
    my_bot: ChatterRobot = ChatterRobot(
        "PyBot",
        False,
        [
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.BestMatch",
        ],
    )
    my_bot.add_corpus_training()
    my_bot.add_list_training(get_default_training_data())
    test_responses(my_bot)
    interactive_talk(my_bot)


if __name__ == "__main__":
    main()
