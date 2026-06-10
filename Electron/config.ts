import { app } from 'electron';

// In a packaged build the env vars from the build shell are gone at runtime, so we
// cannot rely on APP_IS_BETA to know the variant once installed on a user's machine.
// `beta:rename` stamps a beta name/productName/appId into package.json for every beta
// build (local and CI), so app.getName() reliably carries the 'beta' marker. This is
// what drives autoUpdater.allowPrerelease — without it the beta updater looks for
// beta.yml on the latest *stable* release and 404s. APP_IS_BETA stays as a dev override.
const isBetaBuild = app.getName().toLowerCase().includes('beta');

export const isBeta = process.env.APP_IS_BETA ? true : isBetaBuild;
export const isDev = process.env.APP_IS_DEV ? true : false;
