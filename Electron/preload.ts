import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("browserWindow", {
    minimizeWindow: () => ipcRenderer.invoke("minimizeWindow"),
    maximizeWindow: () => ipcRenderer.invoke("maximizeWindow"),
    closeWindow: () => ipcRenderer.invoke("closeWindow"),
    isWindowBrowserMaximized: () => ipcRenderer.invoke("isWindowBrowserMaximized"),
    versions: () => ipcRenderer.invoke("versions"),
});
