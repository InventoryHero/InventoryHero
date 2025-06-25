import type { VTextField, VBtn, VSelect } from 'vuetify/components'

type VTextFieldProps = InstanceType<typeof VTextField>['$props']
type VBtnProps = InstanceType<typeof VBtn>['$props']
type VSelectProps = InstanceType<typeof VSelect>['$props']

export default () => {
    const textFieldStyling = computed<VTextFieldProps>(() => {
        return {
            variant: "solo-filled",
            color: "primary",
            clearable: true,
            persistentClear: true,
            hideDetails: "auto",
            disabled: false,
            density: "comfortable",
            'class': 'align-center'
        } as Partial<object>
    })

    const selectStyling = computed<VSelectProps>(() => {
        return {
            variant: "solo-filled",
            color: "primary",
            clearable: true,
            persistentClear: true,
            hideDetails: "auto",
            disabled: false,
            density: "comfortable",
        }
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
        selectStyling,
        btnStyle
    }
}