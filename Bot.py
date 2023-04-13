import telebot
from telebot import types
import sqlite3 as sq


bot = telebot.TeleBot('6141229023:AAH-wZoozuTLCZchBIdPYZ8oVg3NsCZQJAU')

class Test:
  def __init__(self, name, question, answer1, answer2, answer3, answer4):
    self.name = name
    self.question = question
    self.answer1 = answer1
    self.answer2 = answer2
    self.answer3 = answer3
    self.answer4 = answer4


  def get_message_text(self):
    return self.question

  def get_inline_keyboard(self):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    answer1_button = types.InlineKeyboardButton(text=f'{self.answer1}', callback_data=f'{self.answer1}')
    answer2_button = types.InlineKeyboardButton(text=f'{self.answer2}', callback_data=f'{self.answer2}')
    answer3_button = types.InlineKeyboardButton(text=f'{self.answer3}', callback_data=f'{self.answer3}')
    answer4_button = types.InlineKeyboardButton(text=f'{self.answer4}', callback_data=f'{self.answer4}')
    inline_keyboard.add(answer1_button, answer2_button, answer3_button, answer4_button)

    return inline_keyboard

  def set_right_answer(self, answer):
    self.right_answer = answer


  def get_name(self):
    return self.name





def info(message):
  if message.text == 'История компании':
    info_file = open('F:\Рабочий стол\BotResourses\TextFiles\Information\CompanyInfo.txt', 'r', encoding='utf-8')
    bot.send_message(message.chat.id, info_file.read())

    msg = bot.send_message(message.from_user.id, "Что вам интересно?")
    bot.register_next_step_handler(msg, info)

  elif message.text == 'Сотрудники':
    info_file = open("F:\Рабочий стол\BotResourses\TextFiles\Information\StaffInfo.txt",  'r', encoding='utf=8')
    bot.send_message(message.chat.id, info_file.read())

    msg = bot.send_message(message.from_user.id, "Что вам интересно?")
    bot.register_next_step_handler(msg, info)

  elif message.text == "На главный экран":
    start(message)


  elif message.text == "Продуктовакя линейка":
    info_file = open("F:\Рабочий стол\BotResourses\TextFiles\Information\AdvantageInfo.txt", 'r', encoding='utf=8')
    bot.send_message(message.chat.id, info_file.read())

    msg = bot.send_message(message.from_user.id, "Что вам интересно?")
    bot.register_next_step_handler(msg, info)


def job(message):
  if message.text == "На главный экран":
    start(message)

  elif message.text == "Теория":
    info_file = open("F:\Рабочий стол\BotResourses\TextFiles\Information\Theory.txt")
    bot.send_message(message.chat.id, info_file.read())
    msg = bot.send_message(message.from_user.id, 'Выбирете дальнейшее действие:  ')
    bot.register_next_step_handler(msg, job)




  elif message.text == 'Начать тест':
    Tests = []
    with sq.connect('dataBase.db') as connect:
      cursor = connect.cursor()

      cursor.execute("SELECT * FROM Test")
      test_name_counter = 1
      for result in cursor:
        Test1 = Test(f'Вопрос #{test_name_counter}', f'{result[0]}', f'{result[1]}', f'{result[2]}', f'{result[3]}', f'{result[4]}')
        Test1.set_right_answer(f'{result[5]}')
        Tests.append(Test1)
        test_name_counter += 1

        print(result)


    for i in range(len(Tests)):
      bot.send_message(message.chat.id, Tests[i].get_message_text(), reply_markup=Tests[i].get_inline_keyboard())

    msg = bot.send_message(message.from_user.id, 'Выбирете дальнейшее действие:  ')
    bot.register_next_step_handler(msg, job)


    @bot.callback_query_handler(func=lambda callback: callback.data)
    def check_test(callback):

      for i in range(len(Tests)):
        if callback.data == Tests[i].right_answer:
          bot.send_message(callback.message.chat.id, f'{Tests[i].name}: Верно')



@bot.message_handler(commands=['start'])
def start(message):
  start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                            row_width=1)  # row_width=1 - количество кнопок в строке
  start_button1 = types.KeyboardButton(text='Основные сотрудники')
  start_button2 = types.KeyboardButton(text='Должность')
  start_button3 = types.KeyboardButton(text='Информация о компании')
  start_keyboard.add(start_button1, start_button2, start_button3)

  bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=start_keyboard)


def check_access(cursor, message):
  username = message.from_user.username
  cursor.execute("""SELECT * FROM Staff WHERE tg_tag = '{}';""".format(username))
  if cursor.fetchone() is None:
    try:
      uid = int(message.text)
      cursor.execute("""SELECT * FROM Staff WHERE id = {}""".format(uid))
      if not cursor.fetchone() is None:
        cursor.execute("""UPDATE Staff SET tg_tag = '{0}' WHERE id = {1}""".format(username, uid))
        bot.send_message(message.chat.id, """Вы успешно авторизовались в системе, доступ к пользованию ботом получен!""")
        return True
      else:
        bot.send_message(message.chat.id, """Введенный код сотрудника неверный или более недействительный. Проверьте правильность ввода и попробуйте снова.""")
        return False
    except:
      bot.send_message(message.chat.id, "Данный бот создан исключительно для пользования сотрудниками кампании Noname Pizzeria. Если вы являетесь сотрудником, то отправьте в чат свой код доступа для начала работы.")
      return False
    return
  return True

@bot.message_handler(func=lambda message: True) #func=lambda message = True - бот отвечает на любое сообщение
def menu_message(message):
  with sq.connect('dataBase.db') as connect:
    cursor = connect.cursor()
    #access = check_access(cursor, message)
    #if not access: return
    if message.text == 'Информация о компании':
      info_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
      info_button1 = types.KeyboardButton(text='История компании')
      info_button2 = types.KeyboardButton(text='Сотрудники')
      info_button3 = types.KeyboardButton(text='Продуктовакя линейка')
      info_button4 = types.KeyboardButton(text='На главный экран')
      info_keyboard.add(info_button1, info_button2, info_button3, info_button4)
      msg = bot.send_message(message.from_user.id, "Что вам интересно?", reply_markup=info_keyboard)
      bot.register_next_step_handler(msg, info)

    elif message.text == 'Основные сотрудники':
      cursor.execute("SELECT * FROM Staff")
      for result in cursor:

        bot.send_message(message.chat.id, f"Сотрудник: {result[3]} \nДолжность: {result[1]} \nТелеграм: {result[2]}",)
        print(result)

    elif message.text == "Должность":
      test_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
      test_button1 = types.KeyboardButton(text='На главный экран')
      test_button2 = types.KeyboardButton(text='Начать тест')
      test_button3 = types.KeyboardButton(text='Теория')
      test_keyboard.add(test_button1, test_button2, test_button3)

      msg = bot.send_message(message.from_user.id, 'Вы можете пройти тест, просмотреть теорию, либо вернуться на главный экран:', reply_markup=test_keyboard)
      bot.register_next_step_handler(msg, job)





bot.infinity_polling()