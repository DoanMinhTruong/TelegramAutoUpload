import telebot
from telebot.types import InputMediaPhoto
def is_valid_bot(token):
    bot = telebot.TeleBot(token)
    try:
        bot.get_me()
        return True
    except telebot.apihelper.ApiException:
        return False
    


def is_from_one_bot(link_telegram, token):
    # Kiểm tra xem link Telegram và Token có phải là của cùng 1 bot không
    bot = telebot.TeleBot(token)
    try:
        me = bot.get_me()
        username = me.username.lower()
        link = link_telegram.lower()

        # Compare the link directly with the bot's username
        if link.endswith(username):
            return True
        else:
            return False
    except telebot.apihelper.ApiException:
        return False
    

def bot_sendto_channel(bot_token , channel_id ,images, message):
    bot = telebot.TeleBot(bot_token)
    # channel_link = "@" + channel_link.split('/')[-1]
    try:
        all_photos = []
        for i in range(len(images)):
            all_photos.append(InputMediaPhoto(open(images[i], 'rb'), caption = message if i == 0 else '' , parse_mode="MARKDOWN") )
            print("ok")
        bot.send_media_group(chat_id=channel_id,media=all_photos)
    except Exception as e:
        print(f"Lỗi: {e}")
        return None
def bot_sendto_channel_no_images(bot_token , channel_link , message):
    bot = telebot.TeleBot(bot_token)
    channel_link = "@" + channel_link.split('/')[-1]
    try:
        
        bot.send_message(chat_id=channel_link, text=message, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi: {e}")
        return None

def get_channel_id(bot_token , channel_link):
    bot = telebot.TeleBot(bot_token)
    channel_link = "@" + channel_link.split('/')[-1]
    try:
        message = bot.send_message(channel_link, 'temporary message')
        channel_id = message.chat.id
        bot.delete_message(channel_id, message.message_id)
        return channel_id
    except Exception as e:
        print(f"Lỗi: {e}")
        return None
    
def get_bot_id(bot_token):
    bot = telebot.TeleBot(bot_token)
    try:
        bot_info = bot.get_me()
        bot_id = bot_info.id
        return bot_id
    except Exception as e:
        print(f"Lỗi: {e}")
        return None
    

def check_bot_in_channel(bot_token,channel_link, bot_link):
    bot = telebot.TeleBot(bot_token)
    try:
      channel_id = get_channel_id(bot_token , channel_link)
      bot_id = get_bot_id(bot_token)
      chat_member = bot.get_chat_member(channel_id,bot_id)
      if chat_member.status == 'member' or chat_member.status == 'administrator':
          return True
      else:
          return False
    except Exception as e:
        return False