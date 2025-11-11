import { createSystem, defaultConfig, defineConfig } from '@chakra-ui/react';

const config = defineConfig({
    theme: {
        tokens: {
            colors: {
                themeblack: {
                    value: '#2e2e2e',
                },
            },
            fonts: {
                heading: { value: `"Montserrat", sans-serif` },
                body: { value: `"Roboto", system-ui` },
            },
        },
    },
});

export const system = createSystem(defaultConfig, config);
