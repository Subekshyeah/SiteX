import { VStack, Heading, Text, Field, Input, Button } from '@chakra-ui/react';

import PageContainer from '../components/PageContainer/PageContainer';
import Slideshow from '../components/Slideshow/Slideshow';
import Footer from '../components/Footer/Footer';

const Home = () => {
    return (
        <PageContainer>
            <VStack paddingTop={'40px'} width={'100%'}>
                {/* <Heading
                    fontWeight={'extrabold'}
                    fontSize={'42px'}
                    lineHeight={'40px'}
                >
                    Find a Futsal Court
                </Heading>
                <Text fontSize={'20px'} marginTop={'5px'}>
                    Search low prices on futsal courts near you and beyond...
                </Text>
                {/* form to search location for nearby futsals */}
                <VStack
                    as={'form'}
                    width={'100%'}
                    marginTop={'30px'}
                    gap={'10px'}
                >
                    {/* <Field.Root width={'100%'}>
                        <Field.Label display={'none'}>Location</Field.Label>
                        <Input placeholder='Search Futsals near a location...' />
                        <Field.ErrorText>Couldn't find area!</Field.ErrorText>
                    </Field.Root>
                    <Button type='submit' width={'100%'}>
                        Search
                    </Button> */}
                </VStack>
                {/* slideshow for top rated, recommended, etc futsals */}
                <Slideshow />
                <Slideshow />
                <Footer />
            </VStack>
        </PageContainer>
    );
};

export default Home;
