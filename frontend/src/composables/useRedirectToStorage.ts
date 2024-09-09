import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {StorageTypes} from "@/types";
import {ApiStorage} from "@/types/api.ts";

export default () => {
    const router = useRouter();
    const { t } = useI18n(); // `t` is the translation function from vue-i18n

    const redirect = (storage: ApiStorage | undefined, redirectedFromName: string, redirectedFrom: string = "product") => {
        if (!storage) return;

        switch (storage.type ?? -1) {
            case StorageTypes.Location:
                return router.push(`/storage/locations/${storage.id}/${t(redirectedFrom, { name: redirectedFromName })}`);
            case StorageTypes.Box:
                return router.push(`/storage/boxes/${storage.id}/${t(redirectedFrom, { name: redirectedFromName })}`);
            default:
                return;
        }
    };

    return {
        redirect
    }
}