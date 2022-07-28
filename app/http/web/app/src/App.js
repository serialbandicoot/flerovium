
import './App.css';

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Labels from './Labels';
import Label from './Label';
import LabelUpdate from './LabelEdit';

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Labels/>}/>
          <Route exact path="/label/:id" element={<Label/>}/>
          <Route exact path="/label/edit/:id" element={<LabelUpdate/>}/>
          
        </Routes>
      </BrowserRouter>

  );
}
  
export default App;