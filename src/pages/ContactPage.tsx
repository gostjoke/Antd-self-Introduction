import React from 'react';
import { Space , Typography } from 'antd';
import { GithubOutlined, LinkedinOutlined, MailOutlined } from '@ant-design/icons';


const { Title } = Typography;
const { Paragraph } = Typography; 

const ContactPage: React.FC = () => {
    return (
        <div>
            <Title level={2} style={{display:"flex",flexDirection: 'column', alignItems: 'center'}}>Contact</Title>

            <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
                <div style={{ padding: '20px', border: '1px solid #d9d9d9', borderRadius: '8px', display: 'flex', flexDirection: 'column', alignItems: 'center'  }}>
                    <Paragraph
                        editable
                        copyable
                        ellipsis={{ rows: 2, expandable: true, symbol: 'more...' }}
                        >
                        <MailOutlined /> <a href="mailto:tienweih@uci.edu">tienweih@uci.edu</a>
                    </Paragraph>
                    <Paragraph
                        editable
                        copyable
                        ellipsis={{ rows: 4, expandable: true, symbol: 'more...' }}
                        >
                        <LinkedinOutlined style={{marginRight:10}}/><a href="https://www.linkedin.com/in/tien-wei-h-853598222/" target="_blank">https://www.linkedin.com/in/tien-wei-h-853598222/</a> 
                    </Paragraph>
                    <Paragraph
                        editable
                        copyable
                        ellipsis={{ rows: 4, expandable: true, symbol: 'more...' }}
                        >
                        <GithubOutlined style={{marginRight:10}}/><a href="https://github.com/gostjoke" target="_blank">https://github.com/gostjoke</a>
                    </Paragraph>
                    <Paragraph
                        editable
                        copyable
                        ellipsis={{ rows: 4, expandable: true, symbol: 'more...' }}
                        >
                        <a href="https://leetcode.com/u/gostjoketw/" target="_blank">https://leetcode.com/u/gostjoketw/</a>
                    </Paragraph>
                </div>
            </Space>
        </div>
    );
};



export default ContactPage;
