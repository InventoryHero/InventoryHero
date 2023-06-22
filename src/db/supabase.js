import CryptoJS from 'crypto-js';
import { createClient } from '@supabase/supabase-js'
import { getUser } from './dexie';


const URL = process.env.VUE_APP_URL
const KEY = process.env.VUE_APP_KEY

export const supabase = createClient(URL, KEY)


function HASH(val) {
    return CryptoJS.SHA3(val).toString(CryptoJS.enc.Hex)
}

async function map_rooms_with_boxes(only_rooms = false)
{
    const user = await getUser();
    const {data: db_rooms} = await supabase.from("rooms").select("*").eq("username", user.username);
    let boxes = {'-1': {name: "", room_name: ""}};
    let rooms = {'-1': ""};
    db_rooms.forEach(function(room, ){
        rooms[room.id] = room.name;
    })
    if(only_rooms)
        return {rooms: rooms, boxes: {}};

    const {data: db_boxes} = await supabase.from("boxes").select("*").eq("username", user.username);
    db_boxes.forEach(function(box, ){
        boxes[box.id] = {
            name: box.name,
            room_name: rooms[box.room_id]
        };
    })
    return  {rooms: rooms, boxes: boxes};
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
    if(data.length !== 0) {
        console.log("[ERR] username already taken");
        return "username_taken";
    }
    const {error} = await supabase.from('users').insert(user);
    if(error !== null)
    {
        return "generic_err";
    }
    return "";
}


export async function DB_SB_get_boxes_per_room(room_id, user)
{
    return await supabase.from("boxes").select("*").eq("room_id", room_id).eq("username", user)
}

export async function DB_SB_get_products_per_box(box_id, user)
{
    let {data} = await supabase.from("productmapping").select("*, products!inner(*)").eq("box_id", box_id).eq("products.username", user);
    let {rooms, boxes} = await map_rooms_with_boxes();
    let products = [];
    data.forEach(function(mapping, index){
        let product = mapping.products;
        let curr_product = {
            id: product.id,
            name: product.name,
            box_id: mapping.box_id,
            box_name: boxes[mapping.box_id].name,
            room_id: mapping.room_id,
            room_name: rooms[mapping.room_id],
            amount: mapping.amount,
            username: product.username,
            starred: product.starred,
            creation_date: product.creation_date,
            mapping_id: mapping.id,
        }
        if(curr_product.room_id === -1)
        {
            curr_product.room_name = boxes[curr_product.box_id].room_name
        }
        products.push(curr_product);
    })
    return products;
}

export async function DB_SB_get_products_per_room(room_id, user)
{
    let {data} = await supabase.from("productmapping").select("*, products!inner(*)").eq("room_id", room_id).eq("products.username", user);
    let {rooms} = await map_rooms_with_boxes();
    let products = [];
    data.forEach(function(mapping, index){
        let product = mapping.products;
        let curr_product = {
            id: product.id,
            name: product.name,
            box_id: -1,
            box_name: "",
            room_id: mapping.room_id,
            room_name: rooms[mapping.room_id],
            amount: mapping.amount,
            username: product.username,
            starred: product.starred,
            creation_date: product.creation_date,
            mapping_id: mapping.id,
        }
        if(curr_product.room_id === -1)
        {
            curr_product.room_name = boxes[curr_product.box_id].room_name
        }
        products.push(curr_product);
    })
    return products;
}

export async function DB_SB_getLastUsedProducts(user){
    const {data} = await supabase.from("products").select("*, productmapping(*)").eq("username", user);
    let {rooms, boxes} = await map_rooms_with_boxes();

    let products = [];

    data.forEach(function(product, index){
        let mapping = product.productmapping;
        for(let i = 0; i < mapping.length; ++i)
        {
            let curr_product = {
                id: product.id,
                name: product.name,
                box_id: mapping[i].box_id,
                box_name: boxes[mapping[i].box_id].name,
                room_id: mapping[i].room_id,
                room_name: rooms[mapping[i].room_id],
                amount: mapping[i].amount,
                updated_at: mapping[i].updated_at,
                username: product.username,
                starred: product.starred,
                creation_date: product.creation_date,
                mapping_id: mapping[i].id,

            }
            if(curr_product.room_id === -1)
            {
                curr_product.room_name = boxes[curr_product.box_id].room_name
            }
            products.push(curr_product);

        }
    })

    products.sort((left, right) => {
        var leftDate = new Date(left.updated_at),
            rightDate = new Date(right.updated_at);
        if (leftDate < rightDate){
            return 1;
        }
        if (leftDate > rightDate){
            return -1;
        }
        return 0;
    });

    return products.slice(0, 10);
}

export async function DB_SB_getStarredProducts(user){
    const {data} = await supabase.from("products").select("*, productmapping(*)").eq("username", user).eq("starred", true);
    let {rooms, boxes} = await map_rooms_with_boxes();

    let products = [];

    data.forEach(function(product, index){
        let mapping = product.productmapping;
        for(let i = 0; i < mapping.length; ++i)
        {
            let curr_product = {
                id: product.id,
                name: product.name,
                box_id: mapping[i].box_id,
                box_name: boxes[mapping[i].box_id].name,
                room_id: mapping[i].room_id,
                room_name: rooms[mapping[i].room_id],
                amount: mapping[i].amount,
                updated_at: mapping[i].updated_at,
                username: product.username,
                starred: product.starred,
                creation_date: product.creation_date,
                mapping_id: mapping[i].id,

            }
            if(curr_product.room_id === -1)
            {
                curr_product.room_name = boxes[curr_product.box_id].room_name
            }
            products.push(curr_product);

        }
    })

    return products;
}

export async function DB_SB_getStarredProducts_per_box(box_id, user) {
    return await supabase.from('products').select("*").eq("box_id", box_id).eq("username", user).eq("starred", true)
}

export async function DB_SB_get_rooms(user){

    if(user === undefined)
    {
        user = await getUser();
    }
    const data = await supabase.from("rooms").select("*").eq("username", user);

    const all_boxes = (await supabase.from("boxes").select("*").eq("username", user)).data;
    const all_products = (await supabase.from("products").select("*, productmapping(*)").eq("username", user)).data;

    for(let i = 0; i < data.data.length; i++) {
        let curr_room = data.data.at(i);
        let curr_boxes_amount = 0
        let curr_products_amount = 0

        for (let j = 0; j < all_boxes.length; j++) {
            if (all_boxes[j].room_id === curr_room.id) {
                curr_boxes_amount++;
            }
        }
        for (let j = 0; j < all_products.length; j++) {
            for(let k = 0;  k < all_products[j].productmapping.length; ++k)
            {
                if (all_products[j].productmapping[k].room_id === curr_room.id) {
                    curr_products_amount++;
                }
            }
        }

        curr_room.box_cnt = curr_boxes_amount
        curr_room.product_cnt = curr_products_amount
    }

    return data.data;
}

export async function DB_SB_get_all_products(user){
    const {data} = await supabase.from("products").select("*, productmapping(*)").eq("username", user);
    let {rooms, boxes} = await map_rooms_with_boxes();

    let products = [];

    data.forEach(function(product, index){
        let mapping = product.productmapping;
        for(let i = 0; i < mapping.length; ++i)
        {
            let curr_product = {
                id: product.id,
                name: product.name,
                box_id: mapping[i].box_id,
                box_name: boxes[mapping[i].box_id].name,
                room_id: mapping[i].room_id,
                room_name: rooms[mapping[i].room_id],
                amount: mapping[i].amount,
                username: product.username,
                starred: product.starred,
                creation_date: product.creation_date,
                mapping_id: mapping[i].id,

            }
            if(curr_product.room_id === -1)
            {
                curr_product.room_name = boxes[curr_product.box_id].room_name
            }
            products.push(curr_product);

        }
    })
    return products;
}

export async function DB_SB_get_products_without_storage_location()
{
    const user = await getUser();
    const {data} = await supabase.from("products").select("*").eq("username", user.username);
    return data;
}

export async function DB_SB_change_product_amount(mapping_id, amount) {

    const user = await getUser();
    const {data: product} = await supabase.from("productmapping").select("*, products!inner(*)").eq("id", mapping_id).eq("products.username", user.username);
    if(product === null || product === undefined || product.length === 0)
        return -1;
    const { data, error } = await supabase.rpc("change_product_amount", { mapping_id:mapping_id, change: amount });
  
    if (error) {
      console.log("Error occurred:", error.message);
      return -1;
    } else {
      return data;
    }
  }

  

  export async function DB_SB_get_product(productId, user=undefined) {
    if(user === undefined)
        user = await getUser();

    const { data, error } = await supabase.from("products").select("*").eq("username", user.username).eq("id", productId).single();
  
    if (error) {
      console.log("Error :", error.message);
      return null;
    }
  
    return data;
  }


export async function DB_SB_get_boxes(user, room = -1){
    let data;
    if(room === -1)
    {
        data = (await supabase.from("boxes").select("*").eq("username", user)).data;
    }
    else {
        data = (await supabase.from("boxes").select("*").eq("username", user).eq("room_id", room)).data;
    }

    const all_products_of_user = (await supabase.from("products").select("*, productmapping(*)").eq("username", user)).data;
    
    for(let i = 0; i < data.length; i++) {
        let curr_box = data.at(i);
        let curr_boxes_amount = 0
        let curr_starred_amount = 0

        for (let j = 0; j < all_products_of_user.length; j++) {


            for(let k = 0; k < all_products_of_user[j].productmapping.length; k++)
            {

                if (all_products_of_user[j].productmapping[k].box_id === curr_box.id) {
                    if (all_products_of_user[j].starred) {
                        curr_starred_amount++;

                    }
                    curr_boxes_amount++;
                }
            }

        }
        curr_box.product_cnt = curr_boxes_amount
        curr_box.starred_product_cnt = curr_starred_amount
    }

    return data;
}


export async function DB_SB_get_boxes_of_user(user, room =undefined) {
    let data;
    if(room !== undefined)
    {
        let room_id = await DB_SB_get_id_of_room(room);
        data = await supabase.from("boxes").select("*").eq("username", user.username).eq("room_id", room_id);
        //console.error(data);
    }
    else
    {
        data = await supabase.from("boxes").select("*").eq("username", user.username);
    }
    return data.data;
}


export async function DB_SB_get_rooms_of_user(user) {
    if(user === undefined)
        user = await getUser();

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

    let db_product = await DB_SB_get_product_by_name(product.name);
    let product_id = -1;
    if(db_product !== undefined)
        product_id = db_product.id;
    let mapping = undefined;
    let data = {}
    if(product_id === -1)
    {
        // this is new product
        data = {
            name: product.name,
            username: user.username,
            starred: product.starred
        }
        product_id = await supabase.from("products").insert(data).select("id");
        if(product_id.data.length === 0)
        {
            // ERROR
            console.error(product_id.error);
            return;
        }
        product_id = product_id.data[0].id;
    }
    else
    {
        if(product.starred !== db_product.starred)
        {
            await supabase.from("products").update({starred: product.starred}).eq("id", db_product.id)
        }

        const { data: res} = await supabase.from("productmapping")
                            .select("id, amount")
                            .eq("product_id", product_id)
                            .eq("box_id", box_id)
                            .eq("room_id", room_id);
        if(res !== undefined && res !== null && res.length !== 0)
            mapping = res[0];

    }
    data = {
        box_id: box_id,
        room_id: room_id,
        amount: product.amount
    }
    if(mapping !== undefined)
    {
        data.amount += mapping.amount;
        await supabase.from('productmapping').update(data).eq("id", mapping.id);
    }
    else
    {
        data["product_id"] = product_id;
        await supabase.from('productmapping').insert(data);
    }

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
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return -1;
    return data.data[0].id;
}

export async function DB_SB_get_room(room_id, user = undefined)
{
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("rooms").select("*").eq("username", user.username).eq("id", room_id);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return [];
    return data.data;
}
export async function DB_SB_get_box(box_id, user = undefined)
{
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("boxes").select("*").eq("username", user.username).eq("id", box_id);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return [];
    return data.data;
}
export async function DB_SB_get_room_name(id, user=undefined)
{
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("rooms").select("name").eq("username", user.username).eq("id", id);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return "";
    return data.data[0].name;
}

export async function DB_SB_get_name_of_room_of_box(box)
{
    const user = await getUser();
    const data = await supabase.from("boxes").select("*").eq("username", user.username).eq("name", box);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0) {
        return "";
    }

    return await DB_SB_get_room_name(data.data[0].room_id);
}

export async function DB_SB_get_room_of_box(box, user = undefined)
{
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("boxes").select("*").eq("username", user.username).eq("id", box);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0) {
        return "";
    }

    return await DB_SB_get_room(data.data[0].room_id);
}

export async function DB_SB_get_box_name(id, user=undefined) {
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("boxes").select("name").eq("username", user.username).eq("id", id);
    if (data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return "";
    return data.data[0].name;
}

export async function DB_SB_update_room_name(id, name)
{
    const user = await getUser();
    const {error} = await supabase.from("rooms").update({name: name}).eq("username", user.username).eq('id', id);
    if (error) {
        console.log("Error :", error.message);
        return false;
    }
    return true;
}

export async function DB_SB_get_room_createdat(id)
{
    const user = await getUser();
    const data = await supabase.from("rooms").select("creation_date").eq("username", user.username).eq("id", id);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return "";

    let date = new Date(data.data[0].creation_date);
    return date.toLocaleDateString() + " " + date.toLocaleTimeString();
}

export async function DB_SB_get_box_createdat(id, user)
{
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("boxes").select("creation_date").eq("username", user.username).eq("id", id);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return "";

    let date = new Date(data.data[0].creation_date);
    return date.toLocaleDateString() + " " + date.toLocaleTimeString();
}

export async function DB_SB_update_box_name(id, name)
{
    const user = await getUser();
    const {error} = await supabase.from("boxes").update({name: name}).eq("username", user.username).eq('id', id);
    if (error) {
        console.log("Error :", error.message);
        return false;
    }
    return true;
}

export async function DB_SB_update_box_room(id, name)
{
    const user = await getUser();
    let room_id = await DB_SB_get_id_of_room(name);

    const {error} = await supabase.from("boxes").update({room_id: room_id}).eq("username", user.username).eq('id', id);
    if (error) {
        console.log("Error :", error.message);
        return false;
    }
    return true;
}

export async function DB_SB_update_product(mapping_id, box_id, room_id, product_id)
{
    const user = await getUser();

    const {data: product} = await supabase.from("products").select("*").eq("id", product_id).eq("username", user.username);
    if(product === null || product === undefined || product.length === 0)
        return false;

    const {data: mapping} = await supabase.from("productmapping")
        .select("*")
        .eq("product_id", product_id)
        .eq("box_id", box_id)
        .eq("room_id", room_id);
    if(mapping === null || mapping === undefined || mapping.length === 0)
    {
        // insert into mapping table
        await supabase.from("productmapping").update(
            {box_id: box_id, room_id: room_id}
        ).eq("id", mapping_id);
        return true;
    }
    else
    {
        // update amount
        let amount = 0;
        const {data} = await supabase
                                .from("productmapping")
                                .select("amount")
                                .eq("id", mapping_id);
        if(data !== null && data !== undefined && data.length !== 0)
        {
            amount = data[0].amount;
        }
        await DB_SB_change_product_amount(mapping[0].id, amount);
        await DB_SB_delete_product_mapping(mapping_id);
        return true;
    }
}

export async function DB_SB_get_product_createdat(id, user)
{
    if(user === undefined)
        user = await getUser();
    const data = await supabase.from("products").select("creation_date").eq("username", user.username).eq("id", id);
    if(data === undefined || data == null || data.data === undefined || data.data == null || data.data.length === 0)
        return "";

    let date = new Date(data.data[0].creation_date);
    return date.toLocaleDateString() + " " + date.toLocaleTimeString();
}

export async function DB_SB_update_product_amount(id, amount)
{
    const user = await getUser();
    const {error} = await supabase.from("productmapping").update({amount: amount}).eq('id', id);
    if (error) {
        console.log("Error :", error.message);
        return false;
    }
    return true;
}

export async function DB_SB_delete_product(id, mapping_id, delete_all)
{
    const user = await getUser();
    if(delete_all)
    {
        const {error} = await supabase.from("products").delete().eq("username", user.username).eq('id', id);
        if (error) {
            console.log("Error :", error.message);
            return false;
        }
    }
    else
    {
        const {data} = await supabase.from("products").select("*").eq("username", user.username).eq("id", id);
        if(data.length === 0)
        {
            return false;
        }

        const {data: mapping_entries} = await supabase.from("productmapping").select("*").eq("product_id", id);
        if(mapping_entries.length === 1)
        {
            const {error} = await supabase.from("products").delete().eq("username", user.username).eq('id', id);
            if (error) {
                console.log("Error :", error.message);
                return false;
            }
        }
        else
        {
            const {error} = await supabase.from("productmapping").delete().eq('id', mapping_id);
            if (error) {
                console.log("Error :", error.message);
                return false;
            }
        }
    }

    return true;
}

export async function DB_SB_delete_room(id)
{
    const user = await getUser();
    let {data: products} = await supabase.from('products').select("*").eq("username", user.username);
    let user_product_ids = [];
    products.forEach(function(product){
        user_product_ids.push(product.id)
    });

    let {error} = await supabase.from("productmapping").update({room_id: -1}).eq('room_id', id).in("product_id", user_product_ids);
    if (error) {
        console.log("Error :", error.message);
        return false;
    }

    let {error2} = await supabase.from("boxes").update({room_id: -1}).eq("username", user.username).eq('room_id', id);
    if (error2) {
        console.log("Error :", error.message);
        return false;
    }
    await supabase.from("rooms").delete().eq("username", user.username).eq('id', id);
    return true;
}
export async function DB_SB_delete_box(id)
{
    const user = await getUser();
    const {data: roomid} = await supabase.from("boxes").select("room_id").eq("username", user.username).eq("id", id);
    let {data: products} = await supabase.from('products').select("*").eq("username", user.username);
    let user_product_ids = [];
    products.forEach(function(product){
        user_product_ids.push(product.id)
    });

    let {error} = await supabase.from("productmapping").update({box_id: -1, room_id: roomid[0].room_id}).eq('box_id', id).in('product_id', user_product_ids);
    if (error) {
        console.log("Error :", error.message);
        return false;
    }

    await supabase.from("boxes").delete().eq("username", user.username).eq('id', id);
    return true;
}

export async function DB_SB_get_product_by_name(name)
{
    const user = await getUser();

    let {data} = await supabase.from("products").select("*").eq("name", name).eq("username", user.username);
    if(data.length === 0)
        return undefined;
    return data[0];

}

export async function DB_SB_delete_product_mapping(id)
{
    await supabase.from("productmapping").delete().eq("id", id);
}

export async function DB_SB_toggle_starred(id, update)
{
    const user = await getUser();
    await supabase.from("products").update({starred: update}).eq("id", id).eq("username", user.username);
}
