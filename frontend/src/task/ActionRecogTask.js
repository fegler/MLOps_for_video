import * as React from 'react'; 
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';

import axios from 'axios';

export default function ActionRecogBoard() {
  const [file, setFile] = React.useState(null);
  const [resultImg, setResultImg] = React.useState(null);
  const [replayKey, setReplayKey] = React.useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  } 
  const handleUpload = () => {
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://222.122.67.140:5005/detection', formData)
      .then(res => {  
        const imgBase64 = res.data.result_image;    
        if(file.name.split('.')[1] === 'jpg') {
          setResultImg(`data:image/jpeg;base64,${imgBase64}`);
        } else if(file.name.split('.')[1] === 'mp4') {
          const imgBase64 = res.data.result_image;
          setResultImg(`data:image/gif;base64,${imgBase64}`);
          console.log('end video response')
        }
      })
      .catch(err => {
        console.log(err);
      })
  }
  const handleReplay = () => {
    setReplayKey(prevKey => prevKey + 1); // Increment replayKey to force replay
  };

  return (
      <Grid container spacing={2}>
          <Grid item sx={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center'
          }}>
              {"Input File"}
              <Paper
                  sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  height: 500,
                  width: 550
                  }}
              >
                <div>
                  <input type="file" onChange={handleFileChange}/>
                  <Button onClick={handleUpload}>Upload</Button>
                </div>
              </Paper>
            </Grid>

            <Grid item sx={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center'
            }}>
              {"Result Visualize"}
              <Paper sx={{ 
                  p: 2,
                  height: 500,
                  width: 550}}>
                <img 
                  src={resultImg} 
                  key={replayKey}
                  alt="Result" 
                  style={{maxWidth: '100%', height: 'auto'}}
                />
                {file && file.name.split('.')[1] === 'mp4' && (
                  <button onClick={handleReplay}>Replay</button>
                )}
              </Paper>
            </Grid>
          </Grid>
  );
}