import { VStack, Text, Image } from '@chakra-ui/react';

type SlideshowCardType = {
    name: string;
    location: string;
    rating: number;
    startingPrice: number;
    coverImg: string;
};

const SlideshowCard = ({
    name,
    location,
    rating,
    startingPrice,
    coverImg,
}: SlideshowCardType) => {
    return (
        <VStack width={'250px'} flex={'0 0 auto'} alignItems={'flex-start'}>
            <Text fontWeight={'bold'}>{name}</Text>
            <Text fontStyle={'italic'} lineHeight={'10px'}>
                {location}
            </Text>
            <Image src={coverImg} />
            <Text>{rating}</Text>
            <Text>Rs{startingPrice}</Text>
        </VStack>
    );
};

export default SlideshowCard;
