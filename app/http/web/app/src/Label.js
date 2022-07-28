import React, { useState, useEffect } from 'react';
import {useParams, Link, useNavigate} from 'react-router-dom';
import axios from 'axios';
import JSONbig from 'json-bigint'

const Label = () => {
    const [loading, setLoading] = useState(true);
    const [label, setLabel] = useState({});
    const {id} = useParams();
    let navigate = useNavigate();

    useEffect(() => {
      setLoading(true);
      fetchLabel(id);
    }, [id]);
  
    const fetchLabel = (id) => {

      let url = `http://localhost:5000/label/${id}`
      axios.get(url)
        .then((res) => {
          console.log(JSONbig.parse(res.data));
          setLabel(JSONbig.parse(res.data));
          setLoading(false);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const navigateHome = (id) => {
        
        let url = `http://localhost:5000/label/${id}`
        axios.delete(url)
            .then((res) => {
                console.log('DEL Label');
                navigate("/", { replace: true });
            })
            .catch((err) => {
                console.log(err);
            });
    } 

    return (
        <React.Fragment>
            {loading && <></>}
            {!loading && (
                <div> 
                    <h1>Label {label.label}</h1>
                    <div className='item-container'>
                   
                        <div className='card' key={label.id}>
                        <img src={`http://localhost:5000/image?name=${label.image_label_name}`} alt='' />
            
                        <table>
                        <thead>
                            <tr>
                            <td>Text</td>
                            <td>Id</td>
                            <td>Tag Name</td>
                            <td>Accessible</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{label.text}</td>
                            <td>{label.e_id}</td>
                            <td>{label.tag_name}</td>
                            <td>{label.accessible_name}</td>
                            </tr>
                        </tbody>
                        
                        </table>
                        <br/>
                        <Link to={`/`}>Home</Link>
                        <br/>
                        <br/>
                        <button onClick={() => navigateHome(id)}>Delete</button>
                        <br/>
                        <br/>
                        <Link to={`/label/edit/${id}`}>Edit</Link>
                    </div>
                    
                </div>
                
                </div>
            )}
        </React.Fragment>
        );
}

export default Label;