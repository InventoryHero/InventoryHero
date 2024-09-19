import validator from 'validator';
// TODO USE THIS
export default () =>  {
    const {t} = useI18n()

    const passwordOptions = {
        minLength: 8,
        minLowercase: 1,
        minUppercase: 1,
        minNumbers: 1,
        minSymbols: 1,
        returnScore: false,
        pointsPerUnique: 1,
        pointsPerRepeat: 0.5,
        pointsForContainingLower: 10,
        pointsForContainingUpper: 10,
        pointsForContainingNumber: 10,
        pointsForContainingSymbol: 10
    }

    const isStrongPasswordRule = (value: string): boolean | string => {
        if (!validator.isStrongPassword(value, passwordOptions)) {
            return t('rules.strong_password');
        }
        return true;
    };

    return {
        isStrongPasswordRule
    };
}
