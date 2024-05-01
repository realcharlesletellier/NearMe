'use client'
import React, { useEffect, useState } from 'react';
import eventsData from '../../event_names.json'; // Adjust path based on project structure

interface Event {
    id: number;
    title: string;
  }
  

const EventsContainer = () => {
  const [events, setEvents] = useState<Event[]>([]); // State to hold events

  useEffect(() => {
    // Load events from JSON file
    const loadedEvents = eventsData.map((event, index) => ({
      id: index + 1, // Assign unique ID based on index
      title: event.title, // Read title from JSON
    }));
    setEvents(loadedEvents); // Set the events state
  }, []); // Empty dependency array ensures it runs once

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-4xl font-bold text-center mb-6">What's Going On?</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map((event) => (
          <div key={event.id} className="card bg-base-100 shadow-xl p-4">
            <h2 className="text-2xl font-bold mt-4">{event.title}</h2>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventsContainer;