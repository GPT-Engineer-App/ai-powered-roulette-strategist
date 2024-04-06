import React, { useState } from "react";
import { Box, Heading, Text, VStack, HStack, Button, Input, Image, useToast } from "@chakra-ui/react";
import { FaSpinner } from "react-icons/fa";

const Index = () => {
  const [balance, setBalance] = useState(1000);
  const [betAmount, setBetAmount] = useState(10);
  const [prediction, setPrediction] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const generatePrediction = async () => {
    setIsLoading(true);
    // Simulating API call delay
    await new Promise((resolve) => setTimeout(resolve, 1000));
    const randomNumber = Math.floor(Math.random() * 37);
    setPrediction(randomNumber);
    setIsLoading(false);
  };

  const placeBet = () => {
    if (betAmount > balance) {
      toast({
        title: "Insufficient balance",
        status: "error",
        duration: 2000,
        isClosable: true,
      });
      return;
    }
    setBalance(balance - betAmount);
    generatePrediction();
  };

  return (
    <Box p={8}>
      <VStack spacing={8} align="center">
        <Heading as="h1" size="2xl">
          AI-Powered Roulette Betting Strategist
        </Heading>
        <Image src="https://images.unsplash.com/photo-1592602944193-0848995f4b5a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MDcxMzJ8MHwxfHNlYXJjaHwxfHxyb3VsZXR0ZSUyMHdoZWVsfGVufDB8fHx8MTcxMjM3MzUxM3ww&ixlib=rb-4.0.3&q=80&w=1080" alt="Roulette Wheel" />
        <Text fontSize="xl">Balance: ${balance}</Text>
        <HStack spacing={4}>
          <Input type="number" value={betAmount} onChange={(e) => setBetAmount(parseInt(e.target.value))} placeholder="Bet Amount" />
          <Button colorScheme="blue" onClick={placeBet} disabled={isLoading}>
            {isLoading ? <FaSpinner /> : "Place Bet"}
          </Button>
        </HStack>
        {prediction && (
          <Box>
            <Text fontSize="2xl">AI Prediction: {prediction}</Text>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default Index;
