import CryptoJS from 'crypto-js';
import { createClient } from '@supabase/supabase-js'
import { VUE_APP_URL, VUE_APP_KEY } from "@/.env.js"

//TODO: Export to .env file 
const URL = VUE_APP_URL
const KEY = VUE_APP_KEY
export const supabase = createClient(URL, KEY)


function HASH(val) {
    return CryptoJS.SHA3(val).toString(CryptoJS.enc.Hex)
}

export async function DB_SB_login(username, password) {
    const { data } = await supabase.from('users').select().eq("username", username).eq("password", HASH(password));
    console.log(data.length)
    const success = data.length < 1 ? false : true;
    return success;
}