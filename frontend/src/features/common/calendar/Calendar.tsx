import BaseFullCalendar from "@/components/FullCalendar";
import { useCalendar } from "@/features/common/calendar/hooks/useCalendar";
import { Event } from "@/types/type";
import { EventClickArg, EventDropArg } from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin, { EventResizeDoneArg } from "@fullcalendar/interaction";
import { putEvent } from "@/features/common/events/fetch";
import { useEffect, useState } from "react";
import { Button, ButtonGroup } from "@mui/material";
import "./Calendar.css";

const Calendar = ({
  events,
  height,
  eventClick,
  handleClickCreate,
}: {
  events: Event[];
  height?: number;
  eventClick: (arg: EventClickArg) => void;
  handleClickCreate?: () => void;
}) => {
  const { calendarRef } = useCalendar();

  const [headerDate, setHeaderDate] = useState<Date>(new Date());

  const getCalendarApi = () => {
    const calendar = calendarRef.current?.getApi();
    if (!calendar) throw new Error("Calendar is not initialized");
    return calendar;
  };

  const updateHeaderDate = () => {
    setHeaderDate(getCalendarApi().getDate());
  };

  useEffect(() => {
    updateHeaderDate();
  }, [calendarRef]);

  const handlePrev = () => {
    getCalendarApi().prev();
    updateHeaderDate();
  };

  const handleToday = () => {
    getCalendarApi().today();
    updateHeaderDate();
  };

  const handleNext = () => {
    getCalendarApi().next();
    updateHeaderDate();
  };

  const handleEventChange = (event: EventDropArg | EventResizeDoneArg) => {
    const beforeEvent = events.find((e) => e.id === event.event.id);
    if (!beforeEvent) return;
    const newEvent = {
      ...beforeEvent,
      start: event.event.start?.toISOString(),
      end: event.event.end?.toISOString(),
    };

    // TypeGuard
    const isEvent = (arg: {
      start: string | undefined;
      end: string | undefined;
      id: string;
      title: string;
      genre: string;
      allDay: boolean;
      users?: string[];
    }): arg is Event => {
      return newEvent.start !== null && newEvent.end !== null;
    };

    if (isEvent(newEvent)) {
      putEvent(newEvent);
    }
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginBottom: 6,
        }}
      >
        <h1 style={{ display: "inline-block", margin: 0 }}>
          {headerDate
            ? `${headerDate.getFullYear()}年${headerDate.getMonth() + 1}月`
            : ""}
        </h1>
        <ButtonGroup style={{ height: "full", alignItems: "center", marginLeft: 16 }}>
          <Button onClick={handlePrev} style={{ height: "full" }}>
            前
          </Button>
          <Button onClick={handleToday} style={{ height: "full" }}>
            今日
          </Button>
          <Button onClick={handleNext} style={{ height: "full" }}>
            次
          </Button>
        </ButtonGroup>
        <Button onClick={handleClickCreate} variant="contained" color="primary" style={{ marginLeft: 16 }}>
          予定作成
        </Button>
      </div>

      <div className="calendar-container">
        <div className="calendar">
          <BaseFullCalendar
            reactRef={calendarRef}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            selectable={true}
            editable={true}
            headerToolbar={false}
            locale="ja"
            events={events}
            height={height ?? 800}
            eventClick={eventClick}
            eventDrop={handleEventChange}
            eventResize={handleEventChange}
          />
        </div>
      </div>
    </div>
  );
};

export default Calendar;
