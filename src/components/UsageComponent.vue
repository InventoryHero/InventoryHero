<template>

    <v-list-item class="entries-align-left colorMe" @click="openDetailModal()">
        <v-list-item-title>
            {{ this.productName }}
            <div class="date-test">
                &lpar; {{ getLocaleDate() }} &rpar;
            </div>

            <v-list-item-subtitle v-if='this.box_name !== "" || this.room_name !== ""' class="entries-align-left">
                {{ getSubtitle() }}
            </v-list-item-subtitle>
        </v-list-item-title>
    </v-list-item>

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
import {getSettings} from "@/db/dexie"
import ProductsDetailModal from "@/modals/ProductsDetailModal.vue";
import LoadAnimation from "@/components/LoadAnimation.vue";

export default {
    components: {
        LoadAnimation,
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
        updated_at: String,
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
    data() {
        return {
            theme: "",
            starred: this.product_starred,
            updatedAmount: this.amount,
            dialog: false,
            curr_room_id: this.room_id,
            curr_box_id: this.box_id,
        }
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
        getLocaleDate(){
            let date = new Date(this.updated_at);
            var options = { day: 'numeric', month: 'short' };
            return date.toLocaleDateString('en-GB', options) + " " + date.toLocaleTimeString();
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
    beforeMount()
    {
        getSettings().then((settings) => {
            this.theme = settings.theme;
        })
    }
}
</script>


<style scoped>
.entries-align-left{
    text-align: left;
    width: 100%;
    word-break: break-word;
}

.date-test{
    font-size: 0.7em;
    display: inline-block
}
.colorMe{
    margin-left: 2%;
    margin-bottom: 5px;
    width: 96%;
    background: rgba(113, 112, 141, 0.3);
    border-radius: 4px;
}
</style>
  
