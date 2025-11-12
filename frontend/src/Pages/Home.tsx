import { VStack, Heading, Text, Field, Input, Button } from '@chakra-ui/react';

import PageContainer from '../components/PageContainer/PageContainer';
import Slideshow from '../components/Slideshow/Slideshow';
import Footer from '../components/Footer/Footer';
import MapComponent from './MapComponent';


const Home = () => {
    return (
        <PageContainer>
            <MapComponent />
        </PageContainer>
    );
};

export default Home;
