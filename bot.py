import os
import telebot


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(
            message.chat.id, "👋 Привет, если хочешь узнать свою оценку, напиши мне свое ФИО и группу. В будущем ты сможешь просто писать 'Оценки'")

    bot.polling()


def main():
    token = os.getenv('TOKEN')

    telegram_bot(token)


if __name__ == '__main__':
    main()