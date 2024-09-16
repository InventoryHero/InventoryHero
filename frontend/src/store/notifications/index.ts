import {defineStore} from "pinia";
import {NotificationsOptions, useNotification} from "@kyvg/vue3-notification";

export default defineStore("notification", {
    state: () => {
        return {
            _notifications: [] as Array<NotificationsOptions>
        }
    },
    actions: {
        addNotification(notification: NotificationsOptions){
            this._notifications.push(notification)
        },
        triggerNotifications(){
            const {notify} = useNotification()
            this._notifications.forEach((notification) => {
                notify(notification)
            })
            this.clear()
        },
        clear(){
            this._notifications = []
        }
    },
    getters: {
    }
})