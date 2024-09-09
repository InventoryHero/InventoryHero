

export default () => {
    const textFieldStyle = computed(() => {
        return {
            variant: "solo-filled",
            rounded: "lg",
            color: "primary",
            clearable: true,
            persistentClear: true,
            hideDetails: "auto",
            class: "mb-4",
            disabled: false
        } as Partial<object>
    })


    return {
        textFieldStyle
    }
}