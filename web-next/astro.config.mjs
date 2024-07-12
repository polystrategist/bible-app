import { defineConfig } from 'astro/config';
import UnoCSS from 'unocss/astro';
import netlify from '@astrojs/netlify';

// https://astro.build/config
export default defineConfig({
    output: 'server',
    integrations: [
        UnoCSS({
            injectReset: true,
        }),
    ],
    adapter: netlify(),
});
