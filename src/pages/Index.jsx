import React, { useState } from "react";
import { Box, Heading, Text, VStack, HStack, Button, Input, Image, useToast } from "@chakra-ui/react";
import { FaSpinner } from "react-icons/fa";
import RouletteTable from "../components/RouletteTable";

const Index = () => {
  const [balance, setBalance] = useState(1000);
  const [betAmount, setBetAmount] = useState(10);
  const [prediction, setPrediction] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const generatePrediction = async () => {
    setIsLoading(true);

    await new Promise((resolve) => setTimeout(resolve, 1000));
    const randomNumber = Math.floor(Math.random() * 37);
    setPrediction(randomNumber);
    setIsLoading(false);
  };

  // Additional functions for handling training and playing will be implemented here
  const handleTrain = async () => {
    console.log("Training AI model...");
  };

  const handlePlay = async () => {
    console.log("Playing with AI model...");
  };

  const placeBet = () => {};

  return (
    <Box p={8}>
      <VStack spacing={8} align="center">
        <Heading as="h1" size="2xl">
          AI-Powered Roulette Betting Strategist
        </Heading>
        <HStack spacing={4}>
          <Button colorScheme="green" onClick={generatePrediction} disabled={isLoading}>
            {isLoading ? <FaSpinner /> : "Generate Prediction"}
          </Button>
        </HStack>
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
            <RouletteTable prediction={prediction} />
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default Index;
