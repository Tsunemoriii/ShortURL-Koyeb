import os


API_HASH = os.environ.get("API_HASH", "ce54eacb9b6854768b06daa2864e88fa")
API_ID = int(os.environ.get("API_ID", 4560655))
AUTH_USERS = list(filter(lambda x: x, map(int, os.environ.get("AUTH_USERS", "5672065955 1432756163 682111519 1446111611").split())))
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://SonicOtakus:imindian@cluster0.lfpjg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1001191707498))


# Bot tokens
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6253943582:AAG_JMy30lQn7rMpOs1pwRa_v5i_ZlzeEHw")
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2", "6051155351:AAFTIzVQEytmfPAFZX7OCH60hkP3hCmoQE4")
BOT_TOKEN_3 = os.getenv("BOT_TOKEN_3", "6086088634:AAH-OOsdwcbDJ4dFC5B1NsskaR7uCCoLyPc")
BOT_TOKEN_4 = os.getenv("BOT_TOKEN_4", "6225070483:AAE6dKan-ump5yNVhXbva1OkAJ0UQNXbu7I")
BOT_TOKEN_5 = os.getenv("BOT_TOKEN_5", "5990317516:AAEg4lkBRp1WgqWT8b3U6pG1QKTUIas15DQ")

# channel usernames for force subscribe (without @)
MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "Channel_no_1One")
MAIN_CHANNEL_2 = os.getenv("MAIN_CHANNEL_2", "HAnime_Cosplays")
MAIN_CHANNEL_3 = os.getenv("MAIN_CHANNEL_3", "HAnime_Club")
MAIN_CHANNEL_4 = os.getenv("MAIN_CHANNEL_4","Channel_No_Four")
MAIN_CHANNEL_5 = os.getenv("MAIN_CHANNEL_5", "Channel_No_Five")

# shortener api keys
SHORTENER_API = os.environ.get("SHORTENER_API", "hDDSUg9SwwgX5397ELtXvfOeU6T2")
SHORTENER_API_2 = os.environ.get("SHORTENER_API_2", "bee210ce3303815c525dd1d2a34f0b97406b4ee0")
SHORTENER_API_3 = os.environ.get("SHORTENER_API_3", "bee210ce3303815c525dd1d2a34f0b97406b4ee0")
SHORTENER_API_4 = os.environ.get("SHORTENER_API_4", "bee210ce3303815c525dd1d2a34f0b97406b4ee0")
SHORTENER_API_5 = os.environ.get("SHORTENER_API_5", "23eb5dd17ac140282cad623f70635f2ba0820f4d")

# shortener api urls
SHORTENER_WEB = os.environ.get("SHORTENER_WEB", "https://api.shareus.in/shortLink?token={0}&format=json&link={1}")
SHORTENER_WEB_2 = os.environ.get("SHORTENER_WEB_2", "https://sonic-links.com/api?api={0}&url={1}")
SHORTENER_WEB_3 = os.environ.get("SHORTENER_WEB_3", "https://sonic-links.com/api?api={0}&url={1}")
SHORTENER_WEB_4 = os.environ.get("SHORTENER_WEB_4", "https://sonic-links.com/api?api={0}&url={1}")
SHORTENER_WEB_5 = os.environ.get("SHORTENER_WEB_5", "https://paisakamalo.in/api?api={0}&url={1}")

# Fill bot token, main channel, shortener api, shortener web accordingly.
# bot token 1 will only work with main channel 1 and shortener api 1
# and shortener web 1 will work with shortener api 1 only.
# and so on.
