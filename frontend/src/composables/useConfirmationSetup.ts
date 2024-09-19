type Callback = () => void

export default (action: Callback) => {
    const confirmationDialog = ref(false)
    const actionConfirmed = ref(false)

    const saveAction = () => {
        if(!confirmationDialog.value) {
            confirmationDialog.value = true
            return
        }

    }

    const reallyDo = () => {
        actionConfirmed.value = true
        confirmationDialog.value = false
        action()
    }

    return {
        confirmationDialog,
        saveAction,
        reallyDo
    }

}