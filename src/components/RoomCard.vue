
<template>
    <v-layout justify="center">
        <v-col>
            <v-card  class="room-card">
                <v-card-title align="start" :id='id' >
                    {{ this.name }}
                </v-card-title>
                <div class="d-flex align-center justify-space-evenly room-info mt-1 mb-2 ms-2 me-2 rounded-pill" >
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="boxesOverview(id)" class="me-3" icon="fa:fas fa-boxes"/>{{this.numBoxes}}
                            </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="productsOverview(id)" class="me-3" icon="fa:fas fa-shopping-cart"/>{{this.numProducts}}
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="$emit('addItemToRoom', id)" size="x-large" icon="mdi-plus"> </v-icon>

                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="openDetailModal()" size="large" icon="mdi-information">
                            </v-icon>
                        </v-list-item-subtitle>
                    </v-list-item>
                </div>
            </v-card>
        </v-col>
        <room-detail-modal
            :id="id"
            :name="this.roomName"
            v-model="this.dialog"
            :username="this.username"
            @closeDetailModal="informationButton"
            @roomDeleted="roomDeleted"/>
    </v-layout>
</template>

<script>
import RoomDetailModal from "@/modals/RoomDetailModal.vue";
import {useToast} from "vue-toastification";
  export default {
      setup(){
          const toast = useToast();
          return {toast};
      },
      components: {
          RoomDetailModal
      },
      props: {
          id: Number,
          roomName: String,
          numBoxes: Number,
          numProducts: Number,
          username: String,

      },
      data() {
          return {
              dialog: false,
              name: this.roomName
          }
      },
      methods: {
        roomDeleted(id)
        {
          this.dialog = false;
          this.$emit("roomDeleted", id);
        },
        informationButton(new_name)
        {
            if(new_name !== undefined && new_name !== "") {
                this.toast.success("Successfully renamed room");
                this.name = new_name
            }
            this.dialog=false;
        },
        openDetailModal()
        {
            this.dialog = true;
        },
        productsOverview: function(roomId)
        {
            this.$router.push( "/productsFilteredView?room_id="+roomId);
        },
        boxesOverview: function(roomId)
        {
            this.$router.push( "/boxesFilteredView?room_id="+roomId);
        }
    }
}
</script>


<style scoped>
    .room-info {
        background-color: var(--color-blue);
        color: white;
        height: 2em;
    }
    .room-card{
        background-color: var(--color-darker);
        color: white;
    }
</style>