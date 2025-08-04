import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { useLocation, Link } from 'react-router-dom';
import {
    HomeOutlined,
    UserOutlined,
    PhoneOutlined,
    FundProjectionScreenOutlined,
} from '@ant-design/icons';

const { Header, Content, Footer } = Layout;

interface AppLayoutProps {
    children?: React.ReactNode;
    breadcrumbItems?: { title: string; href?: string }[];
}

const AppLayout: React.FC<AppLayoutProps> = ({
    children,
    breadcrumbItems = [{ title: 'Home' }],

}) => {
    const {
        token: { colorBgContainer, borderRadiusLG },
    } = theme.useToken();

    const location = useLocation();

    const items = [
        {
            key: '/',
            label: (
                <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                    <HomeOutlined /> Home
                </Link>
            ),
        },
        {
            key: '/about',
            label: (
                <Link to="/about" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                    <UserOutlined /> About
                </Link>
            ),
        },
        {
            key: '/skills',
            label: (
                <Link to="/skills" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                    <FundProjectionScreenOutlined /> Skills
                </Link>
            ),
        },
        {
            key: '/contact',
            label: (
                <Link to="/contact" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                    <PhoneOutlined /> Contact
                </Link>
            ),
        },
    ];

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
                    style={{
                        flex: 1,
                        minWidth: 0,
                        justifyContent: 'flex-end',
                        display: 'flex',
                    }}
                />
            </Header>
            <Content style={{ padding: 0, flex: 1 }}>
                <Breadcrumb
                    style={{ margin: '16px 24px' }}
                    items={breadcrumbItems.map(item => ({
                        title: item.href ? <Link to={item.href}>{item.title}</Link> : item.title,
                    }))}
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
            <Footer style={{ textAlign: 'center' }}>Tien-Wei Hsu created 2025@</Footer>
        </Layout>
    );
};

export default AppLayout;
