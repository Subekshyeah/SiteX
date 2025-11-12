import React from "react";
import {
  Flex,
  Heading,
  Text,
  Button,
  Link,
} from "@chakra-ui/react";
import { IconBrandGoogle } from '@tabler/icons-react';
import PageContainer from '../components/PageContainer/PageContainer';

const LoginPage: React.FC = () => {
  return (
    <PageContainer>
      <Flex justify="center" align="center" minH="100vh">
        <Flex
          boxShadow="xl"
          bg="white"
          borderRadius="xl"
          overflow="hidden"
          w={{ base: "100%", md: "500px" }}
          direction="column"
          align="center"
          p={12}
        >
          <Heading fontFamily="Montserrat" mb={2} size="lg">
            Welcome To Our Platform
          </Heading>
          <Text mb={6} color="gray.600" textAlign="center">
            Create your account to continue.
          </Text>
          <Button
            variant="outline"
            colorScheme="teal"
            w="100%"
            mb={6}
          >
            <IconBrandGoogle size={20} style={{ marginRight: 8 }} />
            Sign up with Google
          </Button>
          <Text textAlign="center" color="gray.600" mt={4}>
            Already have an account?{' '}
            <Link href="/login" color="teal.500" fontWeight="medium">
              Log In
            </Link>
          </Text>
        </Flex>
      </Flex>
    </PageContainer>
  );
};

export default LoginPage;