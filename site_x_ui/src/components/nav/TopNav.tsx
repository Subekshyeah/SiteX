import { Link, useLocation } from "react-router-dom";
import { HelpCircle, User, Settings, Crown } from "lucide-react";
import { Button } from "@/components/ui/button";

const NAV_ITEMS = [
  { name: "Workspace", path: "/workspace" },
  { name: "Explore", path: "/" },
  { name: "Property", path: "/property" },
  { name: "POIs", path: "/pois" },
  { name: "Market Overview", path: "/market-overview" },
  { name: "Advanced Reports", path: "/advanced-reports" },
  { name: "Datasets", path: "/datasets" },
];

export default function TopNav() {
  const location = useLocation();

  return (
    <div className="flex flex-col w-full border-b border-slate-200 bg-white z-[9999] relative">
      {/* Top Utility Bar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center gap-4">
          <div className="font-bold text-xl tracking-tight flex items-center gap-2 text-indigo-600">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-black">S</div>
            SiteX
          </div>
          <div className="max-w-md w-full ml-4">
            <div className="relative">
              <svg className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>
              <input 
                type="text" 
                placeholder="Search for Properties, Chains, and more" 
                className="w-full h-9 pl-9 pr-4 rounded-md border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-500">
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"><Settings className="w-4 h-4" /></Button>
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"><HelpCircle className="w-4 h-4" /></Button>
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"><User className="w-4 h-4" /></Button>
        </div>
      </div>

      {/* Main Navigation Tabs */}
      <div className="flex items-center px-4 overflow-x-auto custom-scrollbar bg-white">
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              className={`whitespace-nowrap px-4 py-3 text-sm font-semibold border-b-2 transition-colors ${
                isActive 
                  ? "border-indigo-600 text-indigo-600" 
                  : "border-transparent text-slate-500 hover:text-slate-800 hover:border-slate-300"
              }`}
            >
              {item.name}
            </Link>
          );
        })}
      </div>

      {/* Upgrade Banner (Optional, matches Placer.ai reference) */}
      <div className="flex items-center justify-between px-4 py-2 bg-indigo-50/50 border-t border-slate-100 text-sm">
        <div className="flex items-center gap-2 text-slate-700 font-medium">
          <Crown className="w-4 h-4 text-indigo-500" />
          Upgrade your plan for full access to our reports, analytics and more.
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" className="h-8 bg-white font-semibold">Schedule a Demo</Button>
          <Button size="sm" className="h-8 bg-indigo-600 hover:bg-indigo-700 font-semibold shadow-sm">Upgrade Plan</Button>
        </div>
      </div>
    </div>
  );
}