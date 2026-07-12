import Sidebar from "./components/Sidebar";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Chat from "./pages/Chat";
import Compliance from "./pages/Compliance";
import Commissioning from "./pages/Commissioning";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Risk from "./pages/Risk";
import SupplyChain from "./pages/SupplyChain";
import "./styles/global.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />

        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/login" element={<Login />} />
            <Route path="/compliance" element={<Compliance />} />
            <Route path="/risk" element={<Risk />} />
            <Route path="/supplychain" element={<SupplyChain />} />
            <Route path="/commissioning" element={<Commissioning />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
