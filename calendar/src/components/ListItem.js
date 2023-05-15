import React from 'react'
import { Link } from 'react-router-dom'

const ListItem = ({ event }) => {
    return (
        <Link className='listitem-container' to={`/event/${event.event_id}`}>
            <div className="event-details">
                <h3>Event ID: {event.event_id}</h3>
                <p>Name: {event.name}</p>
                <p>Description: {event.description}</p>
                <p>Reminder Time: {event.reminder_time}</p>
                <p>Localization: {event.localization}</p>
                <p>Duration: {event.duration}</p>
                <p>Creation Date: {event.creation_date}</p>
                <p>Color: {event.color}</p>
                <p>First Occurrence: {event.first_occurrence}</p>
                <p>Event Creator: {event.event_creator}</p>
                <p>Event Category: {event.event_category}</p>
                <p>Priority Level: {event.priority_level}</p>
                <p>Repeat Pattern: {event.repeat_pattern}</p>
            </div>
        </Link>
    )
}

export default ListItem
