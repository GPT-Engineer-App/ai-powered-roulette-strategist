import React, { useRef, useEffect } from 'react';
import { Box } from '@chakra-ui/react';

const RouletteTable = ({ prediction }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    const size = 400;
    canvas.width = size;
    canvas.height = size;

    const drawWheel = () => {
     
    };

    const drawSquares = () => {
     
    };

    const animate = () => {
      ctx.clearRect(0, 0, size, size);

     
      drawWheel();
      drawSquares();

      if (prediction) {
       
      }

      requestAnimationFrame(animate);
    };

    animate();
  }, [prediction]);

  return (
    <Box>
      <canvas ref={canvasRef} />
    </Box>
  );
};

export default RouletteTable;