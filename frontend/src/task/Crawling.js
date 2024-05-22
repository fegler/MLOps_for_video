import { React, useState } from "react";
import { Button, TextField, Stack } from "@mui/material";
import Typography from "@mui/material/Typography";

export default function CrawlBox() {
  const [url, setUrl] = useState("");
  const handleSubmit = (event) => {
    event.preventDefault(); // 폼 제출 시 페이지 리로드 방지
    console.log("Submitting URL:", url); // 콘솔에 URL 출력 (테스트용)
    postData();

    // 여기서 서버로 URL을 전송하는 로직을 구현하세요.
    // 예: axios.post('/api/submit-url', { url: url })
  };
  const postData = () => {
    const url =
      process.env.REACT_APP_AIRFLOW_URL +
      "/api/v1/dags/train_neural_network/dagRuns";
    const username = process.env.REACT_APP_AIRFLOW_URL_USERNAME;
    const password = process.env.REACT_APP_AIRFLOW_URL_PASSWORD;

    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Origin", process.env.REACT_APP_BACKEND_URL);

    const base64 = require("base-64");
    headers.append(
      "Authorization",
      "Basic " + base64.encode(username + ":" + password)
    );

    const bodyData = JSON.stringify({
      conf: {
        train_command:
          "CUDA_VISIBLE_DEVICES=7 python /sources/src/ml/train_vmae.py",
      },
    });
    console.log(bodyData);
    fetch(url, {
      method: "POST",
      headers: headers,
      body: bodyData,
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <form onSubmit={handleSubmit} marginTop={2}>
      <Stack spacing={2} direction="row">
        <TextField
          label="Enter URL"
          variant="outlined"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          fullWidth
        />
        <Button type="submit" variant="contained" color="primary">
          Submit URL
        </Button>
      </Stack>
    </form>
  );
}
