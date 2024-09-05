import {defineStore} from "pinia";
import {ApiProduct, ApiStorage, Product, ProductStorageMapping} from "@/types/api.ts";

export const useProducts =  defineStore("products", {
    state: () => {
        return {
            _products: [] as Array<ApiProduct>,
            _storage: [] as Array<ProductStorageMapping>,
            _selectedProduct: undefined as ApiProduct | undefined,
            _selectedProductStorage: undefined as ProductStorageMapping | undefined
        }
    },
    actions: {
        storeProducts(products: Array<ApiProduct>){
            this._products = [...products]
        },
        storeProductStorage(storage: Array<ProductStorageMapping>){
            this._storage = [...storage]
        },
        selectProduct(product: ApiProduct){
            this._selectedProduct = product
        },
        selectProductStoredAt(productStorage: ProductStorageMapping){
          this._selectedProductStorage = productStorage
        },
        deselectProduct(){
            this._selectedProduct = undefined
            this._storage = []
            this.deselectProductStoredAt()
        },
        deselectProductStoredAt(){
            this._selectedProductStorage = undefined
        },
        updateProduct(product: ApiProduct){
            this._selectedProduct!.name = product.name
            this._selectedProduct!.starred = product.starred
        },
        deleteProduct(productId: number){
            const product = this._products.find(product => product.id === productId)
            if(!product){
                return
            }
            if(this._selectedProduct?.id === product.id){
                this.deselectProduct()
            }
            this._products = this._products.filter(p => p.id !== product.id)
        },
        deleteProductAt(productStorageId: number, amount: number){
            const storage = this._storage.find(storage => storage.id === productStorageId)
            if(!storage){
                return
            }
            if(this._selectedProduct?.id === storage.productId){
                this._selectedProduct.totalAmount -= amount
            }
            this._storage = this._storage.filter(productStorage => productStorage.id !== productStorageId)

        },
        updateProductAt(productStorageId: number, updated: ProductStorageMapping){
            const storage = this._storage.find(storage => storage.id === productStorageId)
            if(!storage){
                return
            }

            if(this._selectedProduct?.id === storage.productId){
                this._selectedProduct.totalAmount -= storage.amount
                this._selectedProduct.totalAmount += updated.amount
            }
            console.log(storage.amount)
            storage.amount = updated.amount
            storage.storage = undefined
            if(updated.storage){
                storage.storage = {
                    ...updated.storage
                } as ApiStorage
            }
            storage.storageId = updated.storageId
            this._selectedProductStorage = storage
        },
    },
    getters: {
        products: state => state._products,
        size: state => state._products.length,
        productStorage: state => state._storage,
        selectedProduct: state => state._selectedProduct,
        selectedProductStorage: state => state._selectedProductStorage

    }
})