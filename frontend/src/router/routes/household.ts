import Household from "@/views/Household.vue";
import {i18n} from "@/lang";
import EditHousehold from "@/components/widgets/Households/EditHousehold.vue";
import Households from "@/components/widgets/Households/Households.vue";

export default  {
    path: "/households",
    name: "households",
    component: Household,
    children: [
        {
            path: '',
            name: "all households",
            component: Households,
        },
        {
            path: "edit/:id",
            name: "edit household",
            component: EditHousehold,
            props: true,
        }
    ],
    meta: {
        requiresAuth: true,
        fillHeight: true,
        title: i18n.global.t('titles.households')
    }
}

