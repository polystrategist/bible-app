import { app, ipcMain } from "electron";
import { isNightly } from "../../config";
import knex from "knex";

const dataPath =
    app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\StoreDB\\Store.db`;

export default () => {
    ipcMain.handle('getNote', (event, payload) => {
        // ToDo: add method to get the note payload will be the study_space_id
    })

    ipcMain.handle('saveNote', (event, payload) => {
        // ToDo: add method to save the note payload will be the study_space_id
    })
}