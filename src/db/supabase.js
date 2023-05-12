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


export async function DB_SB_get_boxes_per_room(room_id, user)
{
    return await supabase.from("boxes").select("*").eq("room_id", room_id).eq("username", user)
}


export async function DB_SB_get_products_per_room(room_id, user)
{
    return await supabase.from("products").select("*").eq("room_id", room_id).eq("username", user)
}


export async function DB_SB_getStarredProducts() {
    const user = await getUser()
    const { data } = await supabase.from('products').select().eq("username", user.username).eq("starred", true)
    return data;
}


export async function DB_SB_get_rooms(user){

    console.log(user);

    const data = await supabase.from("rooms").select("*").eq("username", user);


    for(let i = 0; i < data.data.length; i++)
    {
        let curr_room = data.data.at(i);
        const box_data = await DB_SB_get_boxes_per_room(curr_room.id, user)
        const product_data = await DB_SB_get_products_per_room(curr_room.id, user);
        curr_room.box_cnt = box_data.data.length
        curr_room.product_cnt = product_data.data.length
    }


    return data.data;
}


export async function DB_SB_get_boxes_of_user(user) {
    const data = await supabase.from("boxes").select("*").eq("username", user.username);
    return data.data
}


export async function DB_SB_get_rooms_of_user(user) {
    const data = await supabase.from("rooms").select("*").eq("username", user.username);
    return data.data
}

export async function DB_SB_add_product(product) {
    const user = await getUser();
  
    let box_id = -1;
    if (product.box != "") {
        box_id = await DB_SB_get_id_of_box(product.box);
    }
    let room_id = -1;
    if(product.room != "") {
        room_id = await DB_SB_get_id_of_room(product.room);
    }
    
    let data = {
        name: product.name,
        box_id: box_id,
        room_id: room_id,
        amount: product.amount,
        username: user.username,
        starred: product.starred
    }

    await supabase.from('products').insert(data);
}

export async function DB_SB_add_box(box) {
    const user = await getUser();
    let room_id = -1;
    if(box.room != "") {
        room_id = await DB_SB_get_id_of_room(box.room);
    }

    let data = {
        name: box.name,
        room_id: room_id,
        username: user.username
    }

    await supabase.from('boxes').insert(data);
}

export async function DB_SB_add_room(room) {
    const user = await getUser();

    let data = {
        name: room.name,
        username: user.username
    }
    await supabase.from('rooms').insert(data);
}

async function DB_SB_get_id_of_box(box_name) {
    const user = await getUser();
    const data = await supabase.from("boxes").select("id").eq("username", user.username).eq("name", box_name);
    return data.data[0].id;
}

async function DB_SB_get_id_of_room(room_name) {
    const user = await getUser();
    const data = await supabase.from("rooms").select("id").eq("username", user.username).eq("name", room_name);
    return data.data[0].id;
}