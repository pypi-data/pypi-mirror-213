import yaml

from os import listdir, path

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


import pyAyiin.langs as file

strings_folder = path.join(path.dirname(path.realpath(__file__)), file)
for filename in listdir(strings_folder):
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        languages[language_name] = yaml.safe_load(
            open(path.join(strings_folder, filename), encoding="utf8")
        )
