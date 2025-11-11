import { Box, VStack, Text } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import { Link as ChakraLink } from '@chakra-ui/react';
import { IconX, IconPick } from '@tabler/icons-react';

import type { SidebarTypes } from '../PageContainer/PageContainer';

const SideBar = ({ isSidebarOpen, setIsSidebarOpen }: SidebarTypes) => {
    const sidebarLinks = [
        {
            name: 'option',
            icon: <IconPick />,
            link: 'option',
        },
        {
            name: 'option',
            icon: <IconPick />,
            link: 'option',
        },
        {
            name: 'option',
            icon: <IconPick />,
            link: 'option',
        },
        {
            name: 'option',
            icon: <IconPick />,
            link: 'option',
        },
        {
            name: 'option',
            icon: <IconPick />,
            link: 'option',
        },
        {
            name: 'option',
            icon: <IconPick />,
            link: 'option',
        },
    ];

    return (
        <VStack
            position={'absolute'}
            top={0}
            left={isSidebarOpen ? '0' : '-330px'}
            width={'325px'}
            height={'100%'}
            bgColor={'white'}
            transition={'left 0.2s linear'}
            padding={'10px'}
            zIndex={10}
        >
            <Box
                className='sidebar-close-btn'
                position={'absolute'}
                top={'10px'}
                right={'10px'}
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                cursor={'pointer'}
            >
                <IconX size={'28px'} />
            </Box>
            <VStack
                className='links-container'
                width={'100%'}
                marginTop={'50px'}
                alignItems={'flex-start'}
                gap={'20px'}
            >
                {sidebarLinks.map((link, index) => {
                    return (
                        <ChakraLink key={index} asChild>
                            <ReactRouterLink to={link.link}>
                                <Text as={'span'}>
                                    <IconPick />
                                </Text>
                                <Text as={'span'}>{link.name}</Text>
                            </ReactRouterLink>
                        </ChakraLink>
                    );
                })}
            </VStack>
        </VStack>
    );
};

export default SideBar;
