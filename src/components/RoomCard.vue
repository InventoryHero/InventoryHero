
<template >
    <v-layout justify="center">
        <v-col>
            <v-card  class="room-card">
                <v-card-title align="start" :id='id' >
                    {{ roomName }}
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
                            <v-icon @click="addBoxOrProduct(id)" size="x-large" icon="mdi-plus"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="informationButton(id)" size="large" icon="mdi-information"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                </div>
            </v-card>
        </v-col>
    </v-layout>
</template>

<script>



  export default {
      props: {
          id: Number,
          roomName: String,
          numBoxes: Number,
          numProducts: Number,
      },
      methods: {
          informationButton: function(cardId)
          {

              console.log("you've clicked the information button " + cardId);
          },
          addBoxOrProduct: function(cardId)
          {
              console.log("Adding box or product for room: " + cardId);
          },
          productsOverview: function(roomId)
          {
              console.log("Showing all products in room: " + roomId);
          },
          boxesOverview: function(roomId)
          {
              console.log("hallo");
              this.$router.push( "/boxesFilteredView?room_id="+roomId);
              console.log("Showing all boxes in room: " + roomId);
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