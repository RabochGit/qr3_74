import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами 
bot = telebot.TeleBot("6494951646:AAHNXF65YbOB0XGw7xF9H-Yx6x1NHnd-45M",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "опрос"  # Можно менять текст 
text_button_1 = "Информация о боте"  # Можно менять текст 
text_button_2 = "Не смешной анегдот"  # Можно менять текст 
text_button_3 = "Куда кидать деньги для развития стартапа"  # Можно менять текст 
text_button_4 = "Запретная конопочка"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Для начала работы бота, вам нужно зарегестрироваться, вы готовы? (желательно ответить да, ибо красивого диалога, при вписывании "нет", не будет, так как я не умею коректно работать с функциями "if, else, elif", поэтому пишите что хотите, но бот воспримет все как да)',
        # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Тогда начнем (я же говорил). *Ваше*')  # Можно менять текст 
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! Ваш `возраст?`')  # Можно менять текст 
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию, бот готов к использованию!',
                     reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Этот бот создан не для какой-то конкретной цели, а лишь для того, чтобы обучится азам програмирования и научится создавать своих телеграм-ботов. Функционала у этого бота также нет.",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "'Зачем тут эта кнопка' спросите вы, а я отвечу 'почему нет', ну а качательно анегдота, то мне лень гуглить, поэтому без анегдота получается)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Во первых положи мамину карточку, а во вторых это не стартап, а лишь тестовый бот для обучения основам такого легкого дела, поэтому ничего ни куда скидывать не надо.",
                     reply_markup=menu_keyboard)  # Можно менять текст

@bot.message_handler(func=lambda message: text_button_4 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Кнопочка запретная, ничего тут не будет.")

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()