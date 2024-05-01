import Image from "next/image";
import EventsContainer from "./components/eventscontainer";

export default function Home() {

  return (
    <div className="min-h-screen p-6">
      <EventsContainer />
    </div>
  );
}
