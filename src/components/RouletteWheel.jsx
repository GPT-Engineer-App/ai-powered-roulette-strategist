import React from "react";
import { Box } from "@chakra-ui/react";

const RouletteWheel = () => {
  return (
    <Box className="roulette-wheel">
      <Box className="wheel">
        <Box className="section red">
          <span>1</span>
        </Box>
        <Box className="section black">
          <span>2</span>
        </Box>
        <Box className="section red">
          <span>3</span>
        </Box>
        <Box className="section black">
          <span>4</span>
        </Box>
        <Box className="section red">
          <span>5</span>
        </Box>
        <Box className="section black">
          <span>6</span>
        </Box>
        <Box className="section red">
          <span>7</span>
        </Box>
        <Box className="section black">
          <span>8</span>
        </Box>
        <Box className="section red">
          <span>9</span>
        </Box>
        <Box className="section black">
          <span>10</span>
        </Box>
        <Box className="section red">
          <span>11</span>
        </Box>
        <Box className="section black">
          <span>12</span>
        </Box>
      </Box>
    </Box>
  );
};

export default RouletteWheel;
