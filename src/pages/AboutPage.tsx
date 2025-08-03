import React from 'react';
import { Card, Row, Col } from 'antd';

const AboutPage: React.FC = () => {
  return (
    <div>
      <h1>關於我們</h1>
      <p>這是關於頁面的內容</p>
      
      <Row gutter={16} style={{ marginTop: 20 }}>
        <Col span={8}>
          <Card title="使命" bordered={false}>
            提供優質的用戶體驗和服務
          </Card>
        </Col>
        <Col span={8}>
          <Card title="願景" bordered={false}>
            成為行業領先的解決方案提供商
          </Card>
        </Col>
        <Col span={8}>
          <Card title="價值觀" bordered={false}>
            誠信、創新、合作、卓越
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AboutPage;
