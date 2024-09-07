import {defineStore} from "pinia";
import {ApiStorage} from "@/types";

interface StorageMap {
    [key: string]: Array<ApiStorage>; // Maps storageStore type to an array of storages
}

interface SelectedStorageMap {
    [key: string]: ApiStorage | undefined; // Maps storageStore type to a single selected storageStore
}



export default defineStore("storage", {
    state: () => {
        return {
            _storage: {} as StorageMap,
            _selectedStorage: {} as SelectedStorageMap
        }
    },
    actions: {
        _storeStorage(storage: Array<ApiStorage>, type: string){
            this._storage[type] = storage
        },
        _selectStorage(storage: ApiStorage, type: string){
            this._selectedStorage[type] = storage
        },
        _deselectStorage(type: string){
            this._selectedStorage[type] = undefined
        },
        _updateStorage(updated: ApiStorage, type: string) {
            const storage = this._storage[type]?.find(s => s.id === updated.id)
            if(!storage){
                return
            }

            storage.name = updated.name

            if(type === "box" && updated.storageId !== storage.storageId){
                const location = this._storage["location"].find(l => l.id === updated.storageId)
                const oldLocation = this._storage["location"].find(l => l.id === storage.storageId)
                if(location){
                    location.boxAmount++;
                }
                if(oldLocation){
                    oldLocation.boxAmount--;
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
                this._selectStorage(storage, type)
            }
        },
        _deleteStorage(id: number, type: string){
            const storage = this._storage[type].find(s => s.id === id)
            if(!storage){
                return
            }
            if(this._selectedStorage[type]?.id === storage.id){
                //this._selectedBox = undefined
                this._deselectStorage(type)
            }
            this._storage[type] = this._storage[type].filter(s => s.id !== storage.id)
        },
        _removeProductFromStorage(id: number, type: string){
            const storage = this._storage[type].find(s => s.id === id)
            if(storage){
                storage.productAmount--
                return true
            }
            return false
        },
        _moveProductToStorage(id: number, type: string){
            const storage = this._storage[type].find(s => s.id === id)
            if(storage){
                storage.productAmount++
                return true
            }
            return false
        },


        selectBox(box: ApiStorage){
            this._selectStorage(box, "box")
        },
        deselectBox(){
            this._deselectStorage("box")
        },
        storeBoxes(boxes: Array<ApiStorage>){
            this._storeStorage(boxes, 'box')
        },
        updateBox(updatedBox: ApiStorage){
            //const box =
            this._updateStorage(updatedBox, "box")

            console.log(updatedBox)
        },
        deleteBox(id: number){
            this._deleteStorage(id, "box")
        },
        moveProduct(oldStorageId: number|undefined, newStorageId: number|undefined){
            if(!this._removeProductFromStorage(oldStorageId ?? -1, 'box')){
                this._removeProductFromStorage(oldStorageId ?? -1, 'location')
            }
            if(!this._moveProductToStorage(newStorageId, 'box')){
                this._moveProductToStorage(newStorageId, 'location')
            }

        },
        removeProductfromBox(id: number){
            this._removeProductFromStorage(id, "box")
        },


        storeLocations(locations: Array<ApiStorage>){
            this._storeStorage(locations, "location")
        },
        selectLocation(location: ApiStorage){
            this._selectStorage(location, "location")
        },
        deselectLocation(){
            this._selectedStorage["location"] = undefined
        },
        updateLocation(updated: ApiStorage){
            this._updateStorage(updated, "location")
        },
        deleteLocation(id: number){
            this._deleteStorage(id, "location")
        },
        removeProductFromLocation(id: number){
            this._removeProductFromStorage(id, "location")
        },
        removeBoxFromLocation(locationId: number, boxId: number){
            if(this._selectedStorage["location"].id === locationId){
                this._storage["box"] = this._storage["box"].filter(s => s.id !== locationId)
            }
        },


        reset(){
            this._storage = {}
            this._selectedStorage = {}
        }


    },
    getters:  {
        boxes: state =>  state._storage.box ?? [],
        selectedBox: state => state._selectedStorage.box,
        locations: state =>  state._storage.location ?? [],
        selectedLocation: state => state._selectedStorage.location

    }
})