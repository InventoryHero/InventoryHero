<template>

   <v-dialog
           transition="dialog-bottom-transition"
           width="auto"
   >

       <v-card
          height="100%"
          class="d-flex-column modal-container"
       >
         <v-toolbar
                 :title="this.name"
                 class="toolbar"
         >
         <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"></v-icon>
         </v-toolbar>
         <v-card-text>
           <input-text-enhanced
                   :disabled="true"
                   :place_holder="this.created_at"
           />
           <input-dropdown
                   @valueUpdated="updateSelectedBox"
                   :place_holder="this.new_box.name"
                   :list=this.users_boxes
                   :emitFullObject="true"/>
           <input-dropdown
                   @valueUpdated="updateSelectedRoom"
                   :place_holder="this.new_room.name"
                   :list=this.users_rooms
                   :emitFullObject="true"/>
           <input-text-enhanced
                   id="test"
                   type="number"
                   @valueUpdated="updateAmount"
                   :placeholder="this.current_amount.toString()"
           />
           <p :style="{color: 'red'}">{{ error_message }}</p>
         </v-card-text>
         <v-card-actions class="justify-end">
           <v-btn
                   icon="fa:fas fa-trash"
                   @click="deleteProduct()"
           ></v-btn>
           <v-btn
                   variant="text"
                   @click="closeModalAndUpdateBox()"
           >{{this.$t('save')}}</v-btn>
         </v-card-actions>
       </v-card>

   </v-dialog>

</template>

<script>
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import InputDropdown from '@/components/InputDropdown.vue';
import {
  DB_SB_delete_product,
  DB_SB_get_boxes_of_user,
  DB_SB_get_product_createdat,
  DB_SB_get_room_of_box,
  DB_SB_get_rooms_of_user, DB_SB_update_product,
  DB_SB_update_product_amount,
} from "@/db/supabase";
import {getUser} from "@/db/dexie";
import {useToast} from "vue-toastification";

export default {
  props:{
    id: {
      type: Number,
      default: -1
    },
    name: {
      type: String,
      default: "",
    },
    mapping_id: -1,
    box_id: -1,
    room_id: -1,
    box_name: "",
    room_name: "",
    amount: {
      type: Number,
      default: 0,
    }
  },
  watch: {
    amount: function(newVal, oldVal){
      this.current_amount = newVal;
    },
    box_id: function(newVal, oldVal){
      this.new_box.id = newVal;
    },
    box_name: function(newVal, oldVal){
      this.new_box.name = newVal;
    },
    room_id: function(newVal, oldVal){
      this.new_room.id = newVal;
    },
    room_name: function(newVal, oldVal){
      this.new_room.name = newVal;
    }
  },
  data() {
    return {
      created_at: "",
      new_box: {
        id: this.box_id,
        name: this.box_name
      },
      new_room: {
        id: this.room_id,
        name: this.room_name
      },
      users_boxes: [],
      users_rooms: [],
      error_message: "",
      current_amount: this.amount
    }
  },
  setup(){
    const toast = useToast();
    return {toast};
  },
  components: {
    InputTextEnhanced,
    InputDropdown
  },
  methods: {
    async closeModalAndUpdateBox(){
        if(this.error_message !== "")
          return;


        if(this.current_amount !== this.amount)
        {
          if(await DB_SB_update_product_amount(this.mapping_id, this.current_amount))
          {
            this.toast.success(this.$t('product_detail_modal.toasts.success.amountUpdate', {name: this.name}));
          }
          else
          {
            this.toast.success(this.$t('product_detail_modal.toasts.success.amountUpdate', {name: this.name}));
            this.closeModal();
          }
        }

        if(this.new_box.id !== this.box_id || this.new_room.id !== this.room_id)
        {
          let room_id = this.new_room.id;
          if(this.new_box.id !== -1)
          {
            room_id = -1;
          }
          if(await DB_SB_update_product(this.mapping_id, this.new_box.id, room_id, this.id))
          {
            this.toast.success(this.$t('product_detail_modal.toasts.success.update', {name: this.name}));
          }
          else
          {
            this.toast.error(this.$t('product_detail_modal.toasts.error.update', {name: this.name}));
          }

          this.$emit("reloadProducts");
          return;
        }
        this.$emit("closeDetailModal", this.current_amount);
    },
    async deleteProduct()
    {
      if(await DB_SB_delete_product(this.id))
      {
        this.toast.success(this.$t('product_detail_modal.toasts.success.delete', {name: this.name}));
      }
      else
      {
        this.toast.error(this.$t('product_detail_modal.toasts.error.delete', {name: this.name}));
      }
      this.$emit("productDeleted");
    },
    updateSelectedBox(box) {
      this.new_box = box;

      DB_SB_get_room_of_box(this.new_box.id).then((room) => {
        if(room.length > 0)
        {
          this.new_room = {
            id: room[0].id,
            name: room[0].name
          }
        }
        else
        {
          this.new_room = {
            id: -1,
            name: "",
          }
        }
      })
    },
    updateSelectedRoom(room){
      this.new_room = room;
      this.new_box = {
        id: -1,
        name: "",
      }
    },
    closeModal(){
      this.new_box = {
        id: this.box_id,
            name: this.box_name
      }
      this.new_room =  {
        id: this.room_id,
            name: this.room_name
      }

      this.$emit("closeDetailModal");
    },
    updateAmount(new_amount){
      if(new_amount < 0)
        this.error_message = this.$t('product_detail_modal.amount_below_zero');
      else
        this.error_message = "";
      this.current_amount = new_amount;
    },
  },
  beforeMount() {
    getUser().then((user) => {
      DB_SB_get_rooms_of_user(user).then((rooms) => {
        this.users_rooms = rooms;
      })
      DB_SB_get_boxes_of_user(user).then((boxes) => {
        this.users_boxes = boxes;
      })
      DB_SB_get_product_createdat(this.id, user).then( (created_at) => {
            this.created_at = created_at
      });
    })



  },

}

</script>

<style scoped>
.modal-container{
   background-color: rgba(0,0,0,0.5);
   backdrop-filter: blur(15px);
   border-radius: 10px;
   border: white solid 1px;
   height: 60vh;
   color: white;
 }
.toolbar{
    background-color: transparent;
    border-bottom: white solid 1px;
    color: white;
}


</style>