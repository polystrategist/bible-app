import americanStandardVersion1901 from './Modules/Bible/american-standard-version-1901';
import angBiblia1978 from './Modules/Bible/ang-biblia-1978';
import angSalitaNgDios2015 from './Modules/Bible/ang-salita-ng-dios-2015';
import bibliaAveMaria1959 from './Modules/Bible/biblia-ave-maria-1959';
import bibliaDeJoaoFerreiraDeAlmeidaEdicaoDe1819 from './Modules/Bible/biblia-de-joao-ferreira-de-almeida-edicao-de-1819';
import catholicPublicDomainVersion2009 from './Modules/Bible/catholic-public-domain-version-2009';
import englishStandardVersion20012016 from './Modules/Bible/english-standard-version-2001-2016';
import kingJamesBible1611PureCambridgeEdition1900 from './Modules/Bible/king-james-bible-1611-pure-cambridge-edition-1900';
import kingJamesVersion1769 from './Modules/Bible/king-james-version-1769';
import kingJamesVersionOf1611Or1769 from './Modules/Bible/king-james-version-of-1611-or-1769';
import magandangBalitaBiblia from './Modules/Bible/magandang-balita-biblia';
import newAmericanStandardBible from './Modules/Bible/new-american-standard-bible';
import newAmericanStandardVersion2020 from './Modules/Bible/new-american-standard-version-2020';
import newInternationalVersion from './Modules/Bible/new-international-version';
import tamilBible2017 from './Modules/Bible/tamil-bible-2017';
import newAmericanStandardVersion2020Commentaries from './Modules/Commentaries/new-american-standard-version-2020-commentaries';
import newInternationalVersionCommentaries from './Modules/Commentaries/new-international-version.commentaries';

export type MODULE_BIBLE_TYPE = {
    file_name: string;
    language: string;
    language_full: string;
    title: string;
    description: string;
    download_link: string;
    is_zipped?: boolean | undefined | null;
};

export const bible: MODULE_BIBLE_TYPE[] = [
    americanStandardVersion1901,
    angBiblia1978,
    angSalitaNgDios2015,
    bibliaAveMaria1959,
    bibliaDeJoaoFerreiraDeAlmeidaEdicaoDe1819,
    catholicPublicDomainVersion2009,
    englishStandardVersion20012016,
    kingJamesBible1611PureCambridgeEdition1900,
    kingJamesVersion1769,
    kingJamesVersionOf1611Or1769,
    magandangBalitaBiblia,
    newAmericanStandardBible,
    newInternationalVersion,
    newAmericanStandardVersion2020,
    tamilBible2017,
    {
        description: "A heavily annotated version by Roman Catholic scholars, notable for its excellent literary quality. A revision called The New Jerusalem Bible appeared in 1985.",
        download_link: "https://www.ph4.org/_dl.php?back=bbl&a=RSV&b=mybible&c",
        file_name: "Revised Standard Version.SQLite3",
        is_zipped: true,
        language: "en",
        language_full: "english",
        title: "Revised Standard Version"
    }
];

const fileNames = bible.map(entry => entry.file_name).filter(Boolean);
const duplicates = fileNames.filter((name, index, self) => self.indexOf(name) !== index);

if (duplicates.length > 0) {
    throw new Error("Duplicate file_name(s) found: " + [...new Set(duplicates)].join(", "));
}

export const commentaries = [newInternationalVersionCommentaries, newAmericanStandardVersion2020Commentaries];
