
<template >
    <v-layout justify="center">
        <v-col>
            <v-card class="box-card">
                <v-card-title align="start" :id='id' >
                    {{ this.box_name }}
                </v-card-title>
                <div class="d-flex align-center justify-space-evenly box-info mt-1 mb-2 ms-2 me-2 rounded-pill" :class="theme">
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
                            <v-icon @click="this.$emit('addItemToBox', id)" size="x-large" icon="mdi-plus"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="openDetailModal()" size="large" icon="mdi-information"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                </div>
            </v-card>
        </v-col>
        <box-detail-modal
            :id="id"
            :name="this.boxName"
            :username="this.username"
            v-model="this.dialog"
            @closeDetailModal="closeModal"
            @boxDeleted="boxDeleted"/>
    </v-layout>
</template>

<script>
import BoxDetailModal from "@/modals/BoxDetailModal.vue";
import {useToast} from "vue-toastification";
import {getSettings} from "@/db/dexie";


export default {
    components: {BoxDetailModal},
    props: {
        id: Number,
        boxName: String,
        numProducts: Number,
        numStarredProducts: Number ,
        username: String,
    },
    data() {
        return {
            dialog: false,
            box_name: this.boxName,
            theme: ""
        }
    },
    methods: {
        boxDeleted()
        {
        this.dialog=false;
        this.$emit("boxDeleted");
        },
        closeModal(new_boxname)
        {
            if(new_boxname !== undefined && new_boxname !== "") {
                this.box_name = new_boxname;
                this.$emit("refreshData")
            }
            this.dialog = false
        },
        openDetailModal()
        {
            this.dialog = true;
        },
        productsOverview: function(cardId)
        {
            this.$router.push( "/productsFilteredView?box_id="+cardId);
        },
        starredProductsOverview: function(cardId)
        {
            this.$router.push( "/productsFilteredView?box_id="+cardId+"&starred=true");
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
.box-info .dark-theme{
    background-color: var(--color-dark-theme-background);
    color: white;
    height: 2em;
}
.box-card {
    background-color: var(--color-dark-theme-lighter);
    color: white;
}

.box-info .light-theme{
    background-color: var(--color-light-theme-background);
    color: white;
    height: 2em;
}

.light-theme i {
    color: black
}

.dark-theme {
    background-color: var(--color-dark-theme-darker);
    color: white;
}

.light-theme {
    background-color: var(--color-light-theme-darker);
    color: black;
}

</style>