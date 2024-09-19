import {defineStore} from "pinia";
import {TabType} from "@/types/TabType.ts";

type ScrollPositions = {
    [key: string]: number,
}

type Filters = {
    [key: string]: string|null
}

type Tabs = {
    [key: string]: TabType
}

export default defineStore("scroll", {
    state: () => {
        return {
            _positions: {} as ScrollPositions,
            _filters: {} as Filters,
            _tabs: {} as Tabs
        }
    },
    actions: {
        pushPosition(route: string, position: number){
            this._positions[route] = position
        },
        pushTab(route: string, tab: TabType){
            this._tabs[route] = tab
        },
        pushFilter(route: string, filter: string|null){
            this._filters[route] = filter
        },
        pushConfig(route: string, position: number, filter: string|null){
            this.pushPosition(route, position)
            this.pushFilter(route, filter)
        },
        popPosition(route: string){
            const position = this._positions[route] || 0
            delete this._positions[route]
            return position
        },
        popFilter(route: string){
            const filter = this._filters[route] || ""
            delete this._filters[route]
            return filter
        },
        popTab(route: string){
            const tab = this._tabs[route] || undefined
            delete this._tabs[route]
            return tab
        },
        pop(route: string){
            const position = this.popPosition(route)
            const filter = this.popFilter(route)
            const tab = this.popTab(route)
            return {
                position,
                tab,
                filter
            }
        },

        clear(){
            this._positions = {}
            this._filters = {}
        }
    },
    getters: {
    }
})