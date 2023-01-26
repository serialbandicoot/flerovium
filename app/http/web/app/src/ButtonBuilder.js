import React, { useState } from "react";
import axios from 'axios';

const ButtonBuilder = () => {
  const [qty, setQty] = useState("5");
  const [text, setText] = useState("Preview");
  const [sColor, setColor] = useState("#ffffff");
  const [sBackgroundColor, setBackgroundColor] = useState("#e50a14");
  const [sFontSize, setFontSize] = useState("16px");
  const [sBorder, setBorder] = useState("1px solid #e50a14");
  const [sPadding, setPadding] = useState("10px 130px 10px 130px");
  const [sLetterSpacing, setLetterSpacing] = useState("1px");
  const [sMargin, setMargin] = useState("5px");

  const handleSubmit = (evt) => {
    evt.preventDefault();
    let url = `http://localhost:5000/generate`
    axios.put(url, {
        "qty": qty,
        "text": text,
        "color": sColor,
        "background-color": sBackgroundColor,
        "font-size": sFontSize,
        "border": sBorder,
        "padding": sPadding,
        "letter-spacing": sLetterSpacing,
        "margin": sMargin,
        "type": "BUTTON"

    })
    .then((res)=> {
        console.log(res.data)
    })

}

  return (
    <div>
    <form className="small_form" onSubmit={handleSubmit}>
    <label>
        Label:
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </label>
      <label>
        Color:
        <input
          type="text"
          value={sColor}
          onChange={(e) => setColor(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Background Color:
        <input
          type="text"
          value={sBackgroundColor}
          onChange={(e) => setBackgroundColor(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Font Size:
        <input
          type="text"
          value={sFontSize}
          onChange={(e) => setFontSize(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Border:
        <input
          type="text"
          value={sBorder}
          onChange={(e) => setBorder(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Padding:
        <input
          type="text"
          value={sPadding}
          onChange={(e) => setPadding(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Letter Spacing:
        <input
          type="text"
          value={sLetterSpacing}
          onChange={(e) => setLetterSpacing(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Margin:
        <input
          type="text"
          value={sMargin}
          onChange={(e) => setMargin(e.target.value)}
        />
      </label>
      <br />
      <br />
      <label>
        Quantity to generate:
        <input
          type="text"
          value={qty}
          onChange={(e) => setQty(e.target.value)}
        />
      </label>
      <br />
      <br />
      <div className="form-group">
        <input type="submit" value="Generate" />
      </div>
    </form>
        <div className="body">
            <h3>Preview</h3>
            <button style={{ color: sColor, 
                backgroundColor: sBackgroundColor,
                fontSize: sFontSize,
                border: sBorder,
                padding: sPadding,
                letterSpacing: sLetterSpacing,
                margin: sMargin }} type="button">{text}</button>
        </div>
    </div>

  );
};

export default ButtonBuilder;
