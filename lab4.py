import pymysql
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction


# define a command handler. Command handlers usually take two arguments:
# bot and update
def start(bot, update):
    update.message.reply_text("Welcome to AmITaskList222843_bot!")


# /showTasks
def show(bot, update):
    cursor = conn.cursor()

    sql = 'SELECT todo FROM TASK.taskDB;'

    cursor.execute(sql)

    res = cursor.fetchall()

    update.message.reply_text("That's the task list:")

    if len(res) == 0:
        update.message.reply_text("No tasks in the list.")
    else:
        for row in res:
            for el in row:
                update.message.reply_text("-" + el)

    cursor.close()


# /newTask
def new(bot, update, args):
    cursor = conn.cursor()

    sql = 'SELECT todo FROM TASK.taskDB;'

    cursor.execute(sql)

    res = cursor.fetchall()
    cursor.close()

    no = len(res)

    cursor1 = conn.cursor()

    to_add = ""
    i = 0

    for el in args:
        if i >= 1:
            to_add = to_add + " " + el
            i = i + 1
        else:
            to_add = el
            i = i + 1

    flag = 1

    for cancel in res:
        for el in cancel:
            if el == to_add:
                flag = 0

    if flag == 0:
        update.message.reply_text("Task is already present in the list.")
    else:
        sql = "INSERT INTO TASK.taskDB (todo, id) VALUES (%s, %s);"
        cursor1.execute(sql, (to_add, no))
        update.message.reply_text("The new task was successfully added to the list!")

    cursor1.close()


# /remove
def remove(bot, update, args):
    cursor = conn.cursor()

    sql = 'SELECT todo FROM TASK.taskDB;'

    cursor.execute(sql)

    res = cursor.fetchall()
    cursor.close()

    no = len(res)

    cursor1 = conn.cursor()

    to_remove = ""
    i = 0

    for el in args:
        if i >= 1:
            to_remove = to_remove + " " + el
            i = i + 1
        else:
            to_remove = el
            i = i + 1

    flag = 0

    for cancel in res:
        for el in cancel:
            if el == to_remove:
                flag = 1

    if flag == 0:
        update.message.reply_text("The task you want to delete is not present in the list!")
    else:
        sql = 'DELETE FROM TASK.taskDB WHERE todo=%s;'
        cursor1.execute(sql, to_remove)
        update.message.reply_text("The task has been successfully deleted from the list!")

    cursor1.close()


# /removeAll
def remove_all(bot, update):
    # send the message back

    cursor = conn.cursor()

    sql = 'SELECT todo FROM TASK.taskDB;'

    cursor.execute(sql)

    res = cursor.fetchall()
    cursor.close()

    no = len(res)

    if no == 0:
        update.message.reply_text("I did not find any task to delete!")
    else:
        cursor1 = conn.cursor()
        sql = 'DELETE FROM TASK.taskDB'

        cursor1.execute(sql)
        cursor1.close()
        update.message.reply_text("Every task has been deleted.")


# error
def error(bot, update):
    # simulate typing from the bot
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I am sorry, but I cannot do that")


def main():
    """
    The AmIBot will implement the ex3-lab2)
    """
    # create the EventHandler and pass it your bot's token
    updater = Updater("597694260:AAEDiSFhXrCpofa4B1pzwBEnquBMicx1g5g")

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # add the command handler for the "/start" command
    dp.add_handler(CommandHandler("start", start))

    # / showTasks
    dp.add_handler(CommandHandler("showTasks", show))

    # /newTask < task to add >
    dp.add_handler(CommandHandler("newTask", new, pass_args=True))

    # /removeTask < task to remove >
    dp.add_handler(CommandHandler("removeTask", remove, pass_args=True))

    # /removeAllTasks < substring to use  to remove all  the  tasks that contain it >
    dp.add_handler(CommandHandler("removeAllTasks", remove_all))

    # error
    dp.add_handler(MessageHandler(Filters.text, error))

    # start the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    conn = pymysql.connect(user="root", password="root", database="lab4", host="localhost")

    main()
    conn.close()
