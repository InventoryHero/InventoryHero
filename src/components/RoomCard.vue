
<template>
    <v-layout justify="center">
        <v-col>
            <v-card  class="room-card">
                <v-card-title align="start" :id='id' >
                    {{ this.name }}
                </v-card-title>
                <div class="d-flex align-center justify-space-evenly room-info mt-1 mb-2 ms-2 me-2 rounded-pill" :class="theme">
                    <v-icon @click="boxesOverview(id)"  size="x-small" icon="fa:fas fa-boxes"/><p style="margin-left: -7.5%">{{this.numBoxes}}</p>
                    <v-icon @click="productsOverview(id)" size="x-small" icon="fa:fas fa-shopping-cart"/><p style="margin-left: -7.5%">{{this.numProducts}}</p>
                    <v-icon @click="$emit('addItemToRoom', id)" size="large" icon="mdi-plus"/>
                    <v-icon @click="openDetailModal()" size="x-small" icon="fa:fas fa-info-circle"/>
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
import {getSettings} from "@/db/dexie";

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
              name: this.roomName,
              theme: ""
          }
      },
      methods: {
        roomDeleted(id)
        {
          this.dialog = false;
          this.$emit("roomDeleted", id, this.roomName);
        },
        informationButton(new_name)
        {
            if(new_name !== undefined && new_name !== "") {
                this.name = new_name
                this.$emit("refreshData")
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
    },
      beforeMount() {
          getSettings().then((settings) => {
              this.theme =  settings.theme;
          })
      }
  }
</script>


<style scoped>
    .room-info .dark-theme{
    background-color: var(--color-dark-theme-background);
    color: white;
    height: 2em;
}
.room-card {
    background-color: var(--color-dark-theme-lighter);
    color: white;
}

.room-info .light-theme{
    background-color: var(--color-light-theme-background);
    color: white;
    height: 2em;
}
.dark-theme {
    background-color: var(--color-dark-theme-darker);
    color: white;
}

.light-theme {
    background-color: var(--color-light-theme-darker);
    color: black;
}
.light-theme i {
    color: black
}


.dark-theme i {
    color: lightgray;
}
</style>