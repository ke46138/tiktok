import telebot
from telebot.types import Message
from databaser import Databaser

# Укажите ваш токен бота
BOT_TOKEN = "ne dam ya tebe token"
bot = telebot.TeleBot(BOT_TOKEN)

# Путь к вашей базе данных
DB_PATH = "database.db"

db = Databaser()

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    bot.reply_to(message, "Привет! Отправь мне видео в формате MP4, а также название видео и своё имя.")

# Обработчик видео
@bot.message_handler(content_types=['video'])
def handle_video(message: Message):
    if message.video.mime_type != "video/mp4":
        bot.reply_to(message, "Пожалуйста, отправьте видео в формате MP4.")
        return
    
    video = message.video
    video_id = db.get_last_video_id() + 1

    # Запрашиваем название видео
    msg = bot.reply_to(message, "Какое название у видео?")
    bot.register_next_step_handler(msg, get_title, video_id, video, message.from_user.username)

def get_title(message: Message, video_id, video, username):
    title = message.text

    # Сохраняем видео
    file_info = bot.get_file(video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    video_file_path = f"static/videos/{video_id}.mp4"
    with open(video_file_path, "wb") as f:
        f.write(downloaded_file)

    # Добавляем данные в базу
    db.add_video(title, username, video_id)
    
    bot.reply_to(message, f"Видео '{title}' успешно загружено и сохранено с ID {video_id}!")

def start():
    bot.polling()
