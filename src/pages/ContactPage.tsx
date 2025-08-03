import React from 'react';
import { Button, Space } from 'antd';

const ContactPage: React.FC = () => {
  return (
    <div>
      <h1>聯絡我們</h1>
      <p>這是聯絡頁面的內容</p>
      
      <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
        <div>
          <h3>聯絡方式</h3>
          <p>電話: (02) 1234-5678</p>
          <p>Email: contact@example.com</p>
          <p>地址: 台北市信義區信義路五段7號</p>
        </div>
        
        <div>
          <h3>營業時間</h3>
          <p>週一至週五: 09:00 - 18:00</p>
          <p>週六: 09:00 - 12:00</p>
          <p>週日: 休息</p>
        </div>
        
        <Button type="primary" size="large">
          立即聯絡
        </Button>
      </Space>
    </div>
  );
};

export default ContactPage;
