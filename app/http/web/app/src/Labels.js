import React, { useState, useEffect } from 'react';
import JSONbig from 'json-bigint';
import {
  Link
} from "react-router-dom";

import axios from 'axios';

const Labels = () => {
  const [labels, setLabels] = useState([]);
  
  useEffect(() => {
    fetchLabels();
  }, []);

  const fetchLabels = () => {
    let url = "http://localhost:5000/labels"
    axios.get(url, { transformResponse: function(response) {
        return response;
      }})
      .then((res) => {
        console.log(JSONbig.parse(res.data));
        setLabels(JSONbig.parse(res.data));
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div>
      <h1>Labels</h1>
      <div className='item-container'>
        {labels.map((label) => (
          <div className='card' key={label.id}>
            <img src={`http://localhost:5000/image?name=${label.image_name}`} alt='' />
  
            <table>
              <thead>
                <tr>
                  <td>Label</td>
                  <td>Text</td>
                  <td>Id</td>
                  <td>Tag Name</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{label.label}</td>
                  <td>{label.text}</td>
                  <td>{label.e_id}</td>
                  <td>{label.tag_name}</td>
                </tr>
              </tbody>
              
            </table>
            <br/>
            <Link to={`/label/${label.id}`}>View</Link>
          </div>
        ))}
      </div>
    </div>
  );
};
export default Labels;