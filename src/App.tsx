import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import AppLayout from './components/AppLayout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';

const App: React.FC = () => {
  const location = useLocation();

  const getBreadcrumbItems = () => {
    switch (location.pathname) {
      case '/':
        return [{ title: 'Home' }];
      case '/about':
        return [{ title: 'Home', href: '/' }, { title: 'About' }];
      case '/contact':
        return [{ title: 'Home', href: '/' }, { title: 'Contact' }];
      default:
        return [{ title: 'Home' }];
    }
  };

  return (
    <AppLayout breadcrumbItems={getBreadcrumbItems()}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </AppLayout>
  );
};

export default App;