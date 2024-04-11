const videoInput = document.getElementById("file-input");
const streamingDiv = document.getElementById("stream");

var socket = io();

socket.on("connect", function () {
  console.log("server connected");
});

socket.on("disconnect", function () {
  console.log("server disconnected");
});

socket.on("frame", function (data) {
  const frame_data = data.frame_data;
  const img = document.createElement("img");
  img.src = `data:image/jpeg;base64,${btoa(
    String.fromCharCode(...new Uint8Array(frame_data))
  )}`;
  streamingDiv.appendChild(img);
});

videoInput.addEventListener("change", function (event) {
  console.log("event");
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  reader.onload = () => {
    const videoData = reader.result;
    socket.emit("process_video", videoData);
  };
});

// videoInput.addEventListener("change", async function (event) {
//   const file = event.target.files[0];
//   const formData = new FormData();
//   formData.append("video", file);

//   console.log("change event");
//   const response = await fetch("http://localhost:5000/det_test", {
//     method: "POST",
//     body: formData,
//   });
//   if (!response.ok) {
//     throw new Error(`HTTP error! status: ${response.status}`);
//   }
//   console.log(response.body);
//   const reader = response.body.getReader();

//   const decoder = new TextDecoder("utf-8");
//   let boundary = "";
//   let num = 0;
//   while (true) {
//     console.log(num);
//     num = num + 1;
//     const { done, value } = await reader.read();

//     if (done) {
//       console.log("Stream complete");
//       break;
//     }

//     const chunk = decoder.decode(value, { stream: true });

//     if (!boundary) {
//       const match = chunk.match(/\r\n\r\n--(.*?)\r\n/);
//       if (match) {
//         boundary = match[1];
//         console.log("boundary: ", boundary);
//       }
//     }
//     const frames = chunk.split(boundary);
//     for (const frame of frames) {
//       if (frame.length > 0) {
//         const img = document.createElement("img");
//         img.src = "data:image/jpeg;base64," + frame;
//         streamingDiv.appendChild(img);
//       }
//     }
//   }
// });
