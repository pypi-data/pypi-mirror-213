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

from fipper.enums import ParseMode
from fipper.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InlineQueryResultVideo,
    InputTextMessageContent,
)

from ..config import Var
from ..pyrogram.toolbot import ToolBot


class InlineBot(Var, ToolBot):
    async def inline_pmpermit(self, user_id, ids):
        from pyAyiin.dB.pmpermit import all_pmpermit, get_media_pmpermit, get_message_pmpermit
        
        button = [
            [
                InlineKeyboardButton(
                    text='• Approve •',
                    callback_data=f'terima_{user_id}xd{ids}',
                ),
                InlineKeyboardButton(
                    text='• Disapprove •',
                    callback_data=f'tolak_{user_id}xd{ids}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text='• Close •',
                    callback_data=f'close',
                ),
            ]
        ]
        media_message = await get_media_pmpermit(user_id)
        pm_message = await get_message_pmpermit(user_id)
        endsw = (".mp4", ".gif")
        if media_message is not None: # Jika database HELP_PIC tidak kosong
            if media_message.endswith(endsw): # jika format video atau gif 
                pm_results = [
                    (
                        InlineQueryResultVideo(
                            video_url=media_message,
                            thumb_url=media_message,
                            title="PmPermit",
                            description="inline AyiinUbot.",
                            caption=pm_message,
                            reply_markup=InlineKeyboardMarkup(button),
                        )
                    )
                ]
            else: # Format foto
                pm_results = [
                    (
                        InlineQueryResultPhoto(
                            photo_url=media_message,
                            title="PmPermit",
                            description="inline AyiinUbot.",
                            caption=pm_message,
                            reply_markup=InlineKeyboardMarkup(button),
                        )
                    )
                ]
        else: # Jika database HELP_PIC kosong akan menjadi teks biasa tanpa foto atau video
            pm_results = [
                (
                    InlineQueryResultArticle(
                        title='PmPermit Ayiin Ubot!',
                        reply_markup=InlineKeyboardMarkup(button),
                        input_message_content=InputTextMessageContent(pm_message),
                    )
                )
            ]
        
        return pm_results
    
    async def inline_help(self, output):
        from pyAyiin import CMD_HELP
        from pyAyiin.dB.variable import get_var
        
        HELP_PIC = await get_var('HELP_PIC')
        endsw = (".mp4", ".gif")
        if HELP_PIC is not None: # Jika database HELP_PIC tidak kosong
            if HELP_PIC.endswith(endsw): # jika format video atau gif 
                results = [
                    (
                        InlineQueryResultVideo(
                            video_url=HELP_PIC,
                            thumb_url=HELP_PIC,
                            title="Help",
                            description="inline AyiinUbot.",
                            caption=output,
                            reply_markup=InlineKeyboardMarkup(
                                self.HelpXd(0, CMD_HELP, "xd")
                            ),
                        )
                    )
                ]
            else: # Format foto
                results = [
                    (
                        InlineQueryResultPhoto(
                            photo_url=HELP_PIC,
                            title="Help",
                            description="inline AyiinUbot.",
                            caption=output,
                            reply_markup=InlineKeyboardMarkup(
                                self.HelpXd(0, CMD_HELP, "xd")
                            ),
                        )
                    )
                ]
        else: # Jika database HELP_PIC kosong akan menjadi teks biasa tanpa foto atau video
            results = [
                (
                    InlineQueryResultArticle(
                        title="Help Ayiin Ubot!",
                        reply_markup=InlineKeyboardMarkup(
                                self.HelpXd(0, CMD_HELP, "xd")
                            ),
                        input_message_content=InputTextMessageContent(output),
                    )
                )
            ]
        return results
    
    async def inline_alive(self, output):
        from pyAyiin.dB.variable import get_var
        
        alive_pic = await get_var('ALIVE_PIC')
        buttons = [
            [
                InlineKeyboardButton("•• Group ••", url='https://t.me/AyiinChats'),
                InlineKeyboardButton("•• Channel ••", url='https://t.me/AyiinChannel'),
            ]
        ]
        endsw = (".mp4", ".gif")
        if alive_pic is not None: # Jika database alive tidak kosong
            if alive_pic.endswith(endsw): # jika format video atau gif
                results = [
                    (
                        InlineQueryResultVideo(
                            video_url=alive_pic,
                            thumb_url=alive_pic,
                            title="Alive",
                            description="inline AyiinUbot.",
                            caption=output,
                            reply_markup=InlineKeyboardMarkup(buttons),
                        )
                    )
                ]
            else:
                results = [
                    (
                        InlineQueryResultPhoto(
                            photo_url=alive_pic,
                            title="Alive",
                            description="inline AyiinUbot.",
                            caption=output,
                            reply_markup=InlineKeyboardMarkup(buttons),
                        )
                    )
                ]
        else:
            results = [
                (
                    InlineQueryResultArticle(
                        title="Alive Ayiin Ubot!",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        input_message_content=InputTextMessageContent(output),
                    )
                )
            ]
        return results
