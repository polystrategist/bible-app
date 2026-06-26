import { test } from 'node:test';
import assert from 'node:assert/strict';
import { milestonesUpTo, nextDueMilestone, REMINDER_MESSAGES } from './reminderMilestones';

const DAY = 86_400_000;

test('milestonesUpTo includes base milestones then +10', () => {
    assert.deepEqual(milestonesUpTo(10), [1, 2, 3, 5, 10]);
    assert.deepEqual(milestonesUpTo(35), [1, 2, 3, 5, 10, 20, 30]);
    assert.deepEqual(milestonesUpTo(0), []);
});

test('nextDueMilestone returns highest crossed milestone above lastFired', () => {
    const now = 100 * DAY;
    assert.equal(nextDueMilestone({ now, lastActive: now - 3.5 * DAY, lastFired: 0 }), 3);
    assert.equal(nextDueMilestone({ now, lastActive: now - 3.5 * DAY, lastFired: 3 }), null);
    assert.equal(nextDueMilestone({ now, lastActive: now - 11 * DAY, lastFired: 5 }), 10);
    assert.equal(nextDueMilestone({ now, lastActive: now - 25 * DAY, lastFired: 10 }), 20);
    assert.equal(nextDueMilestone({ now, lastActive: now - 0.5 * DAY, lastFired: 0 }), null);
});

test('message pool is non-empty with title+body', () => {
    assert.ok(REMINDER_MESSAGES.length >= 10);
    for (const m of REMINDER_MESSAGES) {
        assert.ok(m.title.trim().length > 0);
        assert.ok(m.body.trim().length > 0);
    }
});
