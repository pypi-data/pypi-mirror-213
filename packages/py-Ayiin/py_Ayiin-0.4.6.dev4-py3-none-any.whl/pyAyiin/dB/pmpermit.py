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
        return
    return x.get("pmpermit_message", MSG_PERMIT)


async def limit_pmpermit(user_id: int, limit):
    doc = {"user_id": user_id, "limit": limit}
    await pmpermitdb.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)


async def get_limit_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return
    return x.get("limit", LIMIT)


async def block_message_pmpermit(user_id: int, text: str):
    doc = {"user_id": user_id, "block_message": text}
    await pmpermitdb.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)


async def media_pmpermit(user_id: int, text: str):
    doc = {"user_id": user_id, "media_message": text}
    await pmpermitdb.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)


async def get_media_pmermit(user_id: int):
    x = await pmpermitdb.find_one({"user_id": user_id})
    if not x:
        return None
    return x.get("media_message", None)


async def setting_pmpermit(user_id: int):
    result = await pmpermitdb.find_one({"user_id": user_id})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    msg = result.get("pmpermit_message")
    media = result.get("media_message")
    block_msg = result.get("block_message")
    pm_limit = result.get("limit")
    pm_media = media if media is not None else None
    pm_message = msg if msg is not None else MSG_PERMIT
    block_message = block_msg if block_msg is not None else BLOCK_MSG
    limit = pm_limit if pm_limit is not None else LIMIT
    return pmpermit, pm_message, pm_media, limit, block_message




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