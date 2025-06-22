
import {i18n} from "@/lang";
import BoxesView from "@/views/storage/boxes/BoxesView.vue";
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import ItemDetailView from "@/views/items/ItemDetailView.vue";
import BoxContentView from "@/views/storage/boxes/BoxContentView.vue";
import RoomsView from "@/views/storage/rooms/RoomsView.vue";
import RoomContentView from "@/views/storage/rooms/RoomContentView.vue";

export default [
    {
        path: "/boxes",
        name: "Boxes",
        component: BoxesView,
        props: true,
        meta: {
            requiresAuth: true,
            requiresHousehold: true,
            fillHeight: false,
            title: 'titles.boxes',
            layout: DefaultLayout,
            layoutProps: {
                showFab: true
            }
        }
    },
    {
        path: '/box/:id', // The ':id' part is the dynamic parameter
        name: 'BoxContentView',  // The name of the route
        component: BoxContentView,
        props: true,
        meta: {
            layout: DefaultLayout,
            layoutProps: {
                showFab: true
            }
        }
    },
    /**ROOMS**/
    {
        path: "/rooms",
        name: "Rooms",
        component: RoomsView,
        props: true,
        meta: {
            requiresAuth: true,
            requiresHousehold: true,
            fillHeight: false,
            title: 'titles.rooms',
            layout: DefaultLayout,
            layoutProps: {
                showFab: true
            }
        }
    },
    {
        path: '/room/:id', // The ':id' part is the dynamic parameter
        name: 'RoomContentView',  // The name of the route
        component: RoomContentView,
        props: true,
        meta: {
            layout: DefaultLayout,
            layoutProps: {
                showFab: true
            }
        }
    },
]