import Household from "@/views/Household.vue";
import {i18n} from "@/lang";
import EditHousehold from "@/views/EditHousehold.vue";


export const householdsOverview = {
    path: "/households",
    name: "households",
    component: Household,
    meta: {
        requiresAuth: true,
        fillHeight: true,
        title: i18n.global.t('titles.households')
    }
}

export const editHousehold = {
    path: "/household/edit/:id",
    name: "edit household",
    component: EditHousehold,
    props: true,
    meta: {
        requiresAuth: true,
        fillHeight: true,
        title: i18n.global.t('titles.edit_household')
    }
}