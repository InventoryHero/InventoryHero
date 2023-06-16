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
           <input-text-enhanced @valueUpdated="updateRoomName" :place_holder="this.name"/>
           <input-text-enhanced :disabled="true" :place_holder="this.created_at"></input-text-enhanced>
         </v-card-text>
         <v-card-actions class="justify-end">
           <v-btn
                   icon="fa:fas fa-qrcode"
                   @click="generateQRCode()"
           >
           </v-btn>
           <v-btn
                   icon="fa:fas fa-trash"
                   @click="deleteRoom()"
           ></v-btn>
           <v-btn
                   variant="text"
                   @click="closeModalAndUpdateRoom()"
           >Save</v-btn>

         </v-card-actions>
       </v-card>

   </v-dialog>

</template>

<script>
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import {DB_SB_get_room_createdat, DB_SB_update_room_name} from "@/db/supabase";
import {generatePDF} from "@/global/qr_code";

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
    username: String,
  },
  data() {
    return {
      new_name: "",
      created_at: ""
    }
  },
  components: {
    InputTextEnhanced,
  },
  methods: {
    async deleteRoom(){

      this.$emit("roomDeleted", this.id);
    },
    closeModalAndUpdateRoom()
    {
      if(this.new_name !== this.name && this.new_name !== "")
      {
        DB_SB_update_room_name(this.id, this.new_name).then( (ret) => {
          if(ret)
            this.$emit("closeDetailModal", this.new_name);
          else
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
    generateQRCode(){
      generatePDF(
          JSON.stringify({
            id: this.id,
            is_room: true,
            is_box: false,
            username: this.username,
          }),
          this.name,
          "QR-Code for room " + this.name
      );
    }
  },
  beforeMount() {
    this.updateCreatedDate()
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