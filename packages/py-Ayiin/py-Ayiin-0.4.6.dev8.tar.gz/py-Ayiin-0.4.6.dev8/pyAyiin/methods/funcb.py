# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio
import os

from fipper.errors import FloodWait, PeerIdInvalid
from fipper.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    Message,
)


class FuncBot(object):
    async def approve_pmpermit(
        self,
        cb,
        user_ids,
        chat_id,
    ):
        from ..dB.pmpermit import approve_pmpermit, is_pmpermit_approved

        
        if isinstance(cb, CallbackQuery):
            if await is_pmpermit_approved(user_ids, chat_id):
                await cb.answer("Pengguna Ini Sudah Ada Di Database.", show_alert=True)
                return
            await cb.answer()
            await approve_pmpermit(user_ids, chat_id)
            await cb.edit_message_text("Pesan Anda Diterima Tod")
        elif isinstance(cb, Message):
            if await is_pmpermit_approved(user_ids, chat_id):
                await cb.edit("Pengguna Ini Sudah Ada Di Database.", show_alert=True)
                return
            await approve_pmpermit(user_ids, chat_id)
            await cb.edit("Pesan Anda Diterima Tod")
            await cb.delete()
        
    async def disapprove_pmpermit(
        self,
        cb,
        user_ids,
        chat_id,
    ):
        from ..dB.pmpermit import disapprove_pmpermit, is_pmpermit_approved
        
        if isinstance(cb, CallbackQuery):
            if not await is_pmpermit_approved(user_ids, chat_id):
                return await cb.answer("Pengguna Ini Tidak Ada Di Database")
            await disapprove_pmpermit(user_ids, chat_id)
            await cb.edit_message_text("Pesan Anda Ditolak Tod")
        elif isinstance(cb, Message):
            if not await is_pmpermit_approved(user_ids, chat_id):
                return await cb.edit("Pengguna Ini Tidak Ada Di Database")
            await disapprove_pmpermit(user_ids, chat_id)
            await cb.edit("Pesan Anda Ditolak Tod")


    async def start_bot(self, client):
        from pyAyiin.Clients.client import tgbot
        
        tgbot.me = await tgbot.get_me()
        succ = await client.send_message(tgbot.me.username, "/start")
        return succ


    async def logger_bot(
        self,
        client,
        pepek,
        group: bool = False,
    ):
        from pyAyiin.Clients.client import tgbot

        if group:
            from_user = f"{pepek.from_user.first_name}" if pepek.from_user.first_name else None
            try:
                await tgbot.send_message(
                    client.me.id,
                    f"""📨 #TAGS #MESSAGE
• <b>Logs:</b> <code>{client.me.first_name}</code>
• <b>Group:</b> <code>{pepek.chat.title}</code>
• <b>Dari :</b> <code>{from_user}</code>
• <b>Pesan:</b> ↓↓↓↓\n\n<code>{pepek.text}</code>
""",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("👀 Pesan 👀", url=f"{pepek.link}")],
                            [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                        ]
                    ),
                    disable_web_page_preview=True,
                    )
            except PeerIdInvalid:
                xd = await self.start_bot(client)
                if xd:
                    await tgbot.send_message(
                        client.me.id,
                        f"""📨 #TAGS #MESSAGE
• <b>Logs:</b> <code>{client.me.first_name}</code>
• <b>Group:</b> <code>{pepek.chat.title}</code>
• <b>Dari :</b> <code>{from_user}</code>
• <b>Pesan:</b> ↓↓↓↓\n\n<code>{pepek.text}</code>
""",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("👀 Pesan 👀", url=f"{pepek.link}")],
                                [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                            ]
                        ),
                        disable_web_page_preview=True,
                        )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except BaseException:
                pass
        else:
            if pepek.text:
                try:
                    return await tgbot.send_message(
                        client.me.id,
                        f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}\nPesan:\n{pepek.text}",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                            ]
                        ),
                        disable_web_page_preview=True,
                    )
                except PeerIdInvalid:
                    x = await self.start_bot(client)
                    if x:
                        return await tgbot.send_message(
                            client.me.id,
                            f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}\nPesan:\n{pepek.text}",
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                                ]
                            ),
                            disable_web_page_preview=True,
                        )
                    else:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except BaseException:
                    pass
            if pepek.photo:
                file = await client.download_media(pepek.photo)
                try:
                    await tgbot.send_photo(
                        client.me.id,
                        photo=file,
                        caption=f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                            ]
                        ),
                    )
                    os.remove(file)
                    return
                except PeerIdInvalid:
                    x = await self.start_bot(client)
                    if x:
                        await tgbot.send_photo(
                            client.me.id,
                            photo=file,
                            caption=f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}",
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                                ]
                            ),
                        )
                        os.remove(file)
                        return
                    else:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except BaseException:
                    pass
            if pepek.video:
                file = await client.download_media(pepek.video)
                try:
                    await tgbot.send_video(
                        client.me.id,
                        video=file,
                        caption=f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                            ]
                        ),
                    )
                    os.remove(file)
                    return
                except PeerIdInvalid:
                    x = await self.start_bot(client)
                    if x:
                        await tgbot.send_video(
                            client.me.id,
                            video=file,
                            caption=f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}",
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                                ]
                            ),
                        )
                        os.remove(file)
                        return
                    else:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except BaseException:
                    pass
            if pepek.voice:
                file = await client.download_media(pepek.voice)
                try:
                    await tgbot.send_voice(
                        client.me.id,
                        voice=file,
                        caption=f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                            ]
                        ),
                    )
                    os.remove(file)
                    return
                except PeerIdInvalid:
                    x = await self.start_bot(client)
                    if x:
                        await tgbot.send_voice(
                            client.me.id,
                            voice=file,
                            caption=f"Logs: {client.me.first_name}\nPesan Dari: {pepek.from_user.first_name}",
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                                ]
                            ),
                        )
                        os.remove(file)
                        return
                    else:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except BaseException:
                    pass
            if pepek.sticker:
                file = await client.download_media(pepek.sticker)
                try:
                    await tgbot.send_sticker(
                        client.me.id,
                        sticker=file,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                            ]
                        ),
                    )
                    os.remove(file)
                    return
                except PeerIdInvalid:
                    x = await self.start_bot(client)
                    if x:
                        await tgbot.send_sticker(
                            client.me.id,
                            sticker=file,
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [InlineKeyboardButton("💌 Pengirim 💌", url=f"tg://openmessage?user_id={pepek.from_user.id}")],
                                ]
                            ),
                        )
                        os.remove(file)
                        return
                    else:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except BaseException:
                    pass
