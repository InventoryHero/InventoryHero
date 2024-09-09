import {computed, ref} from "vue";

export default () => {
    const editClicked = ref(false)

    const editBtnStyle = computed(() => {
        if(editClicked.value){
            return {
                color: "primary"
            }
        }
        return {
            color: ''
        }
    })


    return {
        editClicked,
        editBtnStyle
    }
}