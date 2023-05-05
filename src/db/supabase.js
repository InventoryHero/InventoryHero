import CryptoJS from 'crypto-js';
import { createClient } from '@supabase/supabase-js'

//TODO: Export to .env file 
const URL = process.env.VUE_APP_URL
const KEY = process.env.VUE_APP_KEY


console.log(URL);
console.log(KEY);

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