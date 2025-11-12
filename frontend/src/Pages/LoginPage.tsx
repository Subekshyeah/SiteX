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
            Welcome Back
          </Heading>
          <Text mb={6} color="gray.600" textAlign="center">
            Log in to your account to continue.
          </Text>
          <Button
            variant="outline"
            colorScheme="teal"
            w="100%"
            mb={6}
            // leftIcon={<FcGoogle size={20} />}
          >
            <IconBrandGoogle size={20} style={{ marginRight: 8 }} />
            Continue with Google
          </Button>
          <Text textAlign="center" color="gray.600" mt={4}>
            Don't have an account?{' '}
            <Link href="/register" color="teal.500" fontWeight="medium">
              Sign Up
            </Link>
          </Text>
        </Flex>
      </Flex>
    </PageContainer>
  );
};

export default LoginPage;