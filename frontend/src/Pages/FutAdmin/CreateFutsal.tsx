import {
    VStack,
    Box,
    Text,
    Input,
    Heading,
    // FormControl,
    // FormLabel,
    Button,
    Center,
    Field
} from '@chakra-ui/react';
import { useState } from 'react';

const CreateFutsal = () => {
    const [form, setForm] = useState({
        name: '',
        address: '',
        location: '',
        description: '',
        contactNumber: '',
        openingTime: '',
        closingTime: '',
    });
    // const toast = useToast();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await fetch('http://localhost:3000/futsals', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(form),
            });
            if (res.ok) {
                alert('Futsal created successfully!');
                setForm({
                    name: '',
                    address: '',
                    location: '',
                    description: '',
                    contactNumber: '',
                    openingTime: '',
                    closingTime: '',
                });
            } else {
                const data = await res.json();
                alert(data.error || 'Failed to create futsal');
            }
        } catch (err) {
            alert('Network error occurred');
        }
    };

    return (
        <VStack width={'100%'} height={'100vh'} bgColor={'powderblue'}>
            <Box
                padding={'20px'}
                width={'100%'}
                bgColor={'skyblue'}
                textAlign={'center'}
            >
                <Heading fontSize={'42px'}>Create Futsal</Heading>
            </Box>
            <Center flex={1}>
                <VStack bgColor={'white'} padding={'20px'}>
                    <Heading fontSize={'24px'}>Add New Futsal</Heading>
                    <VStack as={'form'} marginTop={'20px'} gap={'20px'} onSubmit={handleSubmit}>
                        {[
                            { label: 'Name', name: 'name', type: 'text' },
                            { label: 'Address', name: 'address', type: 'text' },
                            { label: 'Location', name: 'location', type: 'text' },
                            { label: 'Description', name: 'description', type: 'text' },
                            { label: 'Contact Number', name: 'contactNumber', type: 'text' },
                            { label: 'Opening Time', name: 'openingTime', type: 'text' },
                            { label: 'Closing Time', name: 'closingTime', type: 'text' },
                        ].map((field) => (
                            <Field.Root
                                key={field.name}
                                width={'100%'}
                                display={'flex'}
                                flexDirection={'row'}
                                alignItems={'center'}
                                gap={'20px'}
                            >
                                <Field.Label>
                                    <Text fontWeight={'bolder'} fontSize={'18px'}>
                                        {field.label}:
                                    </Text>
                                </Field.Label>
                                <Input
                                    placeholder={field.label + '...'}
                                    type={field.type}
                                    name={field.name}
                                    value={form[field.name as keyof typeof form]}
                                    onChange={handleChange}
                                    required
                                />
                            </Field.Root>
                        ))}
                        <Button type='submit'>Create</Button>
                    </VStack>
                </VStack>
            </Center>
        </VStack>
    );
};

export default CreateFutsal;