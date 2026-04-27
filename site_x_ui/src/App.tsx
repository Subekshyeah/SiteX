// App.tsx (top)
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ResultPage from "./pages/Result";
import ExplorePage from "./pages/Explore";
import DashboardLayout from "@/layouts/DashboardLayout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<ExplorePage />} />
        </Route>
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;