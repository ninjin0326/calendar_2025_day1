import { Event } from "@/types/type";
import { useEffect, useState } from "react";
import ModeEditIcon from "@mui/icons-material/ModeEdit";
import { Box, Button } from "@mui/material";
import { genres } from "@/features/const";

const EventDetail = ({
  eventId,
  events,
  setDialogEdit,
  setDialogDelete,
}: {
  eventId: string;
  events: Event[];
  setDialogEdit: (id: string) => void;
  setDialogDelete: (id: string) => void;
}) => {
  const [event, setEvent] = useState<Event | null>(null);
  useEffect(() => {
    setEvent(events.find((event) => event.id === eventId) || null);
  }, [events, eventId]);
  if (!event) return;

  // TODO: 課題5 - 日時表示のフォーマットを修正してください
  const dateToString = (date: Date, dayOnly = false) => {
    const day = `${date.getFullYear()}/${
      date.getMonth() + 1
    }/${date.getDate()}`;

    if (dayOnly) return day;

    const time = `${date.getHours()}:${
      (date.getMinutes() < 10 ? "0" : "") + date.getMinutes()
    }`;

    return `${day} ${time}`;
  };


  const startDate = new Date(event?.start);
  const startString = dateToString(startDate, event.allDay);

  const endDate = new Date(event?.end);
  // 終日の場合は前日を指定する
  const endString = dateToString(
    event.allDay ? new Date(endDate.getTime() - 1) : endDate,
    event.allDay
  );

  const handleClickEdit = () => {
    setDialogEdit(event.id);
  };


  return (
    <div
      style={{
        width: 500,
        // height: 500,
        padding: 20,
        boxSizing: "border-box",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <h2 style={{ margin: 0 }}>{event.title}</h2>
          <p style={{ margin: 0 }}>
            {startString} ~ {endString}
          </p>
        </div>
        <div style={{ display: "flex" }}>
          <Button onClick={handleClickEdit} size="small" aria-label="edit">
            <ModeEditIcon />
          </Button>
          {/* TODO: 課題6 - 削除ボタンを追加してください */}
        </div>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "100px 1fr" }}>
        <p>
          <strong>ジャンル</strong>
        </p>
        <div style={{ display: "flex", alignItems: "center" }}>
         <Box bgcolor={genres.find((genre) => genre.genres === event.genre)?.color} sx={{ width: 10, height: 10, borderRadius: "50%", marginRight: 1 }} />
          { event.genre }
        </div>
      </div>
    </div>
  );
};

export default EventDetail;
