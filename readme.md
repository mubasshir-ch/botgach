# Botgach: A Discord Music Bot
> **Note:** It is not maintained project and was made long ago, it might not work now.

Botgach is a Discord music bot built using `discord.py`. It allows users to play music from YouTube and manage playlists in their Discord servers. Originally created as a personal project, it has functionalities such as looping, queue management, and more.

## Features
- **Play Music**: Search and play songs directly from YouTube.
- **Queue Management**: Add, remove, and reorder songs in the queue.
- **Looping**: Loop a single song or the entire queue.
- **Voting System**: Optional voting system for skipping, clearing the queue, or leaving the voice channel.
- **Custom Prefix**: Change the command prefix for your server.
- **Error Handling**: Graceful handling of errors with user-friendly messages.
- **Developer Commands**: For loading, unloading, and reloading bot modules.

## Setup Instructions

### Prerequisites
1. Python 3.8 or higher.
2. `ffmpeg` installed and added to your PATH.
3. A Discord bot token. Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications).

### Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd botgach
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up configuration:
   - Rename `config.dat.example` to `config.dat` (if provided).
   - Update the `BOT_TOKEN`, `BOT_ID`, and `DEV_ID` fields in `config.dat`.

### Running the Bot
1. Start the bot using:
   ```bash
   python main.py
   ```
2. Invite the bot to your server using the OAuth2 link from the Discord Developer Portal.

## Usage

### Basic Commands
- **Play a Song**:
  ```
  &play <song name or URL>
  ```
- **Pause/Resume**:
  ```
  &pause
  ```
- **View Queue**:
  ```
  &queue
  ```
- **Skip Song**:
  ```
  &skip
  ```
- **Change Command Prefix** (admin-only):
  ```
  &changeprefix <new prefix>
  ```

### Developer Commands
- **Load a Module**:
  ```
  &load <module_name>
  ```
- **Unload a Module**:
  ```
  &unload <module_name>
  ```
- **Reload a Module**:
  ```
  &reload <module_name>
  ```

## File Structure
- `main.py`: Entry point for the bot.
- `Cogs/`: Contains various bot commands and event listeners.
  - `song.py`: Music playback and queue management.
  - `prop.py`: Configuration commands like changing prefixes.
  - `error.py`: Error handling.
  - `help.py`: Placeholder for help commands.
- `botmodules/`: Utility modules for additional functionalities.
  - `config.py`: Handles bot and server configurations.
  - `video.py`: Fetches YouTube video data.
  - `check.py`: Command checks for permissions and states.
- `requirements.txt`: Python dependencies.
- `Procfile`: For deployment on platforms like Heroku.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.


---

