import React, { useState, useEffect } from 'react'
import ListItem from '../components/ListItem'

const EventsListPage = () => {

    let [events, setEvents] = useState([])
    useEffect(() => {
        getEvents()
    }, [])

    let getEvents = async () => {
        let response = await fetch('/api/events/')
        let data = await response.json()
        console.log(data)
        setEvents(data)

    }

    return (
        <div>
            <div className='eventslistpage-event-list'>
                {events.map((event, index) => (
                    <ListItem key={index} event={event} />
                ))}
            </div>

        </div>
    )
}

export default EventsListPage
