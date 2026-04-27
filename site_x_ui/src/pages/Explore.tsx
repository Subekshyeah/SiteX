import { SidebarPanel } from "@/components/Explore/Sidebar";
import { ExploreMap } from "@/components/Explore/Map";
import { ExploreDirectory } from "@/components/Explore/Directory";

export default function ExplorePage() {
  return (
    <div className="flex h-full w-full bg-gray-50 relative overflow-hidden">
      {/* Left Sidebar */}
      <SidebarPanel />

      {/* Main Area: Map + Overlapping floating panels */}
      <div className="flex-1 w-full h-full relative">
        <ExploreDirectory />
        <ExploreMap />
      </div>
    </div>
  );
}