import ProductStorage from "@/components/widgets/products/ProductStorage.vue";
import {i18n} from "@/lang";
import StorageView from "@/views/StorageView.vue";
import Locations from "@/components/widgets/storage/Locations.vue";
import Location from "@/components/widgets/storage/Location.vue";
import Box from "@/components/widgets/storage/Box.vue"

export default {
    path: "/locations",
    name: "location",
    component: StorageView,
    props: true,
    children:[
        {
            path: '',
            name: "Locations",
            component: Locations,
            meta: {
                title: i18n.global.t('titles.locations')
            }
        },
        {
            path: 'location/:locationId',
            name: "Location",
            component: Location,
            meta: {
                title: i18n.global.t('titles.locations')
            }
        },
        {
            path: 'location/:locationId/box/:boxId',
            name: "Box stored in location",
            component: Box,
            meta: {
                title: i18n.global.t('titles.locations')
            }
        },
        {
            path: 'location/:locationId/box/:boxId/product/:productStorageId',
            name: "Product stored in Box in location",
            component: ProductStorage,
            meta: {
                title: i18n.global.t('titles.locations')
            }
        },
        {
            path: 'location/:locationId/product/:productStorageId',
            name: "Product stored in location",
            component: ProductStorage,
            meta: {
                title: i18n.global.t('titles.locations')
            }
        }
    ],
    meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        key: "/locations"
    },
}