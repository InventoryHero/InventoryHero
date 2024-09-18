import Boxes from "@/components/widgets/storage/Boxes.vue";
import BoxOverlay from "@/components/widgets/storage/Box.vue";
import ProductStorage from "@/components/widgets/products/ProductStorage.vue";
import {i18n} from "@/lang";
import StorageView from "@/views/StorageView.vue";

export default {
    path: "/boxes",
    name: "boxes",
    component: StorageView,
    props: true,
    children:[
        {
            path: '',
            name: "Boxes",
            component: Boxes,
            meta: {
                title: i18n.global.t('titles.boxes')
            }
        },
        {
            path: 'box/:boxId',
            name: "Box",
            component: BoxOverlay,
            meta: {
                title: i18n.global.t('titles.boxes')
            }
        },
        {
            path: 'box/:boxId/product/:productStorageId',
            name: "Product stored in Box details",
            component: ProductStorage,
            meta: {
                title: i18n.global.t('titles.boxes')
            }
        }
    ],
    meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        key: "/boxes"
    },
}