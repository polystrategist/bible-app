import GetVerses from './Common/GetVerses';
import Search from './Common/Search';
import GetBibleFiles from './Common/GetBibleFiles';

export default () => {
    GetBibleFiles();
    GetVerses();
    Search();
};
