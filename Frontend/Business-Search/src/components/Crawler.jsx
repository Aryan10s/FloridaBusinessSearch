import React, { useState } from "react";
import { Button, Input, message, Space } from "antd";
import CustomLoader from "./CustomLoader";
import axios from "axios";
import Navbar from "./Navbar";

export default function Crawler() {
  const [showCustomLoader, setShowCustomLoader] = useState(false);
  const [text,setText] = useState("")

  const handleCrawling = async () =>{
    setShowCustomLoader(true);
    try{
      const response = await axios.post("http://127.0.0.1:8000/api/initiate-crawling",{"query":text});
      console.log(response)
      message.success("Data Fetched Successfully")
    }catch(error){
      message.error("Business Name not Available");
    }finally{
      setShowCustomLoader(false)
    }
    
  }
  const handleChange =(e) =>{
    setText(e.target.value)
  }


  return (
    <>
      <Navbar title="Florida Secretary of State Business Search" />
      <div style={styles.container}>
        <Space.Compact
          style={{
            width: "50%",
          }}
        >
          <Input addonBefore="Business Name" placeholder="Search Business name here..." value={text} onChange={handleChange} />
          <Button type="primary" onClick={handleCrawling}>Start Crawling!</Button>
        </Space.Compact>
        {showCustomLoader && <CustomLoader />}
      </div>
    </>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "80vh",
  },
  tableContainer: {
    marginTop: "20px",
    display: "flex",
    justifyContent: "center",
  },
};
