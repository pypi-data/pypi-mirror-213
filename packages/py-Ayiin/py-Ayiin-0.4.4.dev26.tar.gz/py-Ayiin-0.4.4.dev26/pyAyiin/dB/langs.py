import os
import yaml

from ._core import mongodb


langdb = mongodb.langs

langm = {}
languages = {}


# language
async def get_lang(user_id: int) -> str:
    mode = langm.get(user_id)
    if not mode:
        lang = await langdb.find_one({"user_id": user_id})
        if not lang:
            langm[user_id] = "en"
            return "en"
        langm[user_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(user_id: int, lang: str):
    langm[user_id] = lang
    await langdb.update_one(
        {"user_id": user_id}, {"$set": {"lang": lang}}, upsert=True
    )


def get_string(lang: str):
    return languages[lang]


file_lang = open("pyAyiin/langs/", "r+t")
for filename in file_lang:
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        languages[language_name] = yaml.safe_load(
            open(r"pyAyiin/langs/" + filename, encoding="utf8")
        )
