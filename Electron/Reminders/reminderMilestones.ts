export const BASE_MILESTONES = [1, 2, 3, 5, 10];
export const REPEAT_EVERY_DAYS = 10;
export const FIRE_HOUR = 9;

const DAY_MS = 86_400_000;

/** All milestone day-counts up to and including maxDays. */
export function milestonesUpTo(maxDays: number): number[] {
    const out: number[] = [];
    for (const m of BASE_MILESTONES) {
        if (m <= maxDays) out.push(m);
    }
    let next = BASE_MILESTONES[BASE_MILESTONES.length - 1] + REPEAT_EVERY_DAYS;
    while (next <= maxDays) {
        out.push(next);
        next += REPEAT_EVERY_DAYS;
    }
    return out;
}

/**
 * The highest milestone (in days) crossed since `lastActive` that is greater
 * than `lastFired`, or null if none. Returning only the highest means a long
 * absence produces a single nudge rather than a backlog.
 */
export function nextDueMilestone(args: {
    now: number;
    lastActive: number;
    lastFired: number;
}): number | null {
    const elapsedDays = Math.floor((args.now - args.lastActive) / DAY_MS);
    if (elapsedDays < 1) return null;
    const crossed = milestonesUpTo(elapsedDays).filter((m) => m > args.lastFired);
    if (crossed.length === 0) return null;
    return crossed[crossed.length - 1];
}

export const REMINDER_MESSAGES: { title: string; body: string }[] = [
    { title: 'A moment with God', body: 'Take a quiet moment with God today 🙏' },
    { title: 'Your prayer list', body: 'Your prayer list is waiting for you.' },
    { title: 'Just a few verses', body: 'A few verses can reset your whole day.' },
    { title: 'Pause and breathe', body: 'Pause and breathe — His Word is here for you.' },
    { title: 'Someone needs prayer', body: 'Someone on your prayer list could use a prayer today.' },
    { title: "Today's devotion", body: "Today's devotion is ready when you are." },
    { title: 'Find some peace', body: 'Even five minutes in Scripture brings peace.' },
    { title: 'Pick up where you left off', body: 'Come back and continue your reading.' },
    { title: 'He is near', body: 'Draw near to God, and He will draw near to you.' },
    { title: 'A word for today', body: 'Let a verse speak to your heart this morning.' },
    { title: 'Rest your soul', body: 'Come to Him and find rest for your soul.' },
    { title: 'Stay rooted', body: 'A daily moment in the Word keeps you grounded.' },
];

export function pickReminderMessage(rand: () => number = Math.random) {
    return REMINDER_MESSAGES[Math.floor(rand() * REMINDER_MESSAGES.length)];
}
