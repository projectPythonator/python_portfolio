from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


def spawn_bot(name: str, access: bool, adapters: list) -> ChatBot:
    return ChatBot(name=name, read_only=access, logic_adapters=adapters)


def get_training_data() -> list:
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
    math_question: str = "pythagorean theorem"
    math_answer: str = "a squared plus b squared equals c squared."
    math_talk_1 = [math_question, math_answer]
    math_question: str = "law of cosines"
    math_answer: str = "c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)"
    math_talk_2 = [math_question, math_answer]

    return [small_talk, math_talk_1, math_talk_2]


def train_bot(training_data: list, my_bot: ChatBot):

    corpus_trainer = ChatterBotCorpusTrainer(my_bot)
    corpus_trainer.train("chatterbot.corpus.english")
    bot_trainer = ListTrainer(my_bot)
    for data_set in training_data:
        bot_trainer.train(data_set)


def test_responses(my_bot: ChatBot):
    print(my_bot.get_response("hi"))
    print(my_bot.get_response("i feel awesome today"))
    print(my_bot.get_response("what's your name?"))
    print(my_bot.get_response("show me the pythagorean theorem"))
    print(my_bot.get_response("do you know the law of cosines?"))
    print(my_bot.get_response("what is the most common english letter?"))


def main():
    math_str: str = "chatterbot.logic.MathematicalEvaluation"
    best_str: str = "chatterbot.logic.BestMatch"
    bot_name: str = "PyBot"
    read_access: bool = True
    adapters: list = [math_str, best_str]
    my_bot = spawn_bot(bot_name, read_access, adapters)
    train_bot(get_training_data(), my_bot)
    test_responses(my_bot)


main()
