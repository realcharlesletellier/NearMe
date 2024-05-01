/* eslint-disable */ 
'use client';
import React, { useEffect, useState } from 'react';
import eventsData from '../../events.json';

interface Event {
  id: number;
  title: string;
  link: string;
  image: string;
  date: string;
  location: string;
}

const EventsContainer = () => {
  const [events, setEvents] = useState<Event[]>([]); // State to hold events

  useEffect(() => {
    // Load events from JSON file
    const loadedEvents = eventsData.map((event, index) => ({
      id: index + 1,
      title: event.title,
      link: event.link,
      image: event.image,
      date: event.date,
      location: event.location,
    }));
    setEvents(loadedEvents);
  }, []);

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-4xl font-bold text-center mb-8">What's Going On?</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map((event) => (
          <div key={event.id} className="card bg-secondary-content shadow-xl rounded-lg p-4 flex flex-col items-center">
            <img src={event.image} alt={event.title} className="w-full h-48 object-cover rounded-lg" />
            <h2 className="text-2xl font-bold mt-4 text-primary-content text-center">{event.title}</h2>
            <p className="text-md text-primary-content mt-2">{event.date}</p>
            <p className="text-md text-primary-content">{event.location}</p>
            <a
              href={event.link}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 px-4 py-2 bg-accent text-white rounded-lg hover:bg-blue-600 transition"
            >
              View Event
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventsContainer;
