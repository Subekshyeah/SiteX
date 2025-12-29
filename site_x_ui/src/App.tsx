// App.tsx (top)
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ResultPage from "./pages/Result";
import LocationForm from "@/components/locationForm/locationForm";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LocationForm />} />         {/* your existing root */}
        <Route path="/result" element={<ResultPage />} /> {/* new route */}
        {/* optional: keep existing SPA routes here */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;