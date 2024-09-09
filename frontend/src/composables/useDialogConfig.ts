import { ref } from 'vue'

export default function useDialogConfig() {
    // Visibility state of the dialog
    const isVisible = ref(false)

    // Function to open the dialog
    const openDialog = () => {
        isVisible.value = true
    }

    // Function to close the dialog
    const closeDialog = () => {
        isVisible.value = false
    }

    return {
        isVisible,
        openDialog,
        closeDialog,
        dialogProps: {
            contained: true,
            contentClass: 'detail-dialog pa-0 ma-0',
            persistent: true,
            noClickAnimation: true,
            scrim: false,
            fullscreen: true,
            transition: "dialog-bottom-transition"
        },
    }
}
