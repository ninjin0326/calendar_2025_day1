import FullCalendar from "@fullcalendar/react";
import { CalendarOptions } from "@fullcalendar/core";
import { RefObject } from "react";

type CalendarOptionsProps = CalendarOptions & {
  reactRef: RefObject<FullCalendar>;
};

const Calendar = (props: CalendarOptionsProps) => {
  return <FullCalendar ref={props.reactRef} {...props} />;
};

export default Calendar;
