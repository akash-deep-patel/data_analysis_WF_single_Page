import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [imageUrl2, setImageUrl2] = useState(null);
  const [modelCoef, setmodelCoef] = useState(null);
  const [coefDeter, setcoefDeter] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('http://localhost:5000/api/process-csv', formData);
    setImageUrl(response.data.imageUrl);
    console.log(response.data.imageUrl);
  };

  const handleSubmit2 = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('http://localhost:5000/api/fit_model', formData);
    setImageUrl2(response.data.imageUrl);
    setmodelCoef(response.data.modelCoef);
    setcoefDeter(response.data.coefDeter);
    console.log(response.data.imageUrl);
  };
  return (
    <body>
      <div className='container'>
        <div className="half-page">
          <form onSubmit={handleSubmit}>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <button type="submit">Generate Scatter Plot</button>
          </form>
          {imageUrl && <img src={imageUrl} alt="Scatter_Plot" />}
        </div>

        <div className="half-page">
          <form onSubmit={handleSubmit2}>
            {/* <input type="file" accept=".csv" onChange={handleFileChange} /> */}
            <button type="submit">Generate Scatter Plot with Regression Fit</button>
          </form>
          {imageUrl2 && <img src={imageUrl2} alt="Scatter Model Fit Plot" />}
          
          {modelCoef && <p>Model Coefficient: {modelCoef}</p>}
          {coefDeter && <p>Coefficient of Determination: {coefDeter}</p>}
          {coefDeter && <p>Since 1 is best value for Coefficient of Determination, model is good fit for the data.</p>}
        </div>
      </div>
    </body>

  );
}

export default App;
