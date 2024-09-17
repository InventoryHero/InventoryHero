import {ref} from 'vue';
import {templateRef} from "@vueuse/core";
import {useScrollPositionStore} from "@/store";

export default (refName: string) => {
    const scroller = templateRef(refName)
    const scrolledDown = ref(false)
    const scrollStore = useScrollPositionStore()

    const scrollToTop = () => {
        //@ts-expect-error vue-virtual-scroller definitely exposes this function
        scroller.value.scrollToItem(0)
        scrolledDown.value = false
    }

    const visible = (path: string, maxPosition: number) => {
        const savedPosition = scrollStore.popPosition(path);
        if(savedPosition){
            //@ts-expect-error vue-virtual-scroller definitely exposes this function
            scroller.value.scrollToItem(Math.min(Math.max(0, savedPosition), maxPosition))
        }
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const hasScrolled = (viewStartIndex: number, viewEndIndex: number, visibleStartIndex: number, visibleEndIndex: number) => {
        scrolledDown.value = viewStartIndex != 0 || visibleStartIndex != 0;
    }

    return {
        scrolledDown,
        scrollToTop,
        hasScrolled,
        visible
    }
}