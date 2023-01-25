import React, { useState, useEffect } from 'react';
import {useParams, Link, useNavigate} from 'react-router-dom';
import axios from 'axios';
import JSONbig from 'json-bigint'

const LabelByLabel = () => {
    const [loading, setLoading] = useState(true);
    const [labelData, setLabelData] = useState({});
    const {label} = useParams();
    
    let navigate = useNavigate();

    useEffect(() => {
      setLoading(true);
      fetchLabel(label);
    }, [label]);
  
    const fetchLabel = (label) => {

      let url = `http://localhost:5000/label?label=${label}`
      axios.get(url)
        .then((res) => {
          setLabelData(JSONbig.parse(res.data));
          setLoading(false);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const navigateHome = (label) => {
        
        let url = `http://localhost:5000/label/${label}`
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
                <div className='label'> 
                    <h1>Label {labelData.label}</h1>
                    <div className='item-container'>
                   
                        <div className='label-card' key={labelData.id}>
                        <img src={`http://localhost:5000/image?name=${labelData.image_name}`} alt={label.image_name} />
            
                        <table className='table-card'>
                        <thead>
                            <tr>
                            <td>Text</td>
                            <td>Id</td>
                            <td>Tag Name</td>
                            <td>Accessible</td>
                            <td>Name</td>
                            <td>Class</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{labelData.text}</td>
                            <td>{labelData.e_id}</td>
                            <td>{labelData.tag_name}</td>
                            <td>{labelData.accessible_name}</td>
                            <td>{labelData.name}</td>
                            <td>{labelData.class}</td>
                            </tr>
                        </tbody>
                        
                        </table>
                        <br/>
                        <Link to={`/`}>Home</Link>
                        <br/>
                        <br/>
                        <button onClick={() => navigateHome(labelData.id)}>Delete</button>
                        <br/>
                        <br/>
                        <Link to={`/label/edit/${labelData.id}`}>Edit</Link>
                        <br/>
                        <br/>
                        {/* <h1>Errors</h1>
                        <ErrorsTable fetchLabel={fetchLabel} id={labelData.id} errors={label.errors} /> */}
                  
                    </div>
                    
                </div>
                
                </div>
            )}
        </React.Fragment>
        );
}

export default LabelByLabel;