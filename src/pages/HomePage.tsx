import React from 'react';
import { Card, Col, Divider, Row } from 'antd';

const { Meta } = Card;

const CardList =[
    {
        title: 'Europe Street beat',
        description: 'www.instagram.com',
        image: 'https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png',
    }
    ,
    {
        title: 'Europe Street beat',
        description: 'www.instagram.com',
        image: 'https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png',
    }
    ,
    {
        title: 'Europe Street beat',
        description: 'www.instagram.com',
        image: 'https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png',
    }
]


const HomePage: React.FC = () => {
  return (
    <div>
      <h1>歡迎來到首頁</h1>
      <Row gutter={16}>
        {CardList.map((card, index) => (
            <Col className="gutter-row" span={8}>
                <Card
                    key={index}
                    hoverable
                    style={{ width: 440, marginBottom: 20 }}
                    cover={<img alt={card.title} src={card.image} />}
                >
                    <Meta title={card.title} description={card.description} />
                </Card>
            </Col>
        ))}
      </Row>
    </div>
  );
};

export default HomePage;
