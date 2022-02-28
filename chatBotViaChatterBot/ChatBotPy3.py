from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

READ_ONLY = True


def get_default_training_data() -> list:
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


def main():
    math_args: str = "chatterbot.logic.MathematicalEvaluation"
    best_args: str = "chatterbot.logic.BestMatch"
    bot_name: str = "PyBot"
    perms: bool = READ_ONLY
    adapters: list = [math_args, best_args]
    my_bot: ChatterRobot = ChatterRobot(bot_name, perms, adapters)
    my_bot.add_corpus_training()
    my_bot.add_list_training(get_default_training_data())


main()
