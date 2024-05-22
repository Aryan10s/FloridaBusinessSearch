import React from 'react'
import Box from '@mui/material/Box';
import { Paper, Typography } from '@mui/material';
import MyForm from './MyForm';



export default function Login() {
  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <Box style={{ flex: 1 }}>
        <img
          src="/assets/Images/loginPage.png"
          alt="Login Page"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Box>
      <Box
        style={{
          flex: 1,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}
      >
        <MyForm title = "Florida Business Search"/>
      </Box>
    </div>
  )
}
