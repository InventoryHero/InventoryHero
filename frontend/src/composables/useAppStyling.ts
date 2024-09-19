

export default () => {
    const styling = computed(() => {
        return {
            variant: "solo-filled",
            rounded: "lg",
            color: "primary",
            clearable: true,
            persistentClear: true,
            hideDetails: "auto",
            disabled: false,
            density: "comfortable",
            'class': 'align-center'
        } as Partial<object>
    })


    return {
        styling
    }
}