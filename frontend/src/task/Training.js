import { React, useState } from "react";
import { Button, TextField, Stack } from "@mui/material";
import Typography from "@mui/material/Typography";

export default function TrainBox() {
  const argument_names = [
    "config",
    "model_path",
    "exp_name",
    "train_data_names",
    "val_data_names",
  ];
  const createInitState = (keys) => {
    const init_state = {};
    keys.forEach((key) => {
      init_state[key] = "";
    });
    return init_state;
  };
  const [inputs, setInputs] = useState(createInitState(argument_names));
  const [arglist, setArglist] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    // console.log(e.target.name, e.target.value);
    setInputs({
      ...inputs,
      [name]: value,
    });
    // console.log(inputs);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const args = combineArgs();
    setArglist(args);
  };

  const combineArgs = () => {
    return Object.entries(inputs)
      .filter(([key, value]) => value)
      .map(([key, value]) => `--${key} ${value}`)
      .join(" ");
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
        train_command: `CUDA_VISIBLE_DEVICES=7 python /sources/src/ml/train_vmae.py ${arglist}`,
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
    <div>
      <form onSubmit={handleSubmit}>
        {argument_names.map((arg) => (
          <TextField
            key={arg}
            id={arg}
            label={arg}
            name={arg}
            variant="outlined"
            fullWidth
            onChange={handleChange}
            sx={{ marginTop: 2 }}
          />
        ))}
        <Button
          type="submit"
          variant="contained"
          color="primary"
          sx={{ marginTop: 1 }}
        >
          Generate Command
        </Button>
      </form>
      <Stack direction="row" spacing={2} sx={{ marginTop: 4 }}>
        <Typography
          variant="body1"
          color="text.primary"
          sx={{ wordBreak: "break-all", flexGrow: 1 }}
        >
          {arglist}
        </Typography>
        <Button
          variant="contained"
          size="small"
          sx={{
            bgcolor: "lightgrey", // 배경색을 옅은 회색으로
            color: "black", // 글자색을 검정색으로
            // mt: 1, // 위의 스택과의 마진
            fontWeight: "bold", // 글자 두껍게
          }}
          onClick={postData}
        >
          Train Start
        </Button>
      </Stack>
    </div>
  );
}
