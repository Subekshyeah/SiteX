import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ChakraProvider } from '@chakra-ui/react';
import { system } from './CustomTheme';

import './style.css';

import App from './App';

createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter>
            <ChakraProvider value={system}>
                <App />
            </ChakraProvider>
        </BrowserRouter>
    </React.StrictMode>
);
