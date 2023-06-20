<template>

   <v-dialog
           transition="dialog-bottom-transition"
           width="auto"
           height="100%"
   >

       <v-card
          height="100%"
          class="d-flex-column modal-container"
       >
         <v-toolbar
                 :title="this.name"
                 class="modal-toolbar"
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
                   :place_holder='this.new_box.name === "" ? this.$t("add_modal.box_placeholder") : this.new_box.name'
                   :list='[{id: -1, name: this.$t("add_modal.no_box")}].concat(this.users_boxes)'
                   :emitFullObject="true"/>
           <input-dropdown
                   @valueUpdated="updateSelectedRoom"
                   :place_holder='this.new_room.name === "" ? this.$t("add_modal.location_placeholder") : this.new_room.name'
                   :list='[{id: -1, name: this.$t("add_modal.no_room")}].concat(this.users_rooms)'
                   :emitFullObject="true"
           />
           <input-text-enhanced
                   id="test"
                   type="number"
                   @valueUpdated="updateAmount"
                   :placeholder="this.current_amount.toString()"
           />
           <p :style="{color: 'red'}">{{ error_message }}</p>
         </v-card-text>

         <delete-product-confirm-modal
                 v-model="this.confirmation_modal"
                 :is_box="this.box_id !== -1"
                 :is_room="this.box_id === -1 && this.room_id !== -1"
                 :box_name="this.box_name"
                 :room_name="this.room_name"
                 @deleteProduct="deleteProduct(true)"
                 @deleteProductAtLocation="deleteProduct"
                 @closeConfirmationModal="this.confirmation_modal=false;"
         />


         <v-card-actions class="justify-end">
           <v-btn
                   icon="fa:fas fa-trash"
                   @click="this.confirmation_modal = true;"
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
import DeleteProductConfirmModal from "@/modals/DeleteProductConfirmModal.vue";
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
      current_amount: this.amount,
      confirmation_modal: false,
    }
  },
  setup(){
    const toast = useToast();
    return {toast};
  },
  components: {
    InputTextEnhanced,
    InputDropdown,
    DeleteProductConfirmModal
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

    async deleteProduct(delete_all=false)
    {
      this.confirmation_modal = false;
      if(await DB_SB_delete_product(this.id, this.mapping_id, delete_all))
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
            name:this.$t("add_modal.location_placeholder"),
          }
        }
      })
    },
    updateSelectedRoom(room){
      this.new_room = room;
      this.new_box = {
        id: -1,
        name: this.$t("add_modal.box_placeholder"),
      }
    },
    closeModal(){
      console.log(this.new_box.name);
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



</style>