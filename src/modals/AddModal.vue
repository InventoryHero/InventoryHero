<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="100%"
        height="100%"

    >
        <div class="d-flex-column modal-container" >
            <div class="modal-toolbar ">
                <v-toolbar
                    class="justify-space-evenly vuetify-toolbar-override"
                >
                    <tag
                        class="ms-5"
                        @click="categoryChange(Constants.ProductsView)"
                        :text="this.$t('product')"
                        :active="this.isActive(Constants.ProductsView).toString()"
                        :hidden="!this.showSelectionTabs(Constants.ProductsView)" />
                    <tag
                        @click="categoryChange(Constants.BoxesView)"
                        :active="this.isActive(Constants.BoxesView).toString()"
                        :text="this.$t('box')"
                        :hidden="!this.showSelectionTabs(Constants.BoxesView)"/>
                    <tag
                        @click="categoryChange(Constants.LocationsView)"
                        :active="this.isActive(Constants.LocationsView).toString()"
                        :text="this.$t('location')"
                        :hidden="!this.showSelectionTabs(Constants.LocationsView)"/>
                    <v-spacer :hidden="this.showSelectionTabs(Constants.LocationsView)"/>
                    <v-spacer :hidden="this.showSelectionTabs(Constants.BoxesView)"/>
                    <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"/>

                </v-toolbar>
            </div>

            <div class="modal-content scrollableDiv">
                <div id="containerWhat" v-if="this.isActive(Constants.ProductsView)">
                    <input-dropdown
                        @valueUpdated="setProduct"
                        :emit-full-object="true"
                        :place_holder="this.$t('add_modal.select_product_placeholder')"
                        :list=this.products
                        :isDisabled='false'/>
                    <input-text-enhanced
                        @valueUpdated="updateName"
                        :placeholder="this.$t('add_modal.product_name')"
                        :disabled="this.product_exists"
                        :hidden="this.product_exists"/>
                    <input-dropdown
                        @valueUpdated="updateSelectedBox"
                        :place_holder="this.place_holder_box"
                        :list=this.boxes
                        :isDisabled='this.preselected_box !== "" '/>
                    <input-dropdown
                        @valueUpdated="updateSelectedRoom"
                        :place_holder="this.place_holder_room"
                        :list=this.rooms
                        :isDisabled='this.lockRoom'/>
                    <input-text-enhanced
                        @valueUpdated="updateAmount"
                        :placeholder="this.$t('add_modal.amount_placeholder')"/>
                    <input-starred :starred="this.curr_starred" @valueUpdated="updateStarredProduct" />
                </div>

                <div id="containerWhat" v-if="this.isActive(Constants.BoxesView)">
                    <input-text-enhanced
                        @valueUpdated="updateName"
                        :placeholder="this.$t('add_modal.box_name')"/>
                    <input-dropdown
                        @valueUpdated="updateSelectedRoom"
                        :place_holder="this.place_holder_room"
                        :list=this.rooms
                        :isDisabled='this.lockRoom'/>
                </div>


                <div id="containerWhat" v-if="this.isActive(Constants.LocationsView)">
                    <input-text-enhanced
                        @valueUpdated="updateName"
                        :placeholder="this.$t('add_modal.location_name')"/>
                </div>

            </div>
            <div class="modal-footer">
                <div id="addButton">
                    <v-btn
                        class="addButton"
                        variant="text"
                        @click="addItem"
                    >{{this.getBtnString()}}</v-btn>
                </div>
            </div>


        </div>

    </v-dialog>
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
    DB_SB_get_name_of_room_of_box, DB_SB_get_all_products, DB_SB_get_products_without_storage_location
} from '@/db/supabase';
import { getUser } from '@/db/dexie';
import {Constants} from  "@/global/constants";
import {useToast} from "vue-toastification";

export default {
name: 'App',
setup(){
    const toast = useToast();
    return {toast};
},
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
watch: {
    defaultAddView: function(newVal, oldVal)
    {
        this.active_view = newVal;
    },
    preselected_box: function(newVal, oldVal)
    {
        this.lockRoom = true;
        this.updateSelectedBox(newVal);

    },
    preselected_room: function(newVal, oldVal)
    {
        this.lockRoom = true;
        this.updateSelectedRoom(newVal);

    }
},
data() {
    return {
      active_view: this.defaultAddView,
      rooms: [],
      boxes: [],
      products: [],
      curr_name: "",
      curr_room: "",
      curr_box: "",
      curr_amount: 0,
      curr_starred: false,
      Constants,
      place_holder_box: this.$t('add_modal.box_placeholder'),
      place_holder_room: this.$t('add_modal.location_placeholder'),
      lockRoom: false,
      product_exists: true
    }
},
  methods: {
    setProduct(product){
        if(product.id === -1)
        {
            this.product_exists = false;
            this.curr_name = "";
        }
        else
        {
            this.product_exists = true;
            this.curr_name = product.name;
            this.curr_starred = product.starred;
        }
    },
    isActive(view)
    {
        return view === this.active_view;
    },
    categoryChange(change_to) {
        this.active_view = change_to;
    },
    updateSelectedBox(box) {
        this.curr_box = box;
        this.place_holder_box = box;

        if(this.curr_room === "")
        {
            DB_SB_get_name_of_room_of_box(box).then((room_name) => {
                this.curr_room = room_name;
                this.place_holder_room = room_name;

            });
        }
    },
    updateSelectedRoom(room) {
        this.curr_room = room;
        this.place_holder_room = room;
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
    addItem()
    {
        switch(this.active_view)
        {
            case Constants.ProductsView:
                this.addProduct();
                break;
            case Constants.BoxesView:
                this.addBox();
                break;
            case Constants.LocationsView:
                this.addRoom();
                break;
            default:
                break;
        }
    },
    addProduct() {
        // setting box and room at once is not supported
        if(this.curr_box !== "")
            this.curr_room = "";


        let product = {
            name: this.curr_name,
            box: this.curr_box,
            room: this.curr_room,
            amount: parseInt(this.curr_amount),
            starred: this.curr_starred
        }
        DB_SB_add_product(product).then(() => {
            this.toast.success(
                this.$t('add_modal.add_success_product',
                    {
                        name: product.name
                    }
                )
            );
            this.closeModal();
        });
    },
    closeModal() {
        this.curr_name = ""
        this.curr_room = ""
        this.curr_box = ""
        this.curr_amount = 0
        this.curr_starred = false
        this.place_holder_box = this.$t('add_modal.box_placeholder')
        this.place_holder_room = this.$t('add_modal.location_placeholder')
        this.lockRoom = false
        this.product_exists = true
        this.$emit('closeModal')
    },
    addBox() {
        let box = {
            name: this.curr_name,
            room: this.curr_room
        }
        DB_SB_add_box(box).then(() => {
            this.toast.success(
                this.$t('add_modal.add_success_box',
                    {
                        name: box.name
                    }
                )
            );
            this.closeModal()
        })

    },
    addRoom() {
        let room = {
            name: this.curr_name
        }
        DB_SB_add_room(room).then(() => {
            this.toast.success(
                this.$t('add_modal.add_success_room',
                    {
                        name: room.name
                    }
                )
            );
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
      getBtnString()
      {
          switch(this.active_view)
          {
              case Constants.ProductsView:
                  return this.$t('add_modal.add_btn_product' );
              case Constants.BoxesView:
                  return this.$t('add_modal.add_btn_box' );
              case Constants.LocationsView:
                  return this.$t('add_modal.add_btn_location' );
              default:
                  break;
          }
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
            this.updateSelectedBox(this.preselected_box);
            this.lockRoom = true;
        }
        else {
            DB_SB_get_boxes_of_user(user).then((boxes) => {
                this.boxes = boxes;
            })
        }

        if(this.preselected_room !== "" && this.preselected_box === "")
        {
            this.lockRoom = true;
            this.place_holder_room = this.preselected_room;
            this.updateSelectedRoom(this.preselected_room);
        }
        else {
            DB_SB_get_rooms_of_user(user).then((rooms) => {
                this.rooms = rooms;
            });
        }
        DB_SB_get_products_without_storage_location().then((products) => {
            this.products = products;
            this.products.splice(0, 0, {id: -1, name: this.$t('add_modal.add_new_product')})
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
    width: 90%;
}

.addButton {
    border: rgba(255,255,255,0.5) solid 1px;
    background-color: rgba(0,0,0,0.4);
    backdrop-filter: blur(15px);
    border-radius: 5px;

}
#addButton{
    background: var(--color-dark-theme-lighter);
    border-radius: 5px;
}

</style>
  