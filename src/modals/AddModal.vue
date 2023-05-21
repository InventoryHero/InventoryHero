<template>
    <div id="mainContainerAddModal">
        <svg @click="closeModal()" id="exitButton" xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 96 960 960" width="48"><path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>
        <div id="addWhat">
            <tag @click="categoryChange(Constants.ProductsView)" text="Product" :active="this.product_active" :hidden="!this.showSelectionTabs(Constants.ProductsView)"> </tag>
            <tag @click="categoryChange(Constants.BoxesView)" :active="this.box_active" text="Box" :hidden="!this.showSelectionTabs(Constants.BoxesView)"> </tag>
            <tag @click="categoryChange(Constants.LocationsView)" :active="this.location_active" text="Location" :hidden="!this.showSelectionTabs(Constants.LocationsView)"> </tag>
        </div>

        <div id="containerWhat" v-if="this.product_active == 'true'">
            <input-text-enhanced @valueUpdated="updateName" placeholder="name"/>
            <input-dropdown :key="redrawBoxes" @valueUpdated="updateSelectedBox" :place_holder="this.place_holder_box" :list=this.boxes :isDisabled='this.preselected_box !== "" '/>
            <input-dropdown :key="redrawRoom" @valueUpdated="updateSelectedRoom" :place_holder="this.place_holder_room" :list=this.rooms :isDisabled='this.lockRoom'/>
            <input-text-enhanced @valueUpdated="updateAmount" placeholder="amount"/>
            <input-starred @valueUpdated="updateStarredProduct" />
            <bigger-button-center @click="addProduct" class="addButton" text="Add Product" />
        </div>

        <div id="containerWhat" v-if="this.box_active == 'true'">
            <input-text-enhanced @valueUpdated="updateName" placeholder="name"/>
            <input-dropdown :key="redrawRoom" @valueUpdated="updateSelectedRoom" :place_holder="this.place_holder_room" :list=this.rooms :isDisabled='this.lockRoom'/>
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

import {
    DB_SB_get_boxes_of_user,
    DB_SB_get_rooms_of_user,
    DB_SB_add_product,
    DB_SB_add_box,
    DB_SB_add_room,
    DB_SB_get_room_of_box
} from '@/db/supabase';
import { getUser } from '@/db/dexie';
import {Constants} from  "@/global/constants";

export default {
name: 'App',
props: {
    defaultAddView: {
        type: String,
        default: Constants.ProductsView
    },
    navbarItems: {
        type: [Array, String],
        default: Constants.All
    },
    preselected_box: {
        type: String,
        default: ""
    },
    preselected_room: {
        type: String,
        default: ""
    }
},
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
      Constants,
      place_holder_box: "box",
      place_holder_room: "room",
      redrawRoom: 0,
      redrawBoxes: 0,
      lockRoom: false,
    }
},
  methods: {
    reloadSelectComponents(boxes, rooms){
        if(boxes)
            this.redrawBoxes += 1;
        if(rooms)
            this.redrawRoom += 1;
    },
    categoryChange(change_to) {

        if (change_to === Constants.ProductsView) {
            this.product_active = "true"; this.box_active = "false"; this.location_active = "false";
        } else if (change_to === Constants.BoxesView)  {
            this.product_active = "false"; this.box_active = "true"; this.location_active = "false";
        } else if(change_to === Constants.LocationsView) {
            this.product_active = "false";
            this.box_active = "false";
            this.location_active = "true";
        } else {
            this.product_active = "true";
            this.box_active = "false";
            this.location_active = "false";
        }
    },
    updateSelectedBox(box, init=false) {
        this.curr_box = box;
        if(init) {
            this.reloadSelectComponents(true, false);
        }

        if(this.curr_room === "")
        {
            DB_SB_get_room_of_box(box).then((room_name) => {
                this.curr_room = room_name;
                this.place_holder_room = room_name;
                this.reloadSelectComponents(false, true);
            });
        }
    },
    updateSelectedRoom(room, init=false) {
        this.curr_room = room;
        if(init) {
            this.reloadSelectComponents(false, true);
        }
        getUser().then((user) =>  DB_SB_get_boxes_of_user(user, room).then((boxes) => this.boxes = boxes))
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
    },
      showSelectionTabs(curr_tab){
          if(this.navbarItems === Constants.All)
              return true;
          if(this.navbarItems === curr_tab || (Array.isArray(this.navbarItems) && this.navbarItems.includes(curr_tab)))
              return true;
          return false;
      },

},
beforeMount() {
    getUser().then((user) => {
        if(Array.isArray(this.navbarItems))
        {
            if(this.navbarItems.includes(this.defaultAddView))
                this.categoryChange(this.defaultAddView)
            else
                this.categoryChange(this.navbarItems.at(0))
        }
        else
        {
            if(this.navbarItems !== Constants.All && this.navbarItems !== this.defaultAddView)
                this.categoryChange(this.navbarItems)
            else
                this.categoryChange(this.defaultAddView)
        }

        if(this.preselected_box !== "")
        {
            this.place_holder_box = this.preselected_box;
            this.updateSelectedBox(this.preselected_box, true);
        }
        else {
            DB_SB_get_boxes_of_user(user).then((boxes) => {
                this.boxes = boxes;
            })
        }

        if(this.preselected_room !== "" && this.curr_room === "")
        {
            this.lockRoom = true;
            this.place_holder_room = this.preselected_room;
            this.updateSelectedRoom(this.preselected_room, true);
        }
        else {
            DB_SB_get_rooms_of_user(user).then((rooms) => {
                this.rooms = rooms;
            });
        }
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
  