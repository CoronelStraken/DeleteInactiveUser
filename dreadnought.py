import telebot
from datetime import datetime, timedelta
from collections import defaultdict
# Aquí colocamos tu token
token = '6974120243:AAGZJKXY0oNVZk03RuTSUbx6rVotuTbmn6k'

# Creamos la instancia del bot
bot = telebot.TeleBot(token)


ultima_actividad_usuario = defaultdict(lambda: datetime.min)

def actualizar_actividad_usuario(message):
    user_id = message.from_user.id
    ultima_actividad_usuario[user_id] = datetime.now()

# Función para eliminar usuarios inactivos
def eliminar_usuarios_inactivos(chat_id, dias_inactividad):
    ahora = datetime.now()
    if len(ultima_actividad_usuario)==0:
        bot.send_message(chat_id, f"No existen nuevos mensajes capturados por el bot")

    for user_id, ultima_actividad in ultima_actividad_usuario.items():
        tiempo_inactividad = (ahora - ultima_actividad).days
        if tiempo_inactividad > dias_inactividad:
            try:
                bot.kick_chat_member(chat_id, user_id)
                bot.send_message(chat_id, f"Usuario {user_id} eliminado por inactividad.")
            except Exception as e:
                bot.send_message(chat_id, f"No se pudo eliminar al usuario {user_id}: {e}")

# Comando para limpiar usuarios inactivos
@bot.message_handler(commands=['limpiar'])
def limpiar_usuarios_inactivos(message):
    chat_id = message.chat.id
    # Aquí puedes especificar el número de días de inactividad antes de eliminar a un usuario
    dias_inactividad = 1
    eliminar_usuarios_inactivos(chat_id, dias_inactividad)
    bot.reply_to(message, "Usuarios inactivos eliminados con éxito.")

# Comando de inicio
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Soy un bot para eliminar usuarios inactivos en un grupo.')
    actualizar_actividad_usuario(message)  # Actualizar la actividad del usuario al enviar el comando /start

# Manejador de mensajes
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text.startswith('/'):
        # Si el mensaje es un comando, ejecutar solo la función para actualizar la actividad del usuario
        actualizar_actividad_usuario(message)
    else:
        # Si no es un comando, ejecutar todas las funciones de manejo de mensajes
        actualizar_actividad_usuario(message)
        bot.process_new_messages([message])

# Ejecutar el bot
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
