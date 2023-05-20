
<template >
    <v-layout justify="center">
        <v-col>
            <v-card  class="room-card">
                <v-card-title align="start" :id='id' >
                    {{ productName }}
                </v-card-title>
                <div class="d-flex align-center justify-space-evenly room-info mt-1 mb-2 ms-2 me-2 rounded-pill" >
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="totalAmount(id)" class="me-3" icon="fa:fas fa-boxes"/>{{this.amount}}
                            </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="increaseAmount(id)" class="me-3" icon="mdi-plus"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="decreaseAmount(id)" size="x-large" icon="mdi-minus"/>
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
          productName: String,
          amount: Number,

      },
      methods: {
          informationButton: function(cardId)
          {
              console.log("you've clicked the information button " + cardId);
          },
          totalAmount: function(cardID)
          {
              console.log("Showing all products " + cardID);
          },
          increaseAmount: function(cardId)
          {
              console.log("Increased amount by one " + cardId);
          },
          decreaseAmount: function(cardId)
          {
              console.log("Decreased amount by one " + cardId);
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