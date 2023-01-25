import React from 'react';
import axios from 'axios';
const ErrorsTable = ({fetchLabel, id, errors }) => {
  
  const UpdateKey = (id, K, V) => {
    let url = `http://localhost:5000/label/${id}`
    let error_url = url + "/error"
    errors = {}
    errors[K] = V
    
    axios.put(url, errors)
          .then((res) => {
            axios.put(error_url, {"key": K}).then(
              fetchLabel(id)
            ).catch((err) => {
              console.log(err)
            });

          })
          .catch((err) => {
          });
    };

    const errorsKeys = errors.length

    return (
      <div>
        <table>
          <thead>
            <tr>
              <td>Key</td>
              <td>Value</td>
              <td></td>
            </tr>
          </thead>
          <tbody>
           { errorsKeys > 0 ? (
              Object.entries(errors[0]).map(error => {
                return (
                  <tr>
                    <td>{error[0]}</td>
                    <td>{error[1]}</td>
                    <td><button onClick={() => UpdateKey(id, error[0], error[1])}>Replace</button></td>
                  </tr>
                )
              })
           ) : <></>}
          </tbody>
        </table>
      </div>
    );
};
  
export default ErrorsTable;
