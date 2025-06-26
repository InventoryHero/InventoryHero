import type { VTextField, VBtn, VSelect, VNumberInput } from 'vuetify/components'
import type { VDateInput } from 'vuetify/labs/VDateInput'

type VTextFieldProps = InstanceType<typeof VTextField>['$props']
type VBtnProps = InstanceType<typeof VBtn>['$props']
type VSelectProps = InstanceType<typeof VSelect>['$props']
type VNumberInputProps = InstanceType<typeof VNumberInput>['$props']
type VDateInputProps = InstanceType<typeof VDateInput>['$props']

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

    const dateInputStyling = computed<VDateInputProps>(() => {
        return {
            variant: "solo-filled",
            color: "primary",
            clearable: true,
            density: "comfortable",
            hideDetails: "auto"
        }
    })

    const numberInputStyling = computed<VNumberInputProps>(() => {
        return {
            variant: "solo-filled",
            color: "primary",
            clearable: false,
            persistentClear: false,
            hideDetails: "auto",
            disabled: false,
            density: "comfortable"
        }
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
        numberInputStyling,
        btnStyle,
        dateInputStyling
    }
}