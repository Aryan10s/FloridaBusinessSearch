import React from 'react';
import { Form, Input, Button, message } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const LoginForm = (props) => {
  const navigate = useNavigate()
  function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}
const onFinish = async (values) => {
  console.log("Form submitted with values:", values); // Debugging log

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/login", {
      "user_name": values.username,
      "password": values.password
    });

    console.log("API Response:", response); // Debugging log

    if (response.status === 200) {
      message.success("Login Successful");
      navigate("/operations");
    } else {
      message.error("Login Failed!");
    }
  } catch (error) {
    console.error("API call error:", error); // Debugging log
    message.error("Login Failed!");
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Form submission failed:', errorInfo); // Debugging log
  message.error("Login Failed!");
};
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div style={{ padding: '24px', background: '#fff', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)', borderRadius: '8px' }}>
        <h2 style={{ marginBottom: '24px', textAlign: 'center' }}>Welcome to {props.title}!</h2>
        <Form
          name="basic"
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{ maxWidth: 400 }}
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input/>
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            wrapperCol={{ offset: 8, span: 16 }}
          >
            <Button type="primary" htmlType="submit" style={{ width: '100%' }}>
              Submit
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default LoginForm;
