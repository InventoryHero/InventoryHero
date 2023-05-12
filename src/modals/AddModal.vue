<template>
    <div id="mainContainerAddModal">
        <svg @click="closeModal()" id="exitButton" xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 96 960 960" width="48"><path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>
        <div id="addWhat">
            <tag @click="categoryChange('product')" text="Product" :active="this.product_active"> </tag>
            <tag @click="categoryChange('box')" :active="this.box_active" text="Box"> </tag>
            <tag @click="categoryChange('location')" :active="this.location_active" text="Location"> </tag>
        </div>

        <div id="containerWhat" v-if="this.product_active == 'true'">
            <input-text-enhanced @valueUpdated="updateName" placeholder="name"/>
            <input-dropdown @valueUpdated="updateSelectedBox" place_holder="box" :list=this.boxes />
            <input-dropdown @valueUpdated="updateSelectedRoom" place_holder="room" :list=this.rooms />
            <input-text-enhanced @valueUpdated="updateAmount" placeholder="amount"/>
            <input-starred @valueUpdated="updateStarredProduct" />
            <bigger-button-center @click="addProduct" class="addButton" text="Add Product" />
        </div>

        <div id="containerWhat" v-if="this.box_active == 'true'">
            <input-text-enhanced @valueUpdated="updateName" placeholder="name"/>
            <input-dropdown @valueUpdated="updateSelectedRoom" place_holder="room" :list=this.rooms />
            <bigger-button-center @click="addBox" class="addButton" text="Add Box" />
        </div>


        <div id="containerWhat" v-if="this.location_active == 'true'">
            <input-text-enhanced @valueUpdated="updateName" placeholder="name"/>
            <bigger-button-center @click="addRoom" class="addButton" text="Add Location" />
        </div>

    </div>
</template>

<script>
import Tag from '@/components/Tag.vue';
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import BiggerButtonCenter from '@/components/BiggerButtonCenter.vue';
import InputDropdown from '@/components/InputDropdown.vue';
import InputStarred from '@/components/InputStarred.vue';

import { DB_SB_get_boxes_of_user, DB_SB_get_rooms_of_user, DB_SB_add_product, DB_SB_add_box, DB_SB_add_room } from '@/db/supabase';
import { getUser } from '@/db/dexie';

export default {
name: 'App',
components: {
    Tag,
    InputTextEnhanced,
    BiggerButtonCenter,
    InputDropdown,
    InputStarred
}, 
data() {
    return {
      product_active: "true",
      box_active: "false",
      location_active: "false",
      rooms: [],
      boxes: [],
      curr_name: "",
      curr_room: "",
      curr_box: "",
      curr_amount: 0,
      curr_starred: false,
    }
},
  methods: {
    categoryChange(change_to) {
        if (change_to == "product") {
            this.product_active = "true"; this.box_active = "false"; this.location_active = "false";
        } else if (change_to == "box")  {
            this.product_active = "false"; this.box_active = "true"; this.location_active = "false";
        } else {
            this.product_active = "false"; this.box_active = "false"; this.location_active = "true";
        }
    },
    updateSelectedBox(box) {
        this.curr_box = box;
    },
    updateSelectedRoom(room) {
        this.curr_room = room;
    },
    updateStarredProduct(starred) {
        this.curr_starred = starred;
    },
    updateAmount(amount) {
        this.curr_amount = amount;
    },
    updateName(name) {
        this.curr_name = name;
    },
    addProduct() {
        let product = {
            name: this.curr_name,
            box: this.curr_box,
            room: this.curr_room,
            amount: this.curr_amount,
            starred: this.curr_starred
        }
        DB_SB_add_product(product).then(() => {
            this.closeModal();
        });
    },
    closeModal() {
        this.$emit('closeModal')
    },
    addBox() {
        let box = {
            name: this.curr_name,
            room: this.curr_room
        }
        DB_SB_add_box(box).then(() => {
            this.closeModal()
        })

    },
    addRoom() {
        let room = {
            name: this.curr_name
        }
        DB_SB_add_room(room).then(() => {
            this.closeModal()
        })
    }
},
beforeMount() {
    getUser().then((user) => {
        DB_SB_get_boxes_of_user(user).then((boxes) => {
            this.boxes = boxes;
        });
        DB_SB_get_rooms_of_user(user).then((rooms) => {
            this.rooms = rooms;
        });

    })

}
}
</script>

<style scoped>
#mainContainerAddModal {
    position: absolute;
    top: 20vh;
    left: 5vw;
    right: 5vw;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    border-radius: 10px;
    border: white solid 1px;
    height: 60vh;
}

#exitButton {
    position: absolute;
    right: 10px;
    top: 10px;
    fill: white;
    border: 1px solid white;
    border-radius: 10px;
    cursor: pointer;
}

#addWhat {
    position: absolute;
    display: flex;
    top: 10vh;
    left: 50%;
    transform: translateX(-50%);
}

#containerWhat {
    position: absolute;
    top: 17vh;
    left: 5%;
    bottom: 10px;
    width: 90%;
}

.addButton {
    position: absolute;
    bottom: 10px;
}
</style>
  