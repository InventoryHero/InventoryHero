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
           <input-text-enhanced @valueUpdated="updateRoomName" :place_holder="this.name"/>
           <input-text-enhanced :disabled="true" :place_holder="this.created_at"></input-text-enhanced>
         </v-card-text>
         <delete-confirm-modal
                 :name="this.name"
                 type="location"
                 v-model="this.confirm_modal"
                 @closeConfirmationModal="this.confirm_modal=false;"
                 @deleteContainer="deleteRoom"
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
                   @click="closeModalAndUpdateRoom()"
           > {{this.$t('save')}}</v-btn>

         </v-card-actions>
       </v-card>

   </v-dialog>

</template>

<script>
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import {DB_SB_get_room_createdat, DB_SB_update_room_name} from "@/db/supabase";
import {generatePDF} from "@/global/qr_code";
import {useToast} from "vue-toastification";
import {getUser} from "@/db/dexie";
import DeleteConfirmModal from "@/modals/DeleteConfirmModal.vue";

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
    username: String,
  },
  data() {
    return {
      new_name: "",
      created_at: "",
      confirm_modal: false,
    }
  },
  components: {
    DeleteConfirmModal,
    InputTextEnhanced,
  },
  methods: {
    async deleteRoom(){
      this.confirm_modal=false;
      this.$emit("roomDeleted", this.id);
    },
    closeModalAndUpdateRoom()
    {
      if(this.new_name !== this.name && this.new_name !== "")
      {
        DB_SB_update_room_name(this.id, this.new_name).then( (ret) => {
          if(ret) {
            this.toast.success(this.$t('room_detail_modal.toasts.success.rename', {old: this.name, new: this.new_name}))
            this.$emit("closeDetailModal", this.new_name);
          }
          else
            this.toast.success(this.$t('room_detail_modal.toasts.error.rename', {old: this.name}))
            this.$emit("closeDetailModal");
        });
      }
      else
      {
        this.$emit("closeDetailModal")
      }

    },
    closeModal()
    {
      this.$emit("closeDetailModal");
    },
    updateCreatedDate()
    {
      DB_SB_get_room_createdat(this.id).then((created_at) => this.created_at = created_at);
    },
    updateRoomName(new_name)
    {
      this.new_name = new_name;
    },
    async generateQRCode(){
      let username = (await getUser()).username;
      generatePDF(
          JSON.stringify({
            id: this.id,
            is_room: true,
            is_box: false,
            username: username,
          }),
          this.name,
          this.$t('room_detail_modal.qr_code', {loc: this.name})
      );
    }
  },
  beforeMount() {
    this.updateCreatedDate()
  },

}

</script>

<style scoped>
</style>