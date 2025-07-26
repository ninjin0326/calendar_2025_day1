import FullCalendar from "@fullcalendar/react";
import { useRef } from "react";

export const useCalendar = () => {
  const calendarRef = useRef<FullCalendar>(null);

  return { calendarRef };
};
