import {defineStore} from "pinia";

type ScrollPositions = {
    [key: string]: number,
}


export default defineStore("scroll", {
    state: () => {
        return {
            _positions: {} as ScrollPositions
        }
    },
    actions: {
        pushPosition(route: string, position: number){
            this._positions[route] = position
        },
        popPosition(route: string){
            const position = this._positions[route] || 0
            delete this._positions[route]
            return position
        },
        clear(){
            this._positions = {}
        }
    },
    getters: {
    }
})