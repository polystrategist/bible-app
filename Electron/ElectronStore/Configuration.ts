import ElectronStore from 'electron-store';

export const appConfig = new ElectronStore({
    name: 'appConfig',
    defaults: {
        setting: {},
    },
    schema: {
        setting: {
            type: 'object',
        },
    },
});
