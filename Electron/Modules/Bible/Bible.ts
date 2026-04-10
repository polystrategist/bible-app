import GetVerses from './Common/GetVerses';
import Search from './Common/Search';
import GetBibleFiles from './Common/GetBibleFiles';
import GetVersesCount from './Common/GetVersesCount';
import DeleteBible from './Common/DeleteBible';

export default () => {
    GetBibleFiles();
    GetVerses();
    Search();
    GetVersesCount();
    DeleteBible();
};
