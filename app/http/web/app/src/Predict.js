import React, { useState } from 'react';
import axios from 'axios';

const Predict = ({id}) => {

    const [predictScore, setPredictionScore] = useState("");
    const [predictLabel, setPredictionLabel] = useState("");
  
    const fetchPrediction = (id) => {
        let url = `http://localhost:5000/predict/${id}`
        axios.get(url, { transformResponse: function(response) {
            return response;
        }})
        .then((res) => {
            debugger;
            setPredictionScore(JSON.parse(res.data).score);
            setPredictionLabel(JSON.parse(res.data).label);
        })
        .catch((err) => {
            console.log(err);
        });
    };

    return (
        <div>
            <h2>Predict CNN</h2>
            <button onClick={() => fetchPrediction(id)}>Predict</button>
            <br/>
            <br/>
            <table>
                <tr>
                    <th>Score</th>
                    <th>Label</th>
                </tr>
                <tr>
                    <td>{predictScore}</td>
                    <td>{predictLabel}</td>
                </tr>
            </table>
        </div>
    )

}

export default Predict;