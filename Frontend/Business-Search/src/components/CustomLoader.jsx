import { Typography } from '@mui/material';
import React, { useState, useEffect } from 'react';
import { JellyTriangle } from '@uiball/loaders'

function CustomLoader() {
    const messages = ["Searching about your Business...", "Please wait... We are almost there!", "Don't close this page, we're on it!"];
    const [messageIndex, setMessageIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            if (messageIndex < messages.length - 1) {
                setMessageIndex(messageIndex + 1);
            } else {
                clearInterval(interval);
            }
        }, 20000);

        return () => {
            clearInterval(interval);
        };
    }, [messageIndex]);

    return (
        <div
            style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: "15vh",
                width: "100%",
                flexDirection: "column"
            }}
        >
            <Typography style={{ fontFamily: "inherit", margin: "10px", fontSize: "14px" }}>
                {messages[messageIndex]}
            </Typography>

            <JellyTriangle
                size={18}
                speed={1.75}
                color="#8445F0"
            />
        </div>
    );
}

export default CustomLoader;