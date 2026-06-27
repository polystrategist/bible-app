import { ipcMain } from 'electron';
import {
    getReminderEnabled,
    setReminderEnabled,
    getAutoStartEnabled,
    setAutoStartEnabled,
    applyAutoLaunch,
    recordActivity,
} from '../../Reminders/ReminderScheduler';

export default function ReminderEvents() {
    ipcMain.handle('reminders:get-enabled', () => getReminderEnabled());
    ipcMain.handle('reminders:set-enabled', (_e, value: boolean) => {
        setReminderEnabled(value);
        applyAutoLaunch();
        return getReminderEnabled();
    });

    ipcMain.handle('reminders:get-autostart', () => getAutoStartEnabled());
    ipcMain.handle('reminders:set-autostart', (_e, value: boolean) => {
        setAutoStartEnabled(value);
        applyAutoLaunch();
        return getAutoStartEnabled();
    });

    ipcMain.handle('reminders:record-activity', () => {
        recordActivity();
    });
}
