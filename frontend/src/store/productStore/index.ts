import {defineStore} from "pinia";
import {ApiProduct, ApiStorage, ProductStorageMapping} from "@/types/api.ts";
import {useStorage} from "@/store";

export default defineStore("products", {
    state: () => {
        return {
            _products: [] as Array<ApiProduct>,
            _storage: [] as Array<ProductStorageMapping>,
            _selectedProduct: undefined as ApiProduct | undefined,
            _selectedProductStorage: undefined as ProductStorageMapping | undefined,
            _fromStorage: undefined as number|undefined,
            _loadingProducts: false,
            _loadingProductStorage: false
        }
    },
    actions: {
        storeProducts(products: Array<ApiProduct>){
            this._products = [...products]
        },
        storeProductStorage(storage: Array<ProductStorageMapping>){
            this._storage = [...storage]
        },
        selectProduct(id: number){
            this._selectedProduct = this._products.find(p => p.id === id)
        },
        selectProductStoredAt(id: number){
          this._selectedProductStorage = this._storage.find(p => p.id === id)
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

            if(this._fromStorage !== undefined && this._fromStorage === storage.storage?.id){

                const storageStore = useStorage()

                storageStore.removeProductfromBox(storage.storage.id)
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
            storage.amount = updated.amount

            if(storage.storage?.id !== updated.storage?.id && this._fromStorage !== undefined){
                const storageStore = useStorage()
                storageStore.moveProduct(storage.storage?.id, updated.storage?.id)
                this._products = this._products.filter(p => p.id !== storage.productId)
            }

            storage.storage = undefined
            if(updated.storage){
                storage.storage = {
                    ...updated.storage
                } as ApiStorage
            }


            this._selectedProductStorage = storage
        },
        setStorage(id: number){
            this._fromStorage = id
        },
        updateStarred(id: number){
          const product = this._products.find(p => p.id === id)
          if(product){
              product.starred = !product.starred
          }
        },
        addProduct(product: ApiProduct){
            this._products.push(product)
        },
        setLoadingProducts(value: boolean){
            this._loadingProducts = value
        },
        setLoadingProductStorage(value: boolean){
            this._loadingProductStorage = value
        },
        reset(){
            this._products = []
            this._selectedProduct = undefined
            this._fromStorage = undefined
            this._selectedProductStorage = undefined
            this._storage = []
            this._loadingProducts = false
            this._loadingProductStorage = false
        }
    },
    getters: {
        products: state => state._products,
        size: state => state._products.length,
        productStorage: state => state._storage,
        selectedProduct: state => state._selectedProduct,
        selectedProductStorage: state => state._selectedProductStorage,
        calledFromStorage: state => state._fromStorage !== undefined,
        storedAt: state => state._fromStorage,
        loadingProducts: state => state._loadingProducts,
        loadingProductStorage: state => state._loadingProductStorage
    }
})