import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header, Content, Footer } = Layout;

const items = [
  { key: '/', label: 'Home' },
  { key: '/about', label: 'About' },
  { key: '/contact', label: 'Contact' },
];

interface AppLayoutProps {
  children?: React.ReactNode;
  breadcrumbItems?: { title: string; href?: string }[];
}

const AppLayout: React.FC<AppLayoutProps> = ({ 
  children, 
  breadcrumbItems = [{ title: 'Home' }] 
}) => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  
  const navigate = useNavigate();
  const location = useLocation();

  const handleMenuClick = (e: { key: string }) => {
    navigate(e.key);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 1,
          width: '100%',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={items}
          onClick={handleMenuClick}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: '0', flex: 1 }}>
        <Breadcrumb
          style={{ margin: '16px 24px' }}
          items={breadcrumbItems}
        />
        <div
          style={{
            padding: 24,
            minHeight: 'calc(100vh - 180px)',
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
            margin: '0 24px 24px 24px',
          }}
        >
          {children || 'Welcome to the main page!'}
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        Tien-Wei Hsu created 2025
      </Footer>
    </Layout>
  );
};

export default AppLayout;
