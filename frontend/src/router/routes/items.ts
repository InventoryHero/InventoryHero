
import {i18n} from "@/lang";
import ItemView from "@/views/items/ItemView.vue";
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import ItemDetailView from "@/views/items/ItemDetailView.vue";

export default [
    {
        path: "/items",
        name: "items",
        component: ItemView,
        props: true,
        meta: {
            requiresAuth: true,
            requiresHousehold: true,
            fillHeight: false,
            title: 'titles.items',
            layout: DefaultLayout,
            layoutProps: {
                showFab: true
            }
        }
    },
    {
        path: '/items/:id', // The ':id' part is the dynamic parameter
        name: 'ItemDetail',  // The name of the route
        component: ItemDetailView,
        props: true,
        meta: {
            layout: DefaultLayout,
            layoutProps: {
                showFab: true
            }
        }
    }
]