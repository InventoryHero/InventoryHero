
<template >
    <v-layout justify="center">
        <v-col>
            <v-card  class="room-card">
                <v-card-title align="start" :id='id' >
                    {{ productName }}
                </v-card-title>
                <v-card-subtitle v-if='this.box_name !== "" || this.room_name !== ""' align="start">
                    {{ getSubtitle() }}
                </v-card-subtitle>
                <div class="d-flex align-center justify-space-evenly room-info mt-1 mb-2 ms-2 me-2 rounded-pill" :class="theme">
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon class="me-2" icon="fa:fas fa-shopping-cart"/>{{this.updatedAmount}}
                            </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact" >
                        <v-list-item-subtitle>
                            <v-icon @click="increaseAmount()" icon="mdi-plus"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="decreaseAmount()" size="x-large" icon="mdi-minus"/>
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item density="compact">
                        <v-list-item-subtitle>
                            <v-icon @click="starItem()" size="large" :icon="getStarColor()"/>
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
    </v-layout>
    <products-detail-modal
        @closeDetailModal="closeModal"
        @productDeleted="deletedProduct"
        @reloadProducts="reloadProducts"
        :id="this.id"
         v-model="this.dialog"
        :name="this.productName"
        :box_id="this.curr_box_id"
        :room_id="this.curr_room_id"
        :room_name="this.room_name"
        :box_name="this.box_name"
        :amount="this.updatedAmount"
        :mapping_id="this.mapping_id"
    />
</template>

<script>
import {
    DB_SB_change_product_amount, DB_SB_toggle_starred,
} from '@/db/supabase';
import { DB_SB_get_product } from '@/db/supabase';
import ProductsDetailModal from "@/modals/ProductsDetailModal.vue";
import {useToast} from "vue-toastification";
import {getSettings} from "@/db/dexie"

export default {
    setup(){
        const toast = useToast();
        return {toast};
    },
    components: {
    ProductsDetailModal
    },
    props: {
        id: Number,
        room_id: Number,
        box_id: Number,
        productName: String,
        amount: {
            type: Number,
            default: 0,
        },
        room_name: String,
        box_name: String,
        mapping_id: Number,
        product_starred: Boolean,
    },
    watch: {
    amount: function(newVal, oldVal)
    {
        this.updatedAmount = newVal;
    },
    product_starred: function(newVal, oldVal)
    {
        this.starred = newVal;
    }

    },
    data(){
    return{
        starred: this.product_starred,
        updatedAmount: this.amount,
        dialog: false,
        curr_room_id: this.room_id,
        curr_box_id: this.box_id,
        theme: ""
    };
    },
    methods: {
        getSubtitle()
        {
            if(this.box_name === "" && this.room_name !== "")
                return this.room_name;
            else if(this.box_name !== "" && this.room_name === "")
                return this.box_name;
            else
                return this.room_name + " | " + this.box_name;
        },
        deletedProduct()
        {
            this.dialog=false;
            this.$emit("productDeleted");
        },
        reloadProducts()
        {
            this.$emit("reloadProducts");
            this.dialog = false;
        },
        closeModal(new_amount = -1)
        {
            if(new_amount !== -1 && new_amount !== this.updatedAmount)
            {
                this.updatedAmount = new_amount;
            }

            this.dialog = false;
        },
        openDetailModal()
        {
            this.dialog = true;
        },
        increaseAmount: function()
        {
            DB_SB_change_product_amount(this.mapping_id, 1) .then((updated_amount) => {
            if(updated_amount !== -1){
                this.updatedAmount = updated_amount;
                this.toast.success(this.$t('products_card.toasts.success.amountUpdate', {name: this.productName}));
            }
            else
            {
                this.toast.success(this.$t('products_card.toasts.success.amountUpdate', {name: this.productName}));
            }
        })
        .catch(error => {
            console.log(error.message);
        });
            
        },
        decreaseAmount: function()
        {
            if(this.updatedAmount === 0)
            {
                return;
            }
            DB_SB_change_product_amount(this.mapping_id, -1).then((updated_amount) =>
            {
                if(updated_amount !== -1){
                    this.updatedAmount = updated_amount;
                    this.toast.success(this.$t('products_card.toasts.success.amountUpdate', {name: this.productName}));
                }
                else
                {
                    this.toast.success(this.$t('products_card.toasts.success.amountUpdate', {name: this.productName}));
                }
            })
            .catch(error => {
                console.log(error.message);
            });
    },
        starItem()
        {
            DB_SB_toggle_starred(this.id, !this.starred).then(() => {
                this.starred = !this.starred;
                this.$emit("toggledStarred", this.id);
            });

        },
        getStarColor()
        {
            if(this.starred)
            {
                return "fa:fas fa-star";
            }
            return "fa:far fa-star";
        }
    },
    beforeMount(){
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