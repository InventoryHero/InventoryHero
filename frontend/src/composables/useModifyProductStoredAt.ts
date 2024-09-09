import {ProductEndpoint} from "@/api/http";
import {useProducts} from "@/store";
import {ProductStorageMapping} from "@/types/api.ts";
import useAxios from "@/composables/useAxios.ts";

export default () => {
    const saving = ref(false)
    const deleting = ref(false)
    const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
    const productStore = useProducts()
    // The reusable logic for adjusting the amount
    const updateStoredAt =
        async (productStoredAt: ProductStorageMapping, updateData: Partial<ProductStorageMapping>) => {
        saving.value = true;
        const {success, updated, deleted} = await productEndpoint.updateProductAt(productStoredAt.id, updateData)
        saving.value = false
        if (!success) {
            return success
        }

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