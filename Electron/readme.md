The build variant is controlled by environment variables (see `config.ts`), not by editing source.
The `*:rename` yarn scripts set the matching `name` / `productName` / `appId` in `package.json`.

if developing (uses the beta identity, separate userData from prod):

```ts
// process.env.APP_IS_DEV=yes, process.env.APP_IS_BETA=yes
export const isDev = true;
export const isBeta = true;
```

if deploying beta:

```ts
// process.env.APP_IS_BETA=yes
export const isDev = false;
export const isBeta = true;
```

if deploying production:

```ts
export const isDev = false;
export const isBeta = false;
```
