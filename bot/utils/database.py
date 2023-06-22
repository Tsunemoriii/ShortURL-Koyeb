import datetime
import time

from motor.motor_asyncio import AsyncIOMotorClient

from bot.utils.config import DATABASE_URL


class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        # bot 1 db
        self.col1 = self.db.users
        self.bc1 = self.db.broadcasts
        self.forw1 = self.db.forward
        # bot 2 db
        self.col2 = self.db.users2
        self.bc2 = self.db.broadcasts2
        self.forw2 = self.db.forward2
        # bot 3 db
        self.col3 = self.db.users3
        self.bc3 = self.db.broadcasts3
        self.forw3 = self.db.forward3
        # bot 4 db
        self.col4 = self.db.users4
        self.bc4 = self.db.broadcasts4
        self.forw4 = self.db.forward4
        # bot 5 db
        self.col5 = self.db.users5
        self.bc5 = self.db.broadcasts5
        self.forw5 = self.db.forward5

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            notif=True,
        )

    def new_broadcast(self, id, info):
        return dict(
            broadcast_id=id,
            broadcast_time=time.time(),
            msg_ids=info,
        )
    
    def get_db(self, folder: int, bot_id: int):
        if folder == 1:
            if bot_id == 1:
                return self.col1
            elif bot_id == 2:
                return self.col2
            elif bot_id == 3:
                return self.col3
            elif bot_id == 4:
                return self.col4
            elif bot_id == 5:
                return self.col5
        elif folder == 2:
            if bot_id == 1:
                return self.bc1
            elif bot_id == 2:
                return self.bc2
            elif bot_id == 3:
                return self.bc3
            elif bot_id == 4:
                return self.bc4
            elif bot_id == 5:
                return self.bc5
        elif folder == 3:
            if bot_id == 1:
                return self.forw1
            elif bot_id == 2:
                return self.forw2
            elif bot_id == 3:
                return self.forw3
            elif bot_id == 4:
                return self.forw4
            elif bot_id == 5:
                return self.forw5
        else:
            return None

    async def add_user(self, id, bot_id: int):
        user = self.new_user(id)
        folder = self.get_db(1, bot_id)
        await folder.insert_one(user)

    async def is_user_exist(self, id, bot_id: int):
        folder = self.get_db(1, bot_id)
        user = await folder.find_one({"id": int(id)})
        return True if user else False

    async def total_users_count(self, bot_id: int):
        folder = self.get_db(1, bot_id)
        count = await folder.count_documents({})
        return count

    async def get_all_users(self, bot_id: int):
        folder = self.get_db(1, bot_id)
        all_users = folder.find({})
        return all_users

    async def delete_user(self, user_id, bot_id: int):
        folder = self.get_db(1, bot_id)
        await folder.delete_many({"id": int(user_id)})

    async def set_forward(self, status, bot_id: int):
        folder = self.get_db(3, bot_id)
        try:
            if await self.get_forward():
                await folder.delete_one({"forward": "True"})
            else:
                await folder.delete_one({"forward": "False"})
        except:
            pass
        await folder.insert_one({"forward": status})

    async def get_forward(self, bot_id: int):
        folder = self.get_db(3, bot_id)
        user = await folder.find_one({"forward": "True"})
        return True if user else False

    async def get_broadcast_info(self, broadcast_id, bot_id: int):
        folder = self.get_db(2, bot_id)
        info = await folder.find_one({"broadcast_id": broadcast_id})
        return info

    async def set_broadcast_info(self, broadcast_id, info, bot_id: int):
        folder = self.get_db(2, bot_id)
        to_set = self.new_broadcast(broadcast_id, info)
        await folder.insert_one(to_set)

    async def del_broadcast_info(self, broadcast_id, bot_id: int):
        folder = self.get_db(2, bot_id)
        await folder.delete_one({"broadcast_id": broadcast_id})


db = Database(DATABASE_URL, "ShortUrlBot")
