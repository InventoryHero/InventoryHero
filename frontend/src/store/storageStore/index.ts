import {defineStore} from "pinia";
import {ApiStorage, StorageTypes} from "@/types";

interface StorageMap {
    [key: number]: Array<ApiStorage>; // Maps storageStore type to an array of storages
}

interface SelectedStorageMap {
    [key: number]: ApiStorage | undefined; // Maps storageStore type to a single selected storageStore
}



export default defineStore("storage", {
    state: () => {
        return {
            _storage: {} as StorageMap,
            _selectedStorage: {} as SelectedStorageMap,
            _printSelection: [] as Array<number>,
            _loadingStorage: false,
            _loadingContent: false,
            _fromStorage: undefined as number|undefined
        }
    },
    actions: {
        _storeStorage(storage: Array<ApiStorage>, type: StorageTypes){
            this._storage[type] = storage
        },
        _selectStorage(id: number, type: StorageTypes){
            this._selectedStorage[type] = this._storage[type]?.find(s => s.id === id)
        },
        _deselectStorage(type: StorageTypes){
            this._selectedStorage[type] = undefined
        },
        _updateStorage(updated: ApiStorage, type: StorageTypes) {
            const storage = this._storage[type]?.find(s => s.id === updated.id)
            if(!storage){
                return
            }

            storage.name = updated.name

            if(type === StorageTypes.Box && updated.storageId !== storage.storageId){
                const location = this._storage[StorageTypes.Location]?.find(l => l.id === updated.storageId)
                const oldLocation = this._storage[StorageTypes.Location]?.find(l => l.id === storage.storageId)
                if(location){
                    let currentAmount = location.boxAmount ?? 0
                    location.boxAmount = currentAmount++;
                }
                if(oldLocation){
                    let currentAmount = oldLocation.boxAmount ?? 0
                    oldLocation.boxAmount = currentAmount--;
                }
            }

            storage.storage = updated.storage
            storage.storage = undefined
            if(updated.storage){
                storage.storage = {
                    ...updated.storage
                } as ApiStorage
            }
            storage.storageId = updated.storageId
            if(this._selectedStorage[type]?.id === storage.id){
                //this._selectedBox = undefined
                //this._selectedBox = box
                this._selectStorage(storage.id, type)
            }
        },
        _deleteStorage(id: number, type: StorageTypes){
            const storage = this._storage[type]?.find(s => s.id === id)
            if(!storage){
                return
            }
            if(this._selectedStorage[type]?.id === storage.id){
                //this._selectedBox = undefined
                this._deselectStorage(type)
            }
            this._storage[type] = this._storage[type]?.filter(s => s.id !== storage.id)
        },
        removeProductFromStorage(id: number, type: StorageTypes){
            if(type === undefined){
                return false
            }

            const storage = this._storage[type]?.find(s => s.id === id)
            if(storage){
                storage.productAmount--
                return true
            }
            return false
        },
        _moveProductToStorage(id: number, type: StorageTypes){
            const storage = this._storage[type]?.find(s => s.id === id)
            if(storage){
                storage.productAmount++
                return true
            }
            return false
        },
        _addStorage(storage: ApiStorage, type: StorageTypes){
            if(this._storage[type]){
                this._storage[type]?.push(storage)
            } else{
                this._addStorage(storage, type)
            }
        },


        selectBox(id: number){
            this._selectStorage(id, StorageTypes.Box)
        },
        deselectBox(){
            this._deselectStorage(StorageTypes.Box)
            this._printSelection = []
        },
        storeBoxes(boxes: Array<ApiStorage>){
            this._storeStorage(boxes, StorageTypes.Box)
        },
        updateBox(updatedBox: ApiStorage){
            //const box =
            this._updateStorage(updatedBox, StorageTypes.Box)
        },
        deleteBox(id: number){
            this.removeBoxFromLocation(this._fromStorage ?? -1, id)
            this._deleteStorage(id, StorageTypes.Box)
        },
        moveProduct(oldStorage?: ApiStorage, newStorage?: ApiStorage){
            if(oldStorage){
                this.removeProductFromStorage(oldStorage.id, oldStorage.type)
            }
            if(newStorage){
                this._moveProductToStorage(newStorage.id, newStorage.type)
            }
        },
        removeProductfromBox(id: number){
            this.removeProductFromStorage(id, StorageTypes.Box)
        },
        addBox(newBox: ApiStorage){
          this._addStorage(newBox, StorageTypes.Box)
        },


        storeLocations(locations: Array<ApiStorage>){
            this._storeStorage(locations, StorageTypes.Location)
        },
        selectLocation(location: number){
            this._selectStorage(location, StorageTypes.Location)
        },
        deselectLocation(){
            this._selectedStorage[StorageTypes.Location] = undefined
            this._fromStorage = undefined
        },
        updateLocation(updated: ApiStorage){
            this._updateStorage(updated, StorageTypes.Location)
        },
        deleteLocation(id: number){
            this._deleteStorage(id, StorageTypes.Location)
        },
        removeProductFromLocation(id: number){
            this.removeProductFromStorage(id, StorageTypes.Location)
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        removeBoxFromLocation(locationId: number, boxId: number){
            if(this._selectedStorage[StorageTypes.Location]?.id === locationId){
                this._storage[StorageTypes.Box] = this._storage[StorageTypes.Box].filter(s => s.id !== locationId)
            }
        },
        addLocation(newLocation: ApiStorage){
          this._addStorage(newLocation, StorageTypes.Location)
        },
        getStorage(type: StorageTypes){
            if(type === StorageTypes.Box){
                return this._storage[StorageTypes.Box]
            }
            if(type === StorageTypes.Location){
                return this._storage[StorageTypes.Location]
            }
            return []
        },
        selectForPrinting(id: number, selectAll: boolean = false){
            const item = this._printSelection.findIndex(selection => selection === id)
            if(item === -1){
                this._printSelection.push(id)
            } else if(!selectAll){
                this._printSelection.splice(item, 1);
            }
        },
        deselectAllFromPrinting(){
          this._printSelection = []
        },
        reset() {
            this._storage = {}
            this._selectedStorage = {}
            this._printSelection = []
            this._loadingStorage = false
            this._fromStorage = undefined
        },
        setLoadingStorage(value: boolean){
            this._loadingStorage = value
        },
        setLoadingContent(value: boolean) {
            this._loadingContent = value
        },
        clearPrintSelection(){
            this._printSelection = []
        },
        setFromStorage(id: number){
            this._fromStorage = id
        }

    },
    getters:  {
        boxes: state =>  state._storage[StorageTypes.Box] ?? [],
        selectedBox: state => state._selectedStorage[StorageTypes.Box],
        locations: state =>  state._storage[StorageTypes.Location] ?? [],
        selectedLocation: state => state._selectedStorage[StorageTypes.Location],
        printSelection: state => state._printSelection,
        loadingStorage: state => state._loadingStorage,
        loadingContent: state => state._loadingContent,
        fromStorage: state => state._fromStorage
    }
})