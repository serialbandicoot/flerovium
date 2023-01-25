import React, { useState, useEffect } from 'react';
import {useParams, Link, useNavigate} from 'react-router-dom';
import axios from 'axios';
import JSONbig from 'json-bigint'

const LabelUpdate = () => {
    const [loading, setLoading] = useState(true);
    const [label, setLabel] = useState("");
    const [labelValue, setLabelValue] = useState("");
    const [text, setText] = useState("");
    const [eId, setEId] = useState("");
    const [tagName, setTagName] = useState("");
    const [accessibleName, setAccessibleName] = useState("");
    const [className, setClassName] = useState("");
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
          setLabelValue(JSONbig.parse(res.data).label)
          setText(JSONbig.parse(res.data).text);
          setEId(JSONbig.parse(res.data).e_id);
          setTagName(JSONbig.parse(res.data).tag_name);
          setAccessibleName(JSONbig.parse(res.data).accessible_name);
          setClassName(JSONbig.parse(res.data).class);
          setLoading(false);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const handleSubmit = (evt) => {
        evt.preventDefault();
        let url = `http://localhost:5000/label/${id}`
        axios.put(url, {
            "label": labelValue,
            "text": text,
            "e_id": eId,
            "tag_name": tagName,
            "accessible_name": accessibleName,
            "class": className,
        })
        .then((res)=> {
            console.log(res.data)
            navigate(`/label/${id}`, { replace: true });
        })

    }

    return (
        <React.Fragment>
            {loading && <></>}
            {!loading && (
                <div> 
                    <h1>Label Edit {label.label}</h1>
                    <div className='item-container'>
                   
                        <div className='card' key={label.id}>
                        <img src={`http://localhost:5000/image?name=${label.image_name}`} alt='' />
            
                        <form onSubmit={handleSubmit}>
                            <label>
                                Label:
                                <input
                                type="text"
                                value={labelValue}
                                onChange={e => setLabelValue(e.target.value)}
                                />
                            </label>
                            <br/>
                            <br/>
                            <label>
                                Text:
                                <input
                                type="text"
                                value={text}
                                onChange={e => setText(e.target.value)}
                                />
                            </label>
                            <br/>
                            <br/>
                            <label>
                                Tag Name:
                                <input
                                type="text"
                                value={tagName}
                                onChange={e => setTagName(e.target.value)}
                                />
                            </label>
                            <br/>
                            <br/>
                            <label>
                                ID:
                                <input
                                type="text"
                                value={eId}
                                onChange={e => setEId(e.target.value)}
                                />
                            </label>
                            <br/>
                            <br/>
                            <label>
                                Accessible Name:
                                <input
                                type="text"
                                value={accessibleName}
                                onChange={e => setAccessibleName(e.target.value)}
                                />
                            </label>
                            <br/>
                            <br/>
                            <label>
                                Class:
                                <input
                                type="text"
                                value={className}
                                onChange={e => setClassName(e.target.value)}
                                />
                            </label>
                            <br/>
                            <br/>
                            <div className="form-group">
                                <input type="submit" value="Update" />
                            </div>
                        </form>

                        <br/>
                        <Link to={`/`}>Home</Link>
                        <br/>
                        <br/>
                        <Link to={`/label/${id}`}>Back</Link>
           
                    </div>
                    
                </div>
                
                </div>
            )}
        </React.Fragment>
        );
}

export default LabelUpdate;