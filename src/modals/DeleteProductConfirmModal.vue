<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="100%"
        height="80%"
    >
        <div class="d-flex-column modal-container-sm">
            <v-toolbar
                class="modal-toolbar justify-content-end "
                :title="this.$t('confirmation_modal.delete')"
            >

                <v-spacer></v-spacer>
                <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"/>
            </v-toolbar>
            <v-card-text>
                <div class="mb-4">
                    <p v-if="this.is_room">
                        {{ this.$t('confirmation_modal.delete_product_at_loc_expl', {loc: this.room_name}) }}
                    </p>
                    <p v-else-if="this.is_box">
                        {{ this.$t('confirmation_modal.delete_product_at_box_expl', {box: this.box_name}) }}
                    </p>
                    <p v-else>
                        {{ this.$t('confirmation_modal.delete_product_at_def_expl') }}
                    </p>
                </div>
                <div>
                    <p>
                        {{this.$t('confirmation_modal.delete_product_expl')}}
                    </p>
                </div>
            </v-card-text>
            <v-card-actions class="justify-space-evenly">
                <v-btn
                    class="deleteProduct"
                    :text="this.$t('confirmation_modal.delete_product')"
                    @click="deleteProduct"
                />
                <v-btn
                    class="deleteProductAtLoc"
                    color="warning"
                    :text="this.$t('confirmation_modal.delete_product_at_loc')"
                    @click="deleteProductAtLocation"
                />
            </v-card-actions>
        </div>

    </v-dialog>
</template>

<script>
import Tag from '@/components/Tag.vue';
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import BiggerButtonCenter from '@/components/BiggerButtonCenter.vue';
import InputDropdown from '@/components/InputDropdown.vue';
import InputStarred from '@/components/InputStarred.vue';

import {
    DB_SB_get_boxes_of_user,
    DB_SB_get_rooms_of_user,
    DB_SB_add_product,
    DB_SB_add_box,
    DB_SB_add_room,
    DB_SB_get_name_of_room_of_box, DB_SB_get_all_products, DB_SB_get_products_without_storage_location
} from '@/db/supabase';
import { getUser } from '@/db/dexie';
import {Constants} from  "@/global/constants";
import {useToast} from "vue-toastification";

export default {
name: 'App',
props: {
    name: "",
    is_room: false,
    is_box: false,
    room_name: "",
    box_name: ""
},
components: {
},
data() {
    return {
    }
},
methods: {
    closeModal()
    {
        this.$emit("closeConfirmationModal");
    },
    deleteProductAtLocation()
    {
        this.$emit("deleteProductAtLocation");
    },
    deleteProduct()
    {
        this.$emit("deleteProduct");
    }
},
beforeMount() {
}
}
</script>

<style scoped>

.deleteProduct{
    background: rgba(255, 0, 0, 0.60);
}
.deleteProductAtLoc{
    border: orange 1px solid;
}
</style>
  