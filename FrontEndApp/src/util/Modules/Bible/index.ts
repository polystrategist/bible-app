import americanStandardVersion1901 from "./american-standard-version-1901";
import angBiblia1978 from "./ang-biblia-1978";
import angSalitaNgDios2015 from "./ang-salita-ng-dios-2015";
import bibliaAveMaria1959 from "./biblia-ave-maria-1959";
import bibliaDeJoaoFerreiraDeAlmeidaEdicaoDe1819 from "./biblia-de-joao-ferreira-de-almeida-edicao-de-1819";
import catholicPublicDomainVersion2009 from "./catholic-public-domain-version-2009";
import englishStandardVersion20012016 from "./english-standard-version-2001-2016";
import kingJamesBible1611PureCambridgeEdition1900 from "./king-james-bible-1611-pure-cambridge-edition-1900";
import kingJamesVersion1769 from "./king-james-version-1769";
import kingJamesVersionOf1611Or1769 from "./king-james-version-of-1611-or-1769";
import magandangBalitaBiblia from "./magandang-balita-biblia";
import newAmericanStandardBible from "./new-american-standard-bible";
import newAmericanStandardVersion2020 from "./new-american-standard-version-2020";
import newInternationalVersion from "./new-international-version";
import tamilBible2017 from "./tamil-bible-2017";
import MyBibleModule from "./../../../assets/json/MyBible.module.json";


export default [
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
    },
    ...MyBibleModule as any
]