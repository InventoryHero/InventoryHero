import { Dexie } from 'dexie';

const db = new Dexie("p4ssword_m4nager");
db.version(1).stores({
    curr_user: "++idx, username, password",
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

export async function logout()
{
    await db.curr_user.clear();
}