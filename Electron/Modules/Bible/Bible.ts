import GetVerses from './Common/GetVerses';
import Search from './Common/Search';
import GetBibleFiles from './Common/GetBibleFiles';
import GetVersesCount from './Common/GetVersesCount';

export default () => {
    GetBibleFiles();
    GetVerses();
    Search();
    GetVersesCount();
};
