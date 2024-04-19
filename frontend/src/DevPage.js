import React from "react";

export default function DevPage() {
  const navigateToAirflow = () => {
    window.location.href = process.env.REACT_APP_AIRFLOW_URL;
  };

  const navigateToMlflow = () => {
    window.location.href = process.env.REACT_APP_MLFLOW_URL;
  };

  const navigateToLabelStudio = () => {
    window.location.href = process.env.REACT_APP_LABELSTUDIO_URL;
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

    // Basic Authentication을 위한 처리
    // 비밀번호가 있다면 "username:password" 형태로 인코딩해야합니다.
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
    <div>
      <button onClick={navigateToAirflow}>Training Schedules</button>
      <button onClick={navigateToMlflow}>Experiment Logs</button>
      <button onClick={navigateToLabelStudio}>Label Studio Page</button>
      <button onClick={postData}>Train script start</button>
    </div>
  );
}
