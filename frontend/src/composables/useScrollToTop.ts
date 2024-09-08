import {ref} from 'vue';
import {templateRef} from "@vueuse/core";

export default (refName: string) => {
    const scroller = templateRef(refName)
    const scrolledDown = ref(false)

    const scrollToTop = () => {
        //@ts-expect-error
        scroller.value.scrollToItem(0)
        scrolledDown.value = false
    }

    const hasScrolled = (viewStartIndex: number, viewEndIndex: number, visibleStartIndex: number, visibleEndIndex: number) => {
        scrolledDown.value = viewStartIndex != 0 || visibleStartIndex != 0;
    }

    return {
        scrolledDown,
        scrollToTop,
        hasScrolled
    }
}