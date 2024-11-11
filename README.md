# Telegram C&C Flipper Zero

Telegram bot for remotely controlling a system via commands.

## Tutorial

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. In the `bot.py` file, replace `TOKEN` with your bot's Telegram token and `AUTHORIZED_USER_ID` with the user ID that will have access.

3. To create a `.exe` executable, run:

   ```bash
   python -m PyInstaller --onefile --noconsole bot.py
   ```

4. Start a local HTTP service in the directory where the executable is located:

   ```bash
   python3 -m http.server 8080
   ```

5. Modify the `executeBotC2C.txt` file if needed.

6. Upload the `.txt` file to the Flipper Zero, connect it, and run it.

7. Open the bot and have fun!
