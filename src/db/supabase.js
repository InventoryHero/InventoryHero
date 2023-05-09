import CryptoJS from 'crypto-js';
import { createClient } from '@supabase/supabase-js'

//TODO: Export to .env file 
const URL = process.env.VUE_APP_URL
const KEY = process.env.VUE_APP_KEY

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


export async function DB_SB_register(username, password) {
    const user = {
        username: username,
        password: HASH(password),
    }
    const { data } = await supabase.from('users').select().eq("username", username)
    console.log(data.length, password);
    if(data.length != 0) {
        console.log("[ERR] username already taken");
        return false;
    }
    await supabase.from('users').insert(user);
    return true;
}

export async function DB_SB_get_boxes_per_room(room_id)
{
    return await supabase.from("boxes").select("*").eq("room_id", room_id)
}
export async function DB_SB_get_products_per_room(room_id)
{
    return await supabase.from("products").select("*").eq("room_id", room_id)
}

export async function DB_SB_get_rooms(){
    const data = await supabase.from("rooms").select("*");


    for(let i = 0; i < data.data.length; i++)
    {
        let curr_room = data.data.at(i);
        const box_data = await DB_SB_get_boxes_per_room(curr_room.id)
        const product_data = await DB_SB_get_products_per_room(curr_room.id);
        curr_room.box_cnt = box_data.data.length
        curr_room.product_cnt = product_data.data.length
    }


    return data.data;
}

