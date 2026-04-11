import MyBibleModule from "./../../../assets/json/MyBible.module.json";
import EBibleModule from "./../../../assets/json/eBible.module.json";


export default [
    ...MyBibleModule as any,
    ...EBibleModule as any
]