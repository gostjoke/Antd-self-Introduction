// App.tsx
import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import AppLayout from './components/AppLayout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import SkillsPage from './pages/SkillsPage';
import PageWrapper from './components/PageWrapper'; 

const App: React.FC = () => {
  const location = useLocation();

  // 鏈接條
  const getBreadcrumbItems = () => {
    switch (location.pathname) {
      case '/':
        return [{ title: 'Home' }];
      case '/about':
        return [{ title: 'Home', href: '/' }, { title: 'About' }];
      case '/skills':
        return [{ title: 'Home', href: '/' }, { title: 'Skills' }];
      case '/contact':
        return [{ title: 'Home', href: '/' }, { title: 'Contact' }];
      default:
        return [{ title: 'Home' }];
    }
  };

  return (
    <AppLayout breadcrumbItems={getBreadcrumbItems()}>
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<PageWrapper><HomePage /></PageWrapper>} />
          <Route path="/about" element={<PageWrapper><AboutPage /></PageWrapper>} />
          <Route path="/skills" element={<PageWrapper><SkillsPage /></PageWrapper>} />
          <Route path="/contact" element={<PageWrapper><ContactPage /></PageWrapper>} />
        </Routes>
      </AnimatePresence>
    </AppLayout>
  );
};

export default App;
