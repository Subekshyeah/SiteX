import { Outlet } from "react-router-dom";
import TopNav from "@/components/nav/TopNav";

export default function DashboardLayout() {
  return (
    <div className="flex flex-col h-screen w-full bg-slate-50 font-sans overflow-hidden">
      <TopNav />
      {/* Main Content Area */}
      <main className="flex-1 relative overflow-hidden flex">
        <Outlet />
      </main>
    </div>
  );
}