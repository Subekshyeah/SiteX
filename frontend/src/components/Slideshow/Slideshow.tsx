import { VStack, HStack, Heading } from '@chakra-ui/react';
import SlideshowCard from '../SlideshowCard/SlideshowCard';

const Slideshow = () => {
    const recommendedCourts = [
        {
            name: 'Hamro Baje ko Futsal',
            location: 'Euta Tole, Jilla',
            rating: 4.6,
            startingPrice: 500,
            coverImg: 'gandhi_futsal.jpg',
        },
        {
            name: 'Hamro Baje ko Futsal',
            location: 'Euta Tole, Jilla',
            rating: 4.6,
            startingPrice: 500,
            coverImg: 'gandhi_futsal.jpg',
        },
        {
            name: 'Hamro Baje ko Futsal',
            location: 'Euta Tole, Jilla',
            rating: 4.6,
            startingPrice: 500,
            coverImg: 'gandhi_futsal.jpg',
        },
        {
            name: 'Hamro Baje ko Futsal',
            location: 'Euta Tole, Jilla',
            rating: 4.6,
            startingPrice: 500,
            coverImg: 'gandhi_futsal.jpg',
        },
        {
            name: 'Hamro Baje ko Futsal',
            location: 'Euta Tole, Jilla',
            rating: 4.6,
            startingPrice: 500,
            coverImg: 'gandhi_futsal.jpg',
        },
        {
            name: 'Hamro Baje ko Futsal',
            location: 'Euta Tole, Jilla',
            rating: 4.6,
            startingPrice: 500,
            coverImg: 'gandhi_futsal.jpg',
        },
    ];
    return (
        <VStack width={'100%'} alignItems={'flex-start'} marginTop={'50px'}>
            {/* <Heading fontWeight={'extrabold'}>Recommended</Heading>
            <HStack overflow={'scroll'} width={'100%'} gap={'20px'}>
                {recommendedCourts.map((court, index) => {
                    return <SlideshowCard {...court} key={index} />;
                })}
            </HStack> */}
        </VStack>
    );
};

export default Slideshow;
