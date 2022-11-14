if you developing, make sure to change `config.ts`:

```ts
export const isDev = true;
export const isNightly = true;
```

if deploying nightly:

```ts
export const isDev = false;
export const isNightly = true;
```

if deploying production change config to:

```ts
export const isDev = false;
export const isNightly = false;
```
