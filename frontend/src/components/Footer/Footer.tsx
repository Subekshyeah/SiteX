import { Link as ReactRouterLink } from 'react-router-dom';
import {
    VStack,
    Box,
    Heading,
    Text,
    HStack,
    Link as ChakraLink,
} from '@chakra-ui/react';
import {
    IconBrandFacebookFilled,
    IconBrandInstagram,
    IconBrandX,
    IconBrandTiktokFilled,
    IconBrandBluesky,
} from '@tabler/icons-react';
const Footer = () => {
    const socialMediaList = [
        {
            icon: <IconBrandFacebookFilled />,
            link: '',
        },
        {
            icon: <IconBrandInstagram />,
            link: '',
        },
        {
            icon: <IconBrandX />,
            link: '',
        },
        {
            icon: <IconBrandTiktokFilled />,
            link: '',
        },
        {
            icon: <IconBrandBluesky />,
            link: '',
        },
    ];
    return (
        <VStack className='footer' width={'100%'} marginTop={'80px'}>
            <Box
                className='divider-line'
                width={'100%'}
                height={'1px'}
                boxShadow={'0px 5px 12px 0px rgba(0, 0, 0, 1)'}
                // border={'2px solid black'}
                bgColor={'black'}
            ></Box>
            <HStack
                className='social-icons-container'
                width={'100%'}
                justifyContent={'center'}
                gap={'20px'}
                marginTop={'20px'}
            >
                {socialMediaList.map((media, index) => {
                    return (
                        <ChakraLink
                            key={index}
                            asChild
                            padding={'8px'}
                            borderRadius={'50%'}
                            bgColor={'black'}
                            color={'white'}
                        >
                            <ReactRouterLink to={media.link}>
                                {media.icon}
                            </ReactRouterLink>
                        </ChakraLink>
                    );
                })}
            </HStack>
            <Heading fontSize={'38px'} marginTop={'20px'}>
                Futmaidan
            </Heading>
            <Text fontSize={'18px'} letterSpacing={'2px'} marginTop={'10px'}>
                Managed by Asymptoads
            </Text>
            <Text fontSize={'14px'} letterSpacing={'1px'} lineHeight={'10px'}>
                Bhaktapur, Nepal
            </Text>
            <HStack>
                <Text
                    fontSize={'14px'}
                    letterSpacing={'1px'}
                    // lineHeight={'2px'}
                >
                    T: +977 9843999851
                </Text>
                <Text
                    fontSize={'14px'}
                    letterSpacing={'1px'}
                    lineHeight={'2px'}
                >
                    E: info@asymptoads.com
                </Text>
            </HStack>
            <Box
                className='copyright-container'
                borderTop={'1px solid black'}
                width={'100%'}
                textAlign={'center'}
                marginTop={'20px'}
                paddingTop={'10px'}
            >
                <Text>&copy; 2025 Asymptoads Nepal</Text>
            </Box>
        </VStack>
    );
};

export default Footer;
