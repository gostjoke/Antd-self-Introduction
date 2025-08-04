// src/components/PageWrapper.tsx
import { motion } from 'framer-motion';
import React from 'react';

const variants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

const PageWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <motion.div
    variants={variants}
    initial="initial"
    animate="animate"
    exit="exit"
    transition={{ duration: 0.4 }}
  >
    {children}
  </motion.div>
);

export default PageWrapper;
