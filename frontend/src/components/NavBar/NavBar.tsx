import { Link as ReactRouterLink } from 'react-router-dom';
import { HStack, Box, Heading, Link as ChakraLink } from '@chakra-ui/react';
import { IconMenu2, IconUserCircle } from '@tabler/icons-react';

import type { SidebarTypes } from '../PageContainer/PageContainer';

const NavBar = ({ isSidebarOpen, setIsSidebarOpen }: SidebarTypes) => {
    return (
        <HStack justifyContent={'space-between'} width={'100%'}>
            <Box
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                cursor={'pointer'}
            >
                <IconMenu2 size={'28px'} />
            </Box>
            <Box className='brand-name-container'>
                <Heading as={'h1'} fontVariant={'heading'}>
                    Futmaidan
                </Heading>
            </Box>
            <ChakraLink asChild>
                <ReactRouterLink to={'/login'}>
                    <IconUserCircle size={'28px'} />
                </ReactRouterLink>
            </ChakraLink>
        </HStack>
    );
};

export default NavBar;
