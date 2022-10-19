import { app, BrowserWindow, BrowserWindowConstructorOptions } from "electron";
import installExtension, { VUEJS_DEVTOOLS } from "electron-devtools-installer";
import path from "path";
const isDev = process.env.IS_DEV == "true" ? true : false;

async function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: __dirname + "/preload.js",
        },
        show: false,
        alwaysOnTop: true,
    } as BrowserWindowConstructorOptions);

    // and load the index.html of the app.
    // win.loadFile("index.html");
    await mainWindow.loadURL(isDev ? "http://localhost:3000" : `file://${path.join(__dirname, "./index.html")}`);
    mainWindow.show();

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
