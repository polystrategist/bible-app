import { createI18n } from 'vue-i18n';
import en from './lang/en';
import ja from './lang/ja';
import pt from './lang/pt';
import es from './lang/es';
import ko from './lang/ko';
import zhCN from './lang/zhCN';
import zhTW from './lang/zhTW';
import fil from './lang/fil';
import fr from './lang/fr';
import de from './lang/de';
import hi from './lang/hi';
import id from './lang/id';
import ar from './lang/ar';

const messages: any = {
    English: en,
    Japanese: ja,
    Portuguese: pt,
    Spanish: es,
    Korean: ko,
    '中文简体': zhCN,
    '中文繁體': zhTW,
    Filipino: fil,
    French: fr,
    German: de,
    Hindi: hi,
    Indonesian: id,
    Arabic: ar,
};

const internationalizations = createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'English',
    fallbackLocale: 'English',
    messages,
});

export default internationalizations;
