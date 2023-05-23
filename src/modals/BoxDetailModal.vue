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
           <input-text-enhanced @valueUpdated="updateBoxName" :place_holder="this.name"/>
           <input-text-enhanced :disabled="true" :place_holder="this.created_at"></input-text-enhanced>
           <input-dropdown @valueUpdated="updateBoxRoom" :place_holder="this.placeholder" :list="this.rooms"/>
         </v-card-text>
         <v-card-actions class="justify-end">
           <v-btn
                   variant="text"
                   @click="closeModalAndUpdateBox()"
           >Save</v-btn>

         </v-card-actions>
       </v-card>

   </v-dialog>

</template>

<script>
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import InputDropdown from '@/components/InputDropdown.vue';
import {
  DB_SB_get_box_createdat,
  DB_SB_get_name_of_room_of_box,
  DB_SB_get_rooms_of_user,
  DB_SB_update_box_name, DB_SB_update_box_room
} from "@/db/supabase";

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
  },
  data() {
    return {
      new_name: "",
      new_room: "",
      created_at: "",
      rooms: [],
      placeholder: "",
    }
  },
  components: {
    InputTextEnhanced,
    InputDropdown
  },
  methods: {
    async closeModalAndUpdateBox()
    {
      let successful = true;
      if(this.new_name !== this.name && this.new_name !== "")
      {
        successful &= await DB_SB_update_box_name(this.id, this.new_name);
      }
      if(this.new_room !== this.placeholder)
      {
        await DB_SB_update_box_room(this.id, this.new_room);
      }
      if(successful)
      {
        this.$emit("closeDetailModal", this.new_name);
      }
      else
      {
        this.$emit("closeDetailModal");
      }

    },
    updateBoxRoom(new_room)
    {
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
    }
  },
  beforeMount() {
    this.updateCreatedDate();
    DB_SB_get_name_of_room_of_box(this.name).then((room) => {
      this.placeholder = room;
    })
    DB_SB_get_rooms_of_user(undefined).then((rooms) => {
      this.rooms = rooms;
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