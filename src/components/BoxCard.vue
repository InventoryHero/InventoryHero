
<template >
    <v-layout justify="center">
        <v-col>
            <v-card class="box-card">
                <v-card-title align="start" :id='id' >
                    {{ boxName }}
                </v-card-title>
                <div class="d-flex align-center justify-space-evenly box-info mt-1 mb-2 ms-2 me-2 rounded-pill" >
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="productsOverview(id)" class="me-3" icon="fa:fas fa-shopping-cart"/>{{this.numProducts}}
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="starredProductsOverview(id)" class="me-3" icon="fa:fas fa-star"/>{{this.numStarredProducts}}
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="$emit('addItemToBox', id)" size="x-large" icon="mdi-plus"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="informationButton(id)" size="large" icon="mdi-information"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <!-- <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon size="large" class="me-3" icon="fa:fas fa-eye"/>{{this.numUsage}}
                        </v-list-item-subtitle>
                    </v-list-item> -->
                </div>
            </v-card>
        </v-col>
    </v-layout>
</template>

<script>
  export default {
      props: {
          id: Number,
          boxName: String,
          numProducts: Number,
          numStarredProducts: Number ,
      },
      methods: {
          informationButton: function(cardId)
          {
              console.log("you've clicked the information button " + cardId);
          },
          addProduct: function(cardId)
          {
              console.log("Adding product for box: " + cardId);
          },
          productsOverview: function(cardId)
          {
              this.$router.push( "/productsFilteredView?box_id="+cardId);
          },
          starredProductsOverview: function(cardId)
          {
              console.log("Showing all products in box: " + cardId);
          }
      }
  }
</script>


<style scoped>
    .box-info {
        background-color: var(--color-blue);
        color: white;
        height: 2em;
    }
    .box-card{
        background-color: var(--color-darker);
        color: white;
    }


</style>