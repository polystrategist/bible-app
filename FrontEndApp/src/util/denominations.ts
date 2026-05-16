import denominations from '../assets/json/denominations.json';

type Denomination = {
    name: string;
    code: string;
};

const denominationList = denominations as Denomination[];

const legacyDenominationCodes: Record<string, string> = {
    'Assembly of God': 'assemblies_of_god',
    'Christian Missionary Alliance': 'christian_and_missionary_alliance',
    'Christian/Church of Christ': 'churches_of_christ',
    'Congregational': 'congregationalist',
    'Evangelical Free': 'evangelical_free_church',
    'Evangelical/Non-denominational': 'non_denominational',
    'Foursquare': 'foursquare_gospel',
    'Free Methodist': 'methodist',
    'Friends': 'quaker',
    'Independent/Bible': 'bible_church',
    'Orthodox': 'eastern_orthodox',
    'Presbyterian/Reformed': 'presbyterian',
    'Seventh-Day Adventist': 'seventh_day_adventist',
    'United Methodist': 'united_methodist_church',
    'Vineyard': 'vineyard_churches',
    'Others': 'other',
};

export const DENOMINATION_OPTIONS = denominationList.map(({ name, code }) => ({
    label: name,
    value: code,
}));

export function normalizeDenominationCode(value: string | null | undefined): string | null {
    if (!value) return null;

    if (denominationList.some((denomination) => denomination.code === value)) {
        return value;
    }

    const matchedByName = denominationList.find((denomination) => denomination.name === value);
    if (matchedByName) {
        return matchedByName.code;
    }

    return legacyDenominationCodes[value] ?? value;
}
