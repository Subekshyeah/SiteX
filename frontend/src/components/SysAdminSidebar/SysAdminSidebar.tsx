import { Link as ReactRouterLink } from 'react-router-dom';
import { VStack, Box, Link as ChakraLink } from '@chakra-ui/react';
import { IconX } from '@tabler/icons-react';

import type { SysAdminSidebarTypes } from '../SysAdminPageContainer/SysAdminPageContainer';

const SysAdminSidebar = ({
    isSidebarOpen,
    setIsSidebarOpen,
}: SysAdminSidebarTypes) => {
    const sidebarLinks = [
        {
            name: 'home',
            link: '/sysadmin/',
        },
        {
            name: 'futsal request',
            link: '/sysadmin/futsal-requests',
        },
        {
            name: 'active orders',
            link: '/sysadmin/orders',
        },
        {
            name: 'active refunds',
            link: '/sysadmin/refunds',
        },
        {
            name: 'futsals',
            link: '/sysadmin/futsals',
        },
        {
            name: 'users',
            link: '/sysadmin/users',
        },
    ];

    return (
        <VStack
            position={'absolute'}
            top={0}
            left={isSidebarOpen ? 0 : '-350px'}
            width={'320px'}
            bgColor={'white'}
            height={'100%'}
            alignItems={'flex-start'}
            padding={'20px'}
            transition={'left 0.2s linear'}
            zIndex={10}
        >
            <Box
                className='sidebar-close-btn'
                position={'absolute'}
                top={'20px'}
                right={'20px'}
                cursor={'pointer'}
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            >
                <IconX size={'32px'} />
            </Box>

            <VStack alignItems={'flex-start'} marginTop={'50px'}>
                {sidebarLinks.map((link) => {
                    return (
                        <ChakraLink
                            asChild
                            textTransform={'capitalize'}
                            fontSize={'24px'}
                            key={link.name}
                        >
                            <ReactRouterLink to={link.link}>
                                {link.name}
                            </ReactRouterLink>
                        </ChakraLink>
                    );
                })}
            </VStack>
        </VStack>
    );
};

export default SysAdminSidebar;
