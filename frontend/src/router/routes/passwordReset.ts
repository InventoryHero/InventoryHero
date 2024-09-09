
import {i18n} from "@/lang";
import PasswordReset from "@/views/PasswordReset.vue";


export default {
    path: "/password-reset/:id",
    name: "passwordReset",
    component: PasswordReset,
    props: true,
    meta: {
        requiresAuth: false,
        requiresHousehold: false,
        fillHeight: false,
        title: i18n.global.t('titles.password_reset'),
        tokenized: true
    }
}