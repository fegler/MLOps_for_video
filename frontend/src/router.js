import React from "react";
import { Route, Routes } from "react-router-dom";

import Dashboard from "./page/MainPage";
import DevPage from "./page/DevPage";
// import TestPage from "./page/TestPage";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/dev" element={<DevPage />} />
      {/* <Route path="/test" element={<TestPage />} /> */}
    </Routes>
  );
};

export default App;
