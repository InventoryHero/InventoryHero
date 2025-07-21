
import validator from 'validator';

export default (translationPath: string) =>  {
    const {t} = useI18n()
    const isValidEmailRule = (value: string|null|undefined): boolean | string => {
        if(!value){
            return t(translationPath);
        }
        if (!validator.isEmail(value)) {
            return t(translationPath);
        }
        return true;
    };

    return {
        isValidEmailRule
    };
}
