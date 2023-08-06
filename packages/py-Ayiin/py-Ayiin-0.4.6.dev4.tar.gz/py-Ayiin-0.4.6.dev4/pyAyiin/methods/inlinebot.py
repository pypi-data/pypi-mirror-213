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
        from pyAyiin.dB.variable import get_var
        
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
        PERMIT_PIC = await get_var('PERMIT_PIC')
        endsw = (".mp4", ".gif")
        if PERMIT_PIC is not None: # Jika database HELP_PIC tidak kosong
            if PERMIT_PIC.endswith(endsw): # jika format video atau gif 
                pm_results = [
                    (
                        InlineQueryResultVideo(
                            video_url=PERMIT_PIC,
                            thumb_url=PERMIT_PIC,
                            title="PmPermit",
                            description="inline AyiinUbot.",
                            caption=self.PERMIT_MSG,
                            reply_markup=InlineKeyboardMarkup(button),
                        )
                    )
                ]
            else: # Format foto
                pm_results = [
                    (
                        InlineQueryResultPhoto(
                            photo_url=PERMIT_PIC,
                            title="PmPermit",
                            description="inline AyiinUbot.",
                            caption=self.PERMIT_MSG,
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
                        input_message_content=InputTextMessageContent(self.PERMIT_MSG),
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
    
    async def inline_languages(self, _):
        from pyAyiin.dB.langs import get_languages
        
        text = _["lang"]
        languages = get_languages()
        tutud = [
            InlineKeyboardButton(
                f"{languages[yins]['nama']}",
                callback_data=f"set_{yins}",
            )
            for yins in languages
        ]
        buttons = list(zip(tutud[::2], tutud[1::2]))
        if len(tutud) % 2 == 1:
            buttons.append((tutud[-1],))
        buttons.append([InlineKeyboardButton(_["back"], callback_data="close")])
        return text, buttons
