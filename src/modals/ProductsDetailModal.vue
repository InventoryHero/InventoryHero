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
           <input-text-enhanced :disabled="true" :place_holder="this.created_at"></input-text-enhanced>
           <input-dropdown :key="this.redraw_boxes" @valueUpdated="updateSelectedBox" :place_holder="this.ph_boxes" :list=this.users_boxes :emitFullObject="true"/>
           <input-dropdown :key="this.redraw_rooms" @valueUpdated="updateSelectedRoom" :place_holder="this.ph_rooms" :list=this.users_rooms :emitFullObject="true"/>
           <input-text-enhanced id="test" type="number" @valueUpdated="updateAmount" label="Amount:" :placeholder="this.current_amount.toString()"></input-text-enhanced>
           <p :style="{color: 'red'}">{{ error_message }}</p>
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
  DB_SB_get_box_name,
  DB_SB_get_boxes_of_user,
  DB_SB_get_product_createdat,
  DB_SB_get_room_name,
  DB_SB_get_room_of_box,
  DB_SB_get_rooms_of_user,
  DB_SB_update_product_amount,
  DB_SB_update_product_box,
  DB_SB_update_product_room,
} from "@/db/supabase";
import {getUser} from "@/db/dexie";

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
    box_id: -1,
    room_id: -1,
    amount: {
      type: Number,
      default: 0,
    }
  },
  data() {
    return {
      created_at: "",
      new_box: {
        id: this.box_id,
        name: ""
      },
      new_room: {
        id: this.room_id,
        name: ""
      },
      users_boxes: [],
      users_rooms: [],
      redraw_boxes: 0,
      redraw_rooms: 0,
      ph_rooms: "",
      ph_boxes: "",
      error_message: "",
      current_amount: this.amount
    }
  },
  components: {
    InputTextEnhanced,
    InputDropdown
  },
  methods: {
    async closeModalAndUpdateBox(){
        if(this.error_message !== "")
          return;
        if(this.new_box.id !== this.box_id)
        {
          this.new_room = undefined
          if(!await DB_SB_update_product_box(this.id, this.new_box.id))
          {
            this.closeModal();
          }
        }
        else if(this.new_room.id !== this.room_id)
        {
          this.new_box = undefined
          if(!await DB_SB_update_product_room(this.id, this.new_room.id))
          {
            this.closeModal();
          }
        }
        if(this.current_amount !== this.amount)
        {
          if(!await DB_SB_update_product_amount(this.id, this.current_amount))
          {
            this.closeModal();
          }
        }
        this.$emit("closeDetailModal", this.new_room, this.new_box, this.current_amount);
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
          this.ph_rooms = room[0].name;
          this.redrawDropdowns(false, true);

        }
      })
    },
    updateSelectedRoom(room){
      this.new_room = room;
      this.new_box = {
        id: this.box_id,
        name: this.box_name,
      }
      this.ph_boxes = "";
      this.redrawDropdowns(true, false);
    },
    closeModal(){
      this.$emit("closeDetailModal");
    },
    updateAmount(new_amount){
      if(new_amount < 0)
        this.error_message = "Amount cannot be below zero!";
      else
        this.error_message = "";
      this.current_amount = new_amount;
    },
    redrawDropdowns(boxes, rooms){
      if(boxes)
        this.redraw_boxes += 1;
      if(rooms)
        this.redraw_rooms += 1;
    }
  },
  beforeMount() {
    getUser().then((user) => {
      DB_SB_get_rooms_of_user(user).then((rooms) => {
        this.users_rooms = rooms;
      })
      DB_SB_get_boxes_of_user(user).then((boxes) => {
        this.users_boxes = boxes;
      })

      if(this.room_id !== -1)
      {
        DB_SB_get_room_name(this.room_id, user).then( (name) => {
          this.ph_rooms = name;
          this.new_room.name = name;
          this.new_box = {
            id: -1, name: ""
          }
          this.ph_boxes = "";
        })
      }
      else
      {
        DB_SB_get_box_name(this.box_id, user).then((name) => {
          this.new_box.name = name;
          this.ph_boxes = name;
          this.redrawDropdowns(true, false);
        })
        DB_SB_get_room_of_box(this.box_id, user).then((room) => {
          if(room.length > 0)
          {
            this.new_room = {
              id: room[0].id, name: room[0].name
            }
            this.ph_rooms = room[0].name;
            this.redrawDropdowns(false, true);
          }
        })
      }
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