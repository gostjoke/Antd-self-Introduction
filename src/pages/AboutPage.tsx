import React from 'react';
import { Row, Col, Typography } from 'antd';
const { Title } = Typography;

const AboutPage: React.FC = () => {
    return (
        <React.Fragment>
            <Title level={2}>Skills</Title>
            <p>這是關於頁面的內容</p>   

            <Row gutter={16} style={{ marginTop: 20 }}>
                <Col span={8}>
                </Col>
            </Row>

        </React.Fragment>
    );
};

export default AboutPage;
