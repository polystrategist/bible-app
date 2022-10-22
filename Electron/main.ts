import { app, BrowserWindow, BrowserWindowConstructorOptions, screen } from "electron";
import installExtension, { VUEJS_DEVTOOLS } from "electron-devtools-installer";
import path from "path";
import { appConfig } from "./ElectronStore/Configuration";
import IpcMainEvents from "./IpcMainEvents/IpcMainEvents";
const isDev = process.env.IS_DEV == "true" ? true : false;

async function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    const appBounds: any = appConfig.get("setting.appBounds");
    const BrowserWindowOptions: BrowserWindowConstructorOptions = {
        width: 1200,
        height: 750,
        webPreferences: {
            preload: __dirname + "/preload.js",
        },
        show: false,
        alwaysOnTop: true,
        frame: false,
    };

    if (appBounds !== undefined && appBounds !== null) Object.assign(BrowserWindowOptions, appBounds);
    const mainWindow = new BrowserWindow(BrowserWindowOptions);

    // run ipcMain events before loading the window
    IpcMainEvents(mainWindow);

    // and load the index.html of the app.
    // win.loadFile("index.html");
    await mainWindow.loadURL(isDev ? "http://localhost:3000" : `file://${path.join(__dirname, "./index.html")}`);

    if (appBounds !== undefined && appBounds !== null && appBounds.width > width && appBounds.height > height)
        mainWindow.maximize();
    else mainWindow.show();

    // this will turn off always on top after opening the application
    setTimeout(() => {
        mainWindow.setAlwaysOnTop(false);
    }, 1000);

    // Open the DevTools.
    if (isDev) {
        mainWindow.webContents.openDevTools();
    }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    // if dev

    if (isDev) {
        installExtension(VUEJS_DEVTOOLS)
            .then(() => {
                console.log("Added Extension");
            })
            .catch((err) => {
                console.log("Extension Error: ", err);
            });
    }

    createWindow();
    app.on("activate", function () {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
