import * as React from 'react'; 
// import Badge from '@mui/material/Badge';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import { ChevronLeft } from '@mui/icons-material';
import Button from '@mui/material/Button';

import axios from 'axios';

import io from 'socket.io-client';

export default function ObjectDetBoard() {
  const [file, setFile] = React.useState(null);
  const [resultImg, setResultImg] = React.useState(null);
  const [isVideo, setIsVideo] = React.useState(false);

  const [socket, setSocket] = React.useState();

  function arrayBufferToBase64(buffer) {
    let binary = '';
    let bytes = new Uint8Array(buffer);
    let len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

  // 최초 페이지 렌더링 시 socket 연결 
  React.useEffect(() => {
    // flask local pc 
    console.log('socket connect start');
    const socketio = io('http://192.168.155.135:5000', {
      withCredentials: true,
      extraHeaders: {
        'Access-Control-Allow-Origin': 'http://localhost:3000'
      }
    });
    setSocket(socketio);
  }, []);

  // socket 연결 시 사용할 이벤트 리스너 등록
  React.useEffect(() => {
    if (socket) {
      socket.on('connect', () => {
        console.log('Socket connected');
      });
      socket.on('disconnect', () => {
        console.log('Socket disconnected');
      });
    
      socket.on('stream_data', (data)=>{
        console.log('stream data socket call');
        // console.log(data.stream_frame);
        const canvas = document.getElementById('streaming');
        const ctx = canvas.getContext('2d');
        // console.log(data.stream_frame.buffer);
        var decoder = new TextDecoder("utf-8");
        const str_data = decoder.decode(new Uint8Array(data.stream_frame));
        // const blob = new Blob([data.stream_frame]);
        // const url = URL.createObjectURL(blob);
        const img = new Image();
        img.onload = () => {
          console.log('image load');
          ctx.drawImage(img, 0, 0);
          // URL.revokeObjectURL(url);
        };
        // img.src = url;
        img.src = 'data:image/jpeg;base64,' + str_data;
      })
    }
  }, [socket]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    console.log('upload file');
    if (socket){
      socket.emit('detection', file);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid
        item
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        {"Input File"}
        <Paper
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            height: 500,
            width: 550,
          }}
        >
          <div>
            <input type="file" onChange={handleFileChange} />
            <Button onClick={handleUpload}>Upload</Button>
          </div>
        </Paper>
      </Grid>

      <Grid
        item
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        {"Result Visualize"}
        <Paper
          sx={{
            p: 2,
            height: 500,
            width: 550,
          }}
        >
          <canvas id="streaming" width="550" height="500"></canvas>
        </Paper>
      </Grid>
    </Grid>
  );
}