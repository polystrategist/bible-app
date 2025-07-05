// uno.config.ts
import { defineConfig, transformerDirectives } from 'unocss';

export default defineConfig({
    // ...UnoCSS options
    transformers:[
        transformerDirectives()
    ]
});
