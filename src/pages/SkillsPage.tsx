import React from 'react';
import { Card, Row, Col, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const SkillsPage: React.FC = () => {
    const cardStyle = {
        borderRadius: 8,
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    };

    return (
        <>
            <Title level={2} style={{ marginBottom: 8 }}>Skills</Title>
            <Paragraph style={{ fontSize: 16, color: '#555' }}>
                This page showcases my technical skillset including frontend, backend, databases, tools, and analytics.
            </Paragraph>

            <Row gutter={[24, 24]} style={{ marginTop: 20 }}>
                <Col span={8}>
                    <Card title="Frontend" bordered={false} style={cardStyle}>
                        <ul>
                            <li>HTML / CSS / JavaScript</li>
                            <li>React</li>
                            <li>Bootstrap, MUI, Ant Design</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Backend" bordered={false} style={cardStyle}>
                        <ul>
                            <li>Python, Golang</li>
                            <li>Django, Beego, FastAPI</li>
                            <li>RESTful API design</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Databases" bordered={false} style={cardStyle}>
                        <ul>
                            <li>MySQL, PostgreSQL, MSSQL</li>
                            <li>MongoDB</li>
                            <li>SAP ABAP, ORM</li>
                        </ul>
                    </Card>
                </Col>
            </Row>

            <Row gutter={[24, 24]} style={{ marginTop: 20 }}>
                <Col span={8}>
                    <Card title="Version Control & DevOps" bordered={false} style={cardStyle}>
                        <ul>
                            <li>Git, GitHub, GitLab</li>
                            <li>Docker, Podman</li>
                            <li>Basic CI/CD concepts</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="IDE & Tooling" bordered={false} style={cardStyle}>
                        <ul>
                            <li>Visual Studio Code, Azure Data Studio</li>
                            <li>PyCharm, Jupyter Notebook</li>
                            <li>Postman, Git Bash, Copilot</li>
                        </ul>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Analytics & Visualization" bordered={false} style={cardStyle}>
                        <ul>
                            <li>Pandas, NumPy, Seaborn</li>
                            <li>Excel, Tableau</li>
                            <li>Apache ECharts, AntV</li>
                        </ul>
                    </Card>
                </Col>
            </Row>
        </>
    );
};

export default SkillsPage;
