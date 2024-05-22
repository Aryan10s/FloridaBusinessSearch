import { message } from "antd";
import { Modal, Descriptions } from "antd";
import { Table } from 'antd';
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
export default function Navbar(props) {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [data, setData] = useState([]);
  const [eventData,setEventdata] = useState(null)
  const [loading, setLoading] = useState(false);
  const [loading1, setLoading1] = useState(false);
  const [isModalOpen1,setIsModalOpen1] = useState(false)
  const handleLogOut = () => {
    navigate("/");
  };


  const fetchdata = async() =>{
    
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/get-business-names');
      console.log(response.data)
      setData(response.data.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }finally{
      setLoading(false);
    }
  }

  const showDocuments = async () => {
    setIsModalOpen(true);
    setLoading(true);
    fetchdata()
   
  };

  const handleOk = () => {
    setIsModalOpen(false);
    setData([])
  };
  const handleCancel = () => {
    setIsModalOpen(false);
    setData([])
  };
  const handleOk1 = () => {
    setIsModalOpen1(false);
    setEventdata(null)
  };
  const handleCancel1 = () => {
    setIsModalOpen1(false);
    setEventdata(null)
  };
  const handleRowClick = async(record) => {
    console.log(record.business_name)
    setIsModalOpen(false);
    setIsModalOpen1(true);
    setLoading1(true)
    setData([])
    try{
      const response = await axios.post("http://127.0.0.1:8000/api/get-data",{"business_name": record.business_name})
      setEventdata(response.data.data[0])
    }catch{
      message.error("Unexpected Business Name.")
    }finally{
      setLoading1(false)
    }
    
  };
  const columns = [
    {
      title: 'Business Names',
      dataIndex: 'business_name',
      key: 'business_name',
    },
  ];
  

  return (
    <div>
      <nav
        className="navbar navbar-expand-lg bg-body-tertiary"
        data-bs-theme="dark"
      >
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            {props.title}
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <a className="nav-link active" aria-current="page" onClick={showDocuments}>
                  Available Business Documents
                </a>
              </li>
            </ul>
            <form className="d-flex" role="search">
              <button
                className="btn btn-outline-success"
                type="submit"
                style={{ marginRight: "1rem" }}
              >
                Clear
              </button>
              <button
                className="btn btn-outline-danger"
                type="submit"
                onClick={handleLogOut}
              >
                Log Out
              </button>
            </form>
          </div>
        </div>
      </nav>
      <Modal
        className="First"
        title="Available Business Documents"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Table 
          dataSource={data} 
          columns={columns} 
          loading={loading}
          onRow={(record) => ({
            onClick: () => handleRowClick(record),
          })}
          rowKey="business_name"
        />
      </Modal>
      <Modal
        title="Document Details"
        open={isModalOpen1}
        onOk={handleOk1}
        onCancel={handleCancel1}
      >
        <Descriptions bordered column={1} loading={loading1}>
          <Descriptions.Item label="Business Name">{eventData?.business_name}</Descriptions.Item>
          <Descriptions.Item label="Document Number">{eventData?.document_number}</Descriptions.Item>
          <Descriptions.Item label="Date of Registration">{eventData?.date_of_registration}</Descriptions.Item>
          <Descriptions.Item label="State of Registration">{eventData?.state_of_registration}</Descriptions.Item>
          <Descriptions.Item label="Available Documents">{eventData?.available_documents}</Descriptions.Item>
          <Descriptions.Item label="Principal Name and Address">
            {eventData?.principal_name_and_address.split('\n').map((line, index) => (
              <div key={index}>{line}</div>
            ))}
          </Descriptions.Item>
        </Descriptions>
      </Modal>
    </div>
  );
}
