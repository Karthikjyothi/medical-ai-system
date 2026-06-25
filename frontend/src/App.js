import { BrowserRouter, Routes, Route } from "react-router-dom";
import CompareHistoryPage from "./pages/CompareHistoryPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Dashboard from "./pages/Dashboard";
import DiagnosePage from "./pages/DiagnosePage";
import ResultPage from "./pages/ResultPage";
import HistoryPage from "./pages/HistoryPage";
import AdminTrainPage from "./pages/AdminTrainPage";
import DatasetAnalyticsPage from "./pages/DatasetAnalyticsPage";
import MedicalAssistantPage from "./pages/MedicalAssistantPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/diagnose" element={<DiagnosePage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/admin-train" element={<AdminTrainPage />} />
        <Route path="/compare-history" element={<CompareHistoryPage />} />
        <Route path="/dataset-analytics" element={<DatasetAnalyticsPage />} />
        <Route path="/medical-assistant" element={<MedicalAssistantPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;