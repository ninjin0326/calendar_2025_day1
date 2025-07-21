import { deleteEvent } from "@/features/common/events/fetch";
import { Button } from "@mui/material";

const EventDelete = ({
  eventId,
  setDialogViewDetail,
  setDialogClose,
}: {
  eventId: string;
  setDialogViewDetail: (id: string) => void;
  setDialogClose: () => void;
}) => {
  const handleDelete = () => {
    deleteEvent(eventId).then(() => {
      setDialogClose();
    });
  };
  return (
    <div
      style={{
        width: 500,
        padding: 20,
        boxSizing: "border-box",
      }}
    >
      <h2>予定削除?</h2>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Button onClick={() => setDialogViewDetail(eventId)}>キャンセル</Button>
        <Button onClick={handleDelete} variant="contained" color="error">
          削除
        </Button>
      </div>
    </div>
  );
};

export default EventDelete;
