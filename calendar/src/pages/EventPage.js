import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Link } from 'react-router-dom';

const EventPage = () => {
    const { id } = useParams();
    let [event, setEvent] = useState(null);
    useEffect(() => {
        getEvent()
    }, [id])

    let getEvent = async () => {
        let response = await fetch(`/api/events/${id}`)
        let data = await response.json()
        setEvent(data)
    }
    let updateEvent = async () => {
        fetch(`/api/events/${id}/update`, {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(event)
        })
    }
    let handleSubmit = () => {
        updateEvent()
    }
    let deleteEvent = async () => {
        fetch(`/api/events/${id}/delete`, {
            method: "DELETE",
            headers: { 'Content-Type': 'application/json' }
        })
    }
    return (
        <div className='event-page-container'>
            <div className="event-container">
                <p>Event ID: {event?.event_id}</p>
                <p>Name: {event?.name}</p>
                <p>Description: {event?.description}</p>
                <p>Reminder Time: {event?.reminder_time}</p>
                <p>Localization: {event?.localization}</p>
                <p>Duration: {event?.duration}</p>
                <p>Creation Date: {event?.creation_date}</p>
                <p>Color: {event?.color}</p>
                <p>First Occurrence: {event?.first_occurrence}</p>
                <p>Event Creator: {event?.event_creator}</p>
                <p>Event Category: {event?.event_category}</p>
                <p>Priority Level: {event?.priority_level}</p>
                <p>Repeat Pattern: {event?.repeat_pattern}</p>
            </div>
            <div className='event-action-container'>
                <Link to="/"><button onClick={handleSubmit}>Submit</button></Link>
                <textarea
                    onChange={(e) => {
                        const fieldName = e.target.name;
                        const newValue = e.target.value;
                        setEvent((prevEvent) => {
                            if (newValue === prevEvent[fieldName]) {
                                return { ...prevEvent, [fieldName]: null };
                            } else {
                                return { ...prevEvent, [fieldName]: newValue };
                            }
                        });
                    }}
                    name="description"
                    defaultValue={event?.description}
                ></textarea>
                <Link to="/"><button onClick={deleteEvent}>Delete</button></Link>
            </div>

        </div>
    )
}

export default EventPage
