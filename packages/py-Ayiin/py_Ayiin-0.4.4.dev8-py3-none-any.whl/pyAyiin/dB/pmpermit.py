from ._core import mongodb

pmpermitdb = mongodb.permit


BLOCK_MSG = "Sorry tod lu di blokir karna melakukan spam!!!"

LIMIT = 5

MSG_PERMIT = (
    """
╔═════════════════════╗
│  𖣘 𝚂𝙴𝙻𝙰𝙼𝙰𝚃 𝙳𝙰𝚃𝙰𝙽𝙶 𝚃𝙾𝙳 𖣘ㅤ  ㅤ
╚═════════════════════╝
 ⍟ 𝙹𝙰𝙽𝙶𝙰𝙽 𝚂𝙿𝙰𝙼 𝙲𝙷𝙰𝚃 𝙼𝙰𝙹𝙸𝙺𝙰𝙽 𝙶𝚄𝙰 𝙺𝙴𝙽𝚃𝙾𝙳
 ⍟ 𝙶𝚄𝙰 𝙰𝙺𝙰𝙽 𝙾𝚃𝙾𝙼𝙰𝚃𝙸𝚂 𝙱𝙻𝙾𝙺𝙸𝚁 𝙺𝙰𝙻𝙾 𝙻𝚄 𝚂𝙿𝙰𝙼
 ⍟ 𝙹𝙰𝙳𝙸 𝚃𝚄𝙽𝙶𝙶𝚄 𝚂𝙰𝙼𝙿𝙰𝙸 𝙼𝙰𝙹𝙸𝙺𝙰𝙽 𝙶𝚄𝙰 𝙽𝙴𝚁𝙸𝙼𝙰 𝙿𝙴𝚂𝙰𝙽 𝙻𝚄
╔═════════════════════╗
│ㅤㅤ𖣘 𝙿𝙴𝚂𝙰𝙽 𝙾𝚃𝙾𝙼𝙰𝚃𝙸𝚂 𖣘ㅤㅤ
│ㅤㅤ   𖣘 𝙰𝚈𝙸𝙸𝙽 - 𝚄𝙱𝙾𝚃 𖣘ㅤㅤ
╚═════════════════════╝
"""
)



async def is_pmpermit_approved(user_id: int, chat_id: int) -> bool:
    user = await pmpermitdb.find_one({"user_id": user_id, "chat_id": chat_id})
    if not user:
        return False
    return True


async def approve_pmpermit(user_id: int, chat_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id, chat_id)
    if is_pmpermit:
        return
    return await pmpermitdb.insert_one({"user_id": user_id, "chat_id": chat_id})


async def disapprove_pmpermit(user_id: int, chat_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id, chat_id)
    if not is_pmpermit:
        return
    return await pmpermitdb.delete_one({"user_id": user_id, "chat_id": chat_id})


async def set_pmpermit(user_id, value: bool):
    await pmpermitdb.update_one(
        {"user_id": user_id},
        {"$set": {"pmpermit": value}},
        upsert=True
    )


async def get_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return None
    return x["pmpermit"]


async def message_pmpermit(user_id: int, text: str):
    doc = {"user_id": user_id, "pmpermit_message": text}
    await pmpermitdb.update_one(
        {"user_id": user_id},
        {"$set": doc},
        upsert=True)


async def get_message_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return MSG_PERMIT
    return x["pmpermit_message"]


async def limit_pmpermit(user_id: int, limit):
    doc = {"user_id": user_id, "limit": limit}
    await pmpermitdb.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)


async def get_limit_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return LIMIT
    return x["limit"]


async def block_message_pmpermit(user_id: int, text: str):
    doc = {"user_id": user_id, "block_message": text}
    await pmpermitdb.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)


async def get_block_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return BLOCK_MSG
    return x["block_message"]


async def media_pmpermit(user_id: int, url: str):
    doc = {"user_id": user_id, "media_message": url}
    await pmpermitdb.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)


async def get_media_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return None
    return x["media_message"]


async def all_pmpermit(user_id: int):
    result = await pmpermitdb.find_one({"user_id": user_id})
    #if not result:
    #    return MSG_PERMIT, None, LIMIT
    permit = result["pmpermit"]
    pm_message = result.get("pmpermit_message") if result.get("pmpermit_message") is not None else MSG_PERMIT
    media_message = result.get("media_message") 
    limit = result.get("limit") if result.get("limit") is not None else LIMIT
    return pm_message, media_message, limit




'''
from ._core import mongodb

pmpermitdb = mongodb.permit


async def is_pmpermit_approved(user_id: int) -> bool:
    user = await pmpermitdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def approve_pmpermit(user_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id)
    if is_pmpermit:
        return
    return await pmpermitdb.insert_one({"user_id": user_id})


async def disapprove_pmpermit(user_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id)
    if not is_pmpermit:
        return
    return await pmpermitdb.delete_one({"user_id": user_id})
'''