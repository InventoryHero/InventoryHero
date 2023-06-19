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
           <input-text-enhanced @valueUpdated="updateBoxName" :place_holder="this.name"/>
           <input-text-enhanced :disabled="true" :place_holder="this.created_at"></input-text-enhanced>
           <input-dropdown @valueUpdated="updateBoxRoom" :place_holder="this.placeholder"
                           :list='[{id: -1, name: this.$t("add_modal.no_room")}].concat(this.rooms)'
           />
         </v-card-text>
         <delete-confirm-modal
            :name="this.name"
            type="box"
            v-model="this.confirm_modal"
            @closeConfirmationModal="this.confirm_modal=false;"
            @deleteContainer="deleteBox"
         />
         <v-card-actions class="justify-end">
           <v-btn
             icon="fa:fas fa-qrcode"
             @click="generateQRCode()"
           >
           </v-btn>
           <v-btn
                   icon="fa:fas fa-trash"
                   @click="this.confirm_modal=true"
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
import DeleteConfirmModal from "@/modals/DeleteConfirmModal.vue";
import {
  DB_SB_delete_box,
  DB_SB_get_box_createdat,
  DB_SB_get_name_of_room_of_box,
  DB_SB_get_rooms_of_user,
  DB_SB_update_box_name, DB_SB_update_box_room
} from "@/db/supabase";
import {generatePDF} from "@/global/qr_code";
import {useToast} from "vue-toastification";
import {getUser} from "@/db/dexie";


export default {
  setup(){
    const toast = useToast();
    return {toast};
  },
  props:{
    id: {
      type: Number,
      default: -1
    },
    name: {
      type: String,
      default: "",
    },
    username: String
  },
  watch: {
    name: function(newVal, oldVal)
    {
      this.new_name = newVal;
    }
  },
  data() {
    return {
      created_at: "",
      placeholder: "",
      rooms: [],
      confirm_modal: false,
      new_room: "",
      new_name: this.name,
    }
  },
  components: {
    InputTextEnhanced,
    InputDropdown,
    DeleteConfirmModal
  },
  methods: {
    deleteBox()
    {
      DB_SB_delete_box(this.id).then((result) => {
        if(result)
        {
          this.toast.success(this.$t("box_detail_modal.toasts.success.delete", {name: this.name}));
        }
        else
        {
          this.toast.error(this.$t("box_detail_modal.toasts.error.delete", {name: this.name}));
        }
        this.$emit("boxDeleted");
      });
    },
    async closeModalAndUpdateBox()
    {
      let successful = true;
      if(this.new_name !== this.name && this.new_name !== "")
      {
        successful = await DB_SB_update_box_name(this.id, this.new_name);
      }
      if(this.new_room !== this.placeholder)
      {
        await DB_SB_update_box_room(this.id, this.new_room);
        this.placeholder = this.new_room;
      }
      if(successful)
      {
        this.toast.success(this.$t("box_detail_modal.toasts.success.update", {name: this.name}));
        this.$emit("closeDetailModal", this.new_name);
      }
      else
      {
        this.toast.error(this.$t("box_detail_modal.toasts.error.update", {name: this.name}));
        this.$emit("closeDetailModal");
      }

    },
    updateBoxRoom(new_room)
    {
      if(new_room.id === -1)
      {
        new_room = "";
      }
      this.new_room = new_room;
    },
    closeModal()
    {
      this.$emit("closeDetailModal");
    },
    updateCreatedDate()
    {
      DB_SB_get_box_createdat(this.id).then((created_at) => this.created_at = created_at);
    },
    updateBoxName(new_name)
    {
      this.new_name = new_name;
    },
    async generateQRCode(){
      let username = (await getUser()).username;
      generatePDF(
          JSON.stringify({
            id: this.id,
            is_room: false,
            is_box: true,
            username: username,
          }),
          this.name,
          this.$t("box_detail_modal.qr_code", {box: this.name})
      );
    }
  },
  beforeMount() {
    this.updateCreatedDate();
    DB_SB_get_name_of_room_of_box(this.name).then((room) => {
      this.placeholder = room === "" ? this.$t("add_modal.no_room") : room;
    })
    DB_SB_get_rooms_of_user(undefined).then((rooms) => {
      this.rooms = rooms;
    })
  },

}

</script>

<style scoped>

</style>