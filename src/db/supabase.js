import CryptoJS from 'crypto-js';
import { createClient } from '@supabase/supabase-js'
import { getUser } from './dexie';


//TODO: Export to .env file 
const URL = process.env.VUE_APP_URL
const KEY = process.env.VUE_APP_KEY

export const supabase = createClient(URL, KEY)


function HASH(val) {
    return CryptoJS.SHA3(val).toString(CryptoJS.enc.Hex)
}

export async function DB_SB_login(username, password) {
    const { data } = await supabase.from('users').select().eq("username", username).eq("password", HASH(password));
    const success = data.length < 1 ? false : true;
    return success;
}


export async function DB_SB_register(username, password) {
    const user = {
        username: username,
        password: HASH(password),
    }
    const { data } = await supabase.from('users').select().eq("username", username)
    if(data.length != 0) {
        console.log("[ERR] username already taken");
        return false;
    }
    await supabase.from('users').insert(user);
    return true;
}


export async function DB_SB_getStarredProducts() {
    const user = await getUser()
    const { data } = await supabase.from('products').select().eq("username", user.username).eq("starred", true)
    return data;
}

