import React from "react";
import { Card, Space, Col, Row, Typography } from "antd";

const { Meta } = Card;
const { Title, Paragraph } = Typography;

const CardList = [
    {
        title: "TienWei Hsu",
        // description: "www.instagram.com",
        image: "./imgs/mm.jpg",
    },
];

const HomePage: React.FC = () => {
    return (
        <Row gutter={32} align="middle">
            {/* 左側：Card */}
            <Col span={12}>
                <Card
                    hoverable
                    style={{ minWidth: 300, maxWidth: 500 }}
                    cover={<img alt={CardList[0].title} src={CardList[0].image} />}
                >
                    <Meta title={CardList[0].title} />
                </Card>
            </Col>

            {/* 右側：文字介紹 */}
            <Col span={12}>
                <Space direction="vertical" size="middle">
                    <Title style={{ fontSize: 80, margin: 0 }}>Hellow!</Title>
                    <Title style={{ fontSize: 40, margin: 0 }}>My Name is Tien-Wei Hsu</Title>
                    <Paragraph
                        ellipsis={{ rows: 4, expandable: true, symbol: 'more...' }}
                        style={{ fontSize: 24 }}
                    >
                        A little bit about me: I'm a Full Stack Developer currently working at Foxconn Industrial Internet in the Bay Area.
                        I'm passionate about building platforms, scalable systems, and sleek front-ends. I love working with React, Python, and Go.
                        Lately, I've been exploring WebSockets, Kafka, and AI integrations using LangChain in full-stack architectures.
                        I enjoy solving complex problems and am always eager to learn new technologies.
                        One day, I hope to build some of the best systems in the world.
                    </Paragraph>
                </Space>
            </Col>
        </Row>
    );
};

export default HomePage;
