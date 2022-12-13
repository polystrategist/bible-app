import { createI18n } from 'vue-i18n';
import en from './lang/en';
import ja from './lang/ja';

const messages: any = {
    English: en,
    Japan: ja,
};

const internationalizations = createI18n({
    locale: 'English',
    fallbackLocale: 'English',
    allowComposition: true,
    messages,
});

export default internationalizations;
