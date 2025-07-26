import Calendar from "@/features/common/calendar/Calendar";
import { useEvents } from "@/features/common/events/hooks/useEvents";
import EventDialog from "@/features/routes/EventDialog";
import { useDialogState } from "@/features/routes/hooks/useDialogState";
import { EventClickArg } from "@fullcalendar/core";
import { useEffect } from "react";

const CalendarApp = () => {
  const { events, updateEvents } = useEvents();
  const {
    state,
    setDialogCreate,
    setDialogViewDetail,
    setDialogEdit,
    setDialogDelete,
    setDialogClose,
  } = useDialogState();

  useEffect(() => {
    updateEvents();
  }, [state]);

  const handleClickCreate = () => {
    setDialogCreate();
  };

  const handleEventClick = (arg: EventClickArg) => {
    setDialogViewDetail(arg.event.id);
  };

  return (
    <>
      <main
        style={{
          padding: "0 12px",
        }}
      >
        <div style={{ margin: 20 }}>
          <Calendar
            events={events}
            eventClick={handleEventClick}
            handleClickCreate={handleClickCreate}
          />
        </div>
      </main>

      <EventDialog
        state={state}
        events={events}
        setDialogViewDetail={setDialogViewDetail}
        setDialogEdit={setDialogEdit}
        setDialogDelete={setDialogDelete}
        setDialogClose={setDialogClose}
      />
    </>
  );
};

export default CalendarApp;
