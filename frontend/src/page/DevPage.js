import { React, useState } from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { Button, TextField, Stack } from "@mui/material";

import TrainBox from "../task/Training";

const BackArea = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper, // 흰색 배경
  padding: theme.spacing(2), // padding 추가
  borderRadius: theme.shape.borderRadius, // border radius 추가
  boxShadow: theme.shadows[1], // 그림자 효과 추가
}));

export default function DevPage() {
  const openInNewTab = (url) => {
    // window.open() 함수를 사용하여 새 창에서 URL 열기
    const newWindow = window.open(url, "_blank", "noopener,noreferrer");
    if (newWindow) newWindow.opener = null; // 보안을 위해 사용
  };
  const [url, setUrl] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault(); // 폼 제출 시 페이지 리로드 방지
    console.log("Submitting URL:", url); // 콘솔에 URL 출력 (테스트용)

    // 여기서 서버로 URL을 전송하는 로직을 구현하세요.
    // 예: axios.post('/api/submit-url', { url: url })
  };

  return (
    <Box
      sx={{
        flexGrow: 1,
        maxWidth: 1000,
        backgroundColor: "grey.300",
        margin: "auto",
        padding: 2,
      }}
    >
      <Grid container spacing={2} justifyContent="space-between">
        {/* 첫 번째 Grid 아이템 */}
        <Grid item xs={12} md={5}>
          <Typography
            sx={{ mt: 4, mb: 2 }}
            variant="h6"
            component="div"
            fontWeight="bold"
          >
            Training
          </Typography>
          <BackArea>
            <List>
              <Stack direction="row" spacing={2}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() =>
                    openInNewTab(process.env.REACT_APP_AIRFLOW_URL)
                  }
                  textTransform="none"
                >
                  Training Schedule Page
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => openInNewTab(process.env.REACT_APP_MLFLOW_URL)}
                  textTransform="none"
                >
                  Train Log Page
                </Button>
              </Stack>
              <TrainBox />
            </List>
          </BackArea>
        </Grid>

        {/* 두 번째 Grid 아이템 */}
        <Grid item xs={12} md={5}>
          <Typography
            sx={{ mt: 4, mb: 2 }}
            variant="h6"
            component="div"
            fontWeight="bold"
          >
            Crwaling & Labeling
          </Typography>
          <BackArea>
            <List>
              <Stack direction="row" spacing={2}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() =>
                    openInNewTab(process.env.REACT_APP_LABELSTUDIO_URL)
                  }
                  textTransform="none"
                >
                  Label Studio Page
                </Button>
              </Stack>
              <Button
                variant="contained"
                sx={{
                  bgcolor: "lightgrey", // 배경색을 옅은 회색으로
                  color: "black", // 글자색을 검정색으로
                  width: "100%", // 가로로 꽉 차게
                  mt: 1, // 위의 스택과의 마진
                  fontWeight: "bold", // 글자 두껍게
                  textTransform: "none",
                  mb: 2,
                }}
              >
                Active Learning Start
              </Button>
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
            </List>
          </BackArea>
        </Grid>
      </Grid>
    </Box>
  );
}
