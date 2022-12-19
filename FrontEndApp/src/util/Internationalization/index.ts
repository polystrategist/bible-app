import { createI18n } from 'vue-i18n';
import en from './lang/en';
import ja from './lang/ja';
import pt from './lang/pt';

const messages: any = {
    English: en,
    Japanese: ja,
    Portuguese: pt,
};

const internationalizations = createI18n({
    locale: 'English',
    fallbackLocale: 'English',
    allowComposition: true,
    messages,
});

export default internationalizations;
