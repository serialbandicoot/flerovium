
import './App.css';

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Labels from './Labels';
import Label from './Label';
import LabelUpdate from './LabelEdit';
import Logging from './Logging';
import LoggingByRun from './LoggingByRun';
import LabelByLabel from './LabeByLabel';

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Labels/>}/>
          <Route exact path="/label/:id" element={<Label/>}/>
          <Route exact path="/label_by_label/:label" element={<LabelByLabel/>}/>
          <Route exact path="/label/edit/:id" element={<LabelUpdate/>}/>
          <Route exact path="/logging" element={<Logging/>}/>
          <Route exact path="/logging/fl/:id" element={<LoggingByRun/>}/>
        </Routes>
      </BrowserRouter>

  );
}
  
export default App;