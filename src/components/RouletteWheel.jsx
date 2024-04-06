import React from "react";
import { Box } from "@chakra-ui/react";
import "./RouletteWheel.css";

const RouletteWheel = () => {
  return (
    <Box className="roulette-wheel">
      <Box className="wheel">
        <Box className="section section-1 red">
          <span>1</span>
        </Box>
        <Box className="section section-2 black">
          <span>2</span>
        </Box>
        <Box className="section section-3 red">
          <span>3</span>
        </Box>
        <Box className="section section-4 black">
          <span>4</span>
        </Box>
        <Box className="section section-5 red">
          <span>5</span>
        </Box>
        <Box className="section section-6 black">
          <span>6</span>
        </Box>
        <Box className="section section-7 red">
          <span>7</span>
        </Box>
        <Box className="section section-8 black">
          <span>8</span>
        </Box>
        <Box className="section section-9 red">
          <span>9</span>
        </Box>
        <Box className="section section-10 black">
          <span>10</span>
        </Box>
        <Box className="section section-11 red">
          <span>11</span>
        </Box>
        <Box className="section section-12 black">
          <span>12</span>
        </Box>
      </Box>
    </Box>
  );
};

export default RouletteWheel;
