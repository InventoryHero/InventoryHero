import { Dexie } from 'dexie';
import {resetLangToDefault} from "@/global/constants";

const db = new Dexie("p4ssword_m4nager");
db.version(2).stores({
    curr_user: "++idx, username",
    settings: "++idx, theme, language"
});


export async function setUser(username) {
    const user_exists = await db.curr_user.toArray(); 
    if (user_exists) {
        await db.curr_user.clear();
    }
    const data = {
        username: username,
    }
    await db.curr_user.add(data);
    return true;
}
export async function getUser() {
    const curr_user = await db.curr_user.toArray();
    if(curr_user.length === 0)
    {
        return undefined;
    }
    return curr_user[0];
}

export async function getSettings()
{
    const settings = await db.settings.toArray();
    if(settings.length === 0) {
        document.body.classList.add('dark-theme');
        await db.settings.add({theme: 'dark-theme', language: resetLangToDefault()})
        return await getSettings();
    }
    return settings[0];
}

export async function setTheme(theme)
{
    const settings = await getSettings();
    document.body.classList.remove(settings.theme);
    document.body.classList.add(theme);
    await db.settings.update(settings.idx, {theme: theme});
}
export async function setLanguage(language)
{
    const settings = await getSettings();


    await db.settings.update(settings.idx, {language: language});
}

export async function logout()
{
    await db.curr_user.clear();
}
