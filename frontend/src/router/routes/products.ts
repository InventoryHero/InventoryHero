import Products from "@/components/widgets/products/Products.vue";
import ProductView from "@/views/ProductView.vue"
import {i18n} from "@/lang";
import ProductOverlay from "@/components/widgets/products/Product.vue";
import StoredAtDetail from "@/components/widgets/products/ProductStorage.vue";
//import ProductViewWrapper from "@/views/ProductViewWrapper.vue";
//if routing prooves difficult/impossible: use productviewwrapper with supsense and top level await ... (supsense needs suspensible)
export default {
    path: "/products",
    name: "products",
    component: ProductView,
    props: true,
    children:[
        {
            path: '',
            name: "all products",
            component: Products,
        },
        {
            path: 'product/:productId',
            name: "product",
            component: ProductOverlay,
        },
        {
            path: 'product/:productId/detail/:productStorageId',
            name: "product detail",
            component: StoredAtDetail,
        }
    ],
    meta: {
        requiresAuth: true,
        requiresHousehold: true,
        fillHeight: true,
        title: i18n.global.t('titles.products'),
        key: "/products"
    },
}