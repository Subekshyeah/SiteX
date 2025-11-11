import { useState } from 'react';
import { VStack, Box } from '@chakra-ui/react';

import NavBar from '../NavBar/NavBar';
import SideBar from '../SideBar/SideBar';

type PageContainerProps = {
    children: React.ReactNode;
};

export type SidebarTypes = {
    isSidebarOpen: boolean;
    setIsSidebarOpen: React.Dispatch<
        React.SetStateAction<SidebarTypes['isSidebarOpen']>
    >;
};

const PageContainer = ({ children }: PageContainerProps) => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    return (
        <VStack
            width='100%'
            height={'100vh'}
            padding={'10px'}
            position={'relative'}
        >
            {isSidebarOpen && (
                <Box
                    className='open-sidebar-overlay'
                    width={'100%'}
                    height={'100%'}
                    backgroundColor={'rgba(20, 20, 20, 0.71)'}
                    position={'absolute'}
                    top={0}
                    left={0}
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    zIndex={5}
                ></Box>
            )}
            <NavBar {...{ isSidebarOpen, setIsSidebarOpen }} />
            <SideBar {...{ isSidebarOpen, setIsSidebarOpen }} />
            <VStack width={'100%'} overflow={'auto'} flex={1}>
                {children}
            </VStack>
        </VStack>
    );
};

export default PageContainer;
