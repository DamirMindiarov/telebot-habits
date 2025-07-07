from telebot.util import quick_markup

buttons = {
    "🔔Вкл / 🔕Выкл": {"callback_data": "cb_notifications"},
}
keyboard = quick_markup(buttons)