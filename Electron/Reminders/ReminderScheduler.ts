import Log from 'electron-log';
import { Notification } from 'electron';
import { appConfig } from '../ElectronStore/Configuration';
import { setAutoLaunch } from '../util/autoLaunch';
import { nextDueMilestone, pickReminderMessage, FIRE_HOUR } from './reminderMilestones';

const CHECK_INTERVAL_MS = 30 * 60 * 1000; // 30 minutes
let timer: NodeJS.Timeout | null = null;

export function getReminderEnabled(): boolean {
    return appConfig.get('setting.reminders.enabled', true) as boolean;
}

export function setReminderEnabled(v: boolean): void {
    appConfig.set('setting.reminders.enabled', v);
    if (v) recordActivity();
}

/** Whether the app starts hidden at login so reminders survive a reboot. */
export function getAutoStartEnabled(): boolean {
    return appConfig.get('setting.reminders.autoStart', true) as boolean;
}

export function setAutoStartEnabled(v: boolean): void {
    appConfig.set('setting.reminders.autoStart', v);
}

/**
 * Register the OS login item iff reminders AND auto-start are both on. Auto-start
 * is pointless without reminders, so the two are AND-ed into one effective state.
 */
export function applyAutoLaunch(): void {
    setAutoLaunch(getReminderEnabled() && getAutoStartEnabled());
}

/** Re-anchor inactivity to "now" and clear the fired marker (the reset). */
export function recordActivity(): void {
    appConfig.set('setting.reminders.lastActiveAt', Date.now());
    appConfig.set('setting.reminders.lastFiredMilestone', 0);
}

export function checkAndFire(now: number = Date.now()): void {
    if (!getReminderEnabled()) return;
    if (!Notification.isSupported()) return;

    const lastActive = appConfig.get('setting.reminders.lastActiveAt', now) as number;
    const lastFired = appConfig.get('setting.reminders.lastFiredMilestone', 0) as number;

    const due = nextDueMilestone({ now, lastActive, lastFired });
    if (due === null) return;

    // Avoid dead-of-night nudges: only fire from FIRE_HOUR onward (local).
    if (new Date(now).getHours() < FIRE_HOUR) return;

    const msg = pickReminderMessage();
    try {
        new Notification({ title: msg.title, body: msg.body }).show();
        appConfig.set('setting.reminders.lastFiredMilestone', due);
        Log.info(`[Reminders] fired milestone ${due}`);
    } catch (e) {
        Log.warn('[Reminders] failed to show notification:', e);
    }
}

export function startReminderScheduler(): void {
    if (timer) return;
    timer = setInterval(() => checkAndFire(), CHECK_INTERVAL_MS);
    checkAndFire();
}

export function stopReminderScheduler(): void {
    if (timer) {
        clearInterval(timer);
        timer = null;
    }
}
