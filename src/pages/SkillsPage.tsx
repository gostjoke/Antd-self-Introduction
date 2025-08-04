import React from 'react';
import { Card, Row, Col, Typography } from 'antd';
const { Title } = Typography;

const SkillsPage: React.FC = () => {
    return (
        <React.Fragment>
            <Title level={2}>Skills</Title>
            <p>這是關於頁面的內容</p>   

            <Row gutter={16} style={{ marginTop: 20 }}>
                <Col span={8}>
                    <Card title="Frontend" bordered={false}>
                        <ul >
                            <li>HTML/CSS/JS</li>
                            <li>React</li>
                            <li>Bootstrap, MUI, ANTD</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Backend" bordered={false}>
                        <ul >
                            <li>Python</li>
                            <li>Golang</li>
                            <li>Bootstrap, MUI, ANTD</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Database" bordered={false}>
                        <ul >
                            <li>MySQL, MSSQL, Postgresql,ORM</li>
                            <li>MongoDB</li>
                            <li>SAP ABAP</li>
                        </ul>
                    </Card>
                </Col>
            </Row>
            <Row gutter={16} style={{ marginTop: 20 }}>
                <Col span={8}>
                    <Card title="Frontend(2023)" bordered={false}>
                        <ul >
                            <li>HTML/CSS/JS</li>
                            <li>React</li>
                            <li>Bootstrap, MUI, ANTD</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Backend(2021)" bordered={false}>
                        <ul >
                            <li>Python</li>
                            <li>Golang</li>
                            <li>Bootstrap, MUI, ANTD</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Database" bordered={false}>
                        誠信、創新、合作、卓越
                    </Card>
                </Col>
            </Row>

        </React.Fragment>
    );
};

export default SkillsPage;
