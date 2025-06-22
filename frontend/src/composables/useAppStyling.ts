import type { VTextField, VBtn } from 'vuetify/components'

type VTextFieldProps = InstanceType<typeof VTextField>['$props']
type VBtnProps = InstanceType<typeof VBtn>['$props']

export default () => {
    const textFieldStyling = computed<VTextFieldProps>(() => {
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
    const btnStyle = computed<VBtnProps>(() => {
        return {
            color: "primary",
            class: 'text-none',
            density: 'default'
        }
    })



    return {
        textFieldStyling,
        btnStyle
    }
}