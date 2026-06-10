/** Accent color + lucide icon name for a prayer's group/category. */
export interface GroupStyle {
    color: string;
    icon: string;
}

const KNOWN: Record<string, GroupStyle> = {
    family: { color: '#3B82F6', icon: 'lucide:users' },
    health: { color: '#16A34A', icon: 'lucide:heart-pulse' },
    work: { color: '#F59E0B', icon: 'lucide:briefcase' },
    finance: { color: '#0EA5E9', icon: 'lucide:piggy-bank' },
    church: { color: '#8B5CF6', icon: 'lucide:church' },
    ministry: { color: '#8B5CF6', icon: 'lucide:hand-heart' },
    school: { color: '#6366F1', icon: 'lucide:graduation-cap' },
    friends: { color: '#EC4899', icon: 'lucide:users-round' },
    guidance: { color: '#14B8A6', icon: 'lucide:compass' },
    thanksgiving: { color: '#EAB308', icon: 'lucide:party-popper' },
    marriage: { color: '#E11D48', icon: 'lucide:heart' },
    children: { color: '#F97316', icon: 'lucide:baby' },
    healing: { color: '#16A34A', icon: 'lucide:cross' },
    salvation: { color: '#EAB308', icon: 'lucide:sparkles' },
    protection: { color: '#64748B', icon: 'lucide:shield' },
    provision: { color: '#0EA5E9', icon: 'lucide:gift' },
    wisdom: { color: '#8B5CF6', icon: 'lucide:lightbulb' },
};

/**
 * Selectable preset categories offered in the group picker. Stored verbatim
 * (Title Case); `groupStyle` lower-cases for the lookup. Kept in sync with the
 * mobile `PrayerGroupStyle.predefined`.
 */
export const PREDEFINED_GROUPS: string[] = [
    'Family',
    'Health',
    'Finance',
    'Work',
    'Church',
    'Ministry',
    'Friends',
    'School',
    'Marriage',
    'Children',
    'Healing',
    'Guidance',
    'Salvation',
    'Protection',
    'Provision',
    'Thanksgiving',
    'Wisdom',
];

const PALETTE = ['#3B82F6', '#16A34A', '#F59E0B', '#8B5CF6', '#EC4899', '#14B8A6', '#0EA5E9', '#6366F1'];

function hash(s: string): number {
    let h = 0;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
    return Math.abs(h);
}

export function groupStyle(group?: string | null): GroupStyle {
    const key = (group ?? '').trim().toLowerCase();
    if (!key) return { color: '#3B82F6', icon: 'lucide:hand-heart' };
    if (KNOWN[key]) return KNOWN[key];
    return { color: PALETTE[hash(key) % PALETTE.length], icon: 'lucide:flower-2' };
}

/** "Added today" / "2 days ago" from an ISO8601 created_at string. */
export function relativeTime(iso?: string): string {
    if (!iso) return '';
    const created = new Date(iso);
    if (Number.isNaN(created.getTime())) return '';
    const today = new Date();
    const a = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const b = new Date(created.getFullYear(), created.getMonth(), created.getDate());
    const diff = Math.round((a.getTime() - b.getTime()) / 86400000);
    if (diff <= 0) return 'Added today';
    if (diff === 1) return 'Yesterday';
    if (diff < 7) return `${diff} days ago`;
    if (diff < 14) return 'Last week';
    if (diff < 30) return `${Math.floor(diff / 7)} weeks ago`;
    if (diff < 365) return `${Math.floor(diff / 30)} months ago`;
    return `${Math.floor(diff / 365)} years ago`;
}
