import React from "react";
import { Route, Routes } from "react-router-dom";

import Dashboard from "./MainPage";
import DevPage from "./DevPage";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/dev" element={<DevPage />} />
    </Routes>
  );
};

export default App;
