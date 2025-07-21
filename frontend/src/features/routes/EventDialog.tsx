import EventDelete from "@/features/common/events/EventDelete";
import EventDetail from "@/features/common/events/EventDetail";
import EventFormDialog from "@/features/common/events/EventFormDialog";
import { DialogState } from "@/features/routes/hooks/useDialogState";
import { Event } from "@/types/type";
import { Dialog } from "@mui/material";

const EventDialog = ({
  state,
  events,
  setDialogViewDetail,
  setDialogEdit,
  setDialogDelete,
  setDialogClose,
}: {
  state: DialogState;
  events: Event[];
  setDialogViewDetail: (id: string) => void;
  setDialogEdit: (id: string) => void;
  setDialogDelete: (id: string) => void;
  setDialogClose: () => void;
}) => {
  const DialogContentSwitcher = () => {
    switch (state.type) {
      case "create":
      case "edit":
        return (
          <EventFormDialog
            state={state}
            events={events}
            setDialogClose={setDialogClose}
            setDialogViewDetail={setDialogViewDetail}
          />
        );
      case "detail":
        return (
          <EventDetail
            eventId={state.id}
            events={events}
            setDialogEdit={setDialogEdit}
            setDialogDelete={setDialogDelete}
          />
        );
      case "delete":
        return (
          <EventDelete
            eventId={state.id}
            setDialogViewDetail={setDialogViewDetail}
            setDialogClose={setDialogClose}
          />
        );
      default:
        return null;
    }
  };
  return (
    <Dialog
      open={state.type !== "close"}
      maxWidth="xl"
      onClose={setDialogClose}
    >
      <DialogContentSwitcher />
    </Dialog>
  );
};

export default EventDialog;
