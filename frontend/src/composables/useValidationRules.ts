import validator from 'validator'

type ValidationOptions = {
  validatePassword: boolean
}

export default (
  password: Ref<string | undefined | null>,
  options: ValidationOptions = { validatePassword: false }
) => {
  const { t } = useI18n()

  const usernameAlreadyInUse = ref<boolean>(false)
  const emailAlreadyInUse = ref<boolean>(false)

  const usernameRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.username.required'),
    (value: string) => value.length >= 3 || t('validation.username.too_short'),
    (value: string) => value.length <= 256 || t('validation.username.too_long'),
    (value: string) =>
      validator.isAlphanumeric(value) ||
      t('validation.username.invalid_characters'),
    (value: string) =>
      !usernameAlreadyInUse.value || t('validation.username.already_in_use')
  ])

  const emailRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.email.required'),
    (value: string) =>
      validator.isEmail(value) || t('validation.email.invalid_email'),
    (value: string) =>
      !emailAlreadyInUse.value || t('validation.email.already_in_use')
  ])

  // TODO PASSWORD VALIDATION
  const passwordRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.password.required'),
    ...(options.validatePassword
      ? [
          (value: string) =>
            validator.isStrongPassword(value || '', {
              minLength: 8,
              minLowercase: 1,
              minUppercase: 1,
              minNumbers: 1,
              minSymbols: 1
            }) || 'weak'
        ]
      : [])
  ])

  const passwordRepeatRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.repeat_password.required'),
    (value: string) =>
      value === password.value ||
      t('validation.repeat_password.password_mismatch')
  ])

  return {
    usernameAlreadyInUse,
    emailAlreadyInUse,

    usernameRules,
    emailRules,
    passwordRules,
    passwordRepeatRules
  }
}
