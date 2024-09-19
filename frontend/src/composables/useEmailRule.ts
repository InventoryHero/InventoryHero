
import validator from 'validator';

export default () =>  {
    const {t} = useI18n()
    const isValidEmailRule = (value: string): boolean | string => {
        if (!validator.isEmail(value)) {
            return t('rules.valid_email');
        }
        return true;
    };

    return {
        isValidEmailRule
    };
}
