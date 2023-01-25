import React, { useState, useEffect } from 'react';
import JSONbig from 'json-bigint';
import axios from 'axios';
import {Link} from 'react-router-dom';
const Logging = () => {
  const [logs, setLogs] = useState([]);
  
  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = () => {
    let url = "http://localhost:5000/logging"
    axios.get(url, { transformResponse: function(response) {
        return response;
      }})
      .then((res) => {
        console.log(JSONbig.parse(res.data));
        setLogs(JSONbig.parse(res.data));
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div>
      <h1>Logs</h1>
      <div className='item-container'>
        
          <div className='label-card'>
           
            <table className='table-card'>
              <thead>
                <tr>
                  <td>Label</td>
                  <td>Method</td>
                  <td>Date</td>
                  <td>Error</td>
                  <td>Element</td>
                  <td>Screenshot</td>
                  <td>fl</td>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (  
                  <tr key={log.id}>
                    <td><Link to={`/label_by_label/${encodeURIComponent(log.label)}`}>{log.label}</Link></td>
                    <td>{log.method}</td>
                    <td>{log.date_time}</td>
                    <td>{log.error}</td>
                    <td><img src={`http://localhost:5000/logging_image?id=${log.id}&element=true`} alt='' onError={(event) => event.target.style.display = 'none'} /></td>
                    <td><img src={`http://localhost:5000/logging_image?id=${log.id}&screnshot=true`} alt='' onError={(event) => event.target.style.display = 'none'} /></td>
                    <td><Link to={`/logging/fl/${log.fl_id}`}>View</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
      </div>
    </div>
  );
};
export default Logging;