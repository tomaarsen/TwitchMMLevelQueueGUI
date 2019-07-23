# TwitchMMLevelQueueGUI
 Twitch bot which create a queue for Mario Maker 2 Levels from chat, with a GUI

---

# Explanation
When the bot has started, it will open up this GUI:

![image](https://user-images.githubusercontent.com/37621491/60526875-7d9cf300-9cf1-11e9-9e9b-305d307e6e69.png)

The bot connected to this GUI will, when "Run" is pressed, allow chat members to add their levels to a queue. When the streamer wishes to play a level, they can play the first level of the queue. This level will also be available for chatters to access by the use of a command.

In short, this bot allows streamers to fairly pick chat levels with just one click.

This bot is similar to my [Twitch Mario Maker Level Picker](https://github.com/CubieDev/TwitchMMLevelPickerGUI). However, the bot in this repository uses a queue that does not give advantages to subscribers, while the [Level Picker](https://github.com/CubieDev/TwitchMMLevelPickerGUI) semi-randomly picks levels from the list of all added levels, giving better odds to people who have been subscribed for longer.

--- 

# Commands

<pre>
<b>!addlevel XXX-XXX-XXX</b>
</pre>
- Adds the level with code XXX-XXX-XXX to the queue.<br>
- Anyone can use this.
---
<pre>
<b>!nextlevel</b>
</pre>
- Changes the current level to the next level.<br>
- Anyone with the allowed rank can use this. (See [Settings](https://github.com/CubieDev/TwitchMMLevelQueueGUI#Settings) for more information)
---
<pre>
<b>!level/!current/!currentlevel</b>
</pre>
- Shows the creator and code of the current level in the chat.
- Anyone can use this.
---
<pre>
<b>!clearlevel</b>
</pre>
- Clears the queue of levels
- Anyone with the allowed rank can use this. (See [Settings](https://github.com/CubieDev/TwitchMMLevelQueueGUI/blob/master/README.md#Settings) for more information)
---
<pre>
<b>!levelhelp/!helplevel</b>
</pre>
- Shows information about the commands everyone can use.
- Anyone can use this.
---
<pre>
<b>!queue</b>
</pre>
- Shows where the user is in the queue.
- Anyone can use this.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "AllowedRanks": [
        "broadcaster",
        "moderator"
    ],
    "AllowedPeople": []
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| AllowedRanks  | List of ranks required to be able to perform the commands. | ["broadcaster", "moderator"] |
| AllowedPeople | List of users who, even if they don't have the right ranks, will be allowed to perform the commands. | ["cubiedev"] |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# GUI
For reference, this is the GUI:

![image](https://user-images.githubusercontent.com/37621491/60526875-7d9cf300-9cf1-11e9-9e9b-305d307e6e69.png)

Let's clarify the functionality from the GUI:

| **Button** | **Action** |
| ---------- | ----------- |
| Auth | This button will hide or unhide your Authentication token. This way you can hide it when you aren't changing it, so that it will not leak. |
| Run | This button is both "Stop" and "Run" at the same time. When the bot is running, the button will say Stop. While it is not, it will display "Run". Pressing this button will either stop the bot from running, or start the bot using the information filled in above. | 
| Move to Next Level | Equivalent to typing `!nextlevel` in chat. Picks the next level. |
| Clear: <date> | Clears the list of levels. The date shows when the list of levels was last cleared. |

In addition to these buttons, there is a textbox which will automatically fill with chat levels. This textbox represents the queue. The #1 item in the queue will be the current level used by `!currentlevel`, and shows up as bold.

---

# Requirements
* Python 3+ (Only tested on 3.6)

Download Python online.

* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchUrbanDictionary](https://github.com/CubieDev/TwitchUrbanDictionary)
* [TwitchWeather](https://github.com/CubieDev/TwitchWeather)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
