import { ref } from 'vue';
import {ProductEndpoint} from "@/api/http";
import {useProducts} from "@/store";
import {ProductStorageMapping} from "@/types/api.ts";
import {useNotification} from "@kyvg/vue3-notification";
import useAxios from "@/composables/useAxios.ts";
import {useI18n} from "vue-i18n";

export default () => {
    const saving = ref(false)
    const deleting = ref(false)
    const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
    const productStore = useProducts()
    const {notify} = useNotification()
    const {t: $t} = useI18n()
    // The reusable logic for adjusting the amount
    const updateStoredAt =
        async (productStoredAt: ProductStorageMapping, updateData: Partial<ProductStorageMapping>) => {
        saving.value = true;
        const {success, updated, deleted} = await productEndpoint.updateProductAt(productStoredAt.id, updateData)
        saving.value = false
        if (!success) {
            return success
        }
        console.log(deleted, updated)
        if(deleted){
            productStore.deleteProductAt(deleted.id, deleted.amount)
        }

        if (updated) {
            productStore.updateProductAt(productStoredAt.id, updated);
        }
        return success
    };

    const deleteStoredAt = async (productStoredAt: ProductStorageMapping) => {
        deleting.value = true
        const success = await productEndpoint.deleteProductAt(productStoredAt.id)
        deleting.value = false
        return success
    }

    return {
        saving,
        deleting,
        updateStoredAt,
        deleteStoredAt
    };
}