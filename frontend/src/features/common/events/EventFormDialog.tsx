import { postEvent, putEvent } from "@/features/common/events/fetch";
import useCreateForm from "@/features/common/events/hooks/useCreateForm";
import { genres } from "@/features/const";
import { DialogState } from "@/features/routes/hooks/useDialogState";
import { Event } from "@/types/type";
import { ceilDate, floorDate } from "@/utils/dayjsUtils";
import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Switch,
  TextField,
} from "@mui/material";
import { DatePicker, TimePicker } from "@mui/x-date-pickers";
import dayjs, { Dayjs } from "dayjs";

const EventFormDialog = ({
  state,
  events,
  setDialogViewDetail,
  setDialogClose,
}: {
  state: DialogState;
  events: Event[];
  setDialogViewDetail: (id: string) => void;
  setDialogClose: () => void;
}) => {
  const convertEventToCreateEventState = (event?: Event) => {
    if (!event) return;
    return {
      id: event.id,
      title: event.title,
      start: dayjs(event.start),
      end: event.allDay ? dayjs(event.end).add(-1, "second") : dayjs(event.end),
      genre: event.genre,
      allDay: event.allDay,
    };
  };

  const { event, setTitle, setStart, setEnd, setGenre, setAllDay, canSubmit } =
    useCreateForm(
      state.type === "edit"
        ? convertEventToCreateEventState(
            events.find((event) => event.id === state.id)
          )
        : undefined
    );

  if (state.type !== "create" && state.type !== "edit") return null;

  const handleChangeTitle = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
  };

  const handleChangeAllDay = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAllDay(e.target.checked);
  };

  const handleChangeStart = (date: dayjs.Dayjs | null) => {
    if (date === null) return;
    setStart(date);
  };

  const handleChangeEnd = (date: Dayjs | null) => {
    if (date === null) return;
    setEnd(date);
  };

  const isNotValidEnd = (date: Dayjs) => {
    return !date.isAfter(event.start) || date.isSame(event.start);
  };

  const handleChangeGenre = (e: SelectChangeEvent) => {
    setGenre(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const submitParams = {
      ...event,
      id: event.id === null ? undefined : event.id,
      start: event.allDay
        ? floorDate(event.start, "day").toJSON()
        : event.start.toJSON(),
      end: event.allDay
        ? ceilDate(event.end, "day").toJSON()
        : event.end.toJSON(),
    };
    if (state.type === "edit" && submitParams.id !== undefined) {
      await putEvent(submitParams as Event).then(() => {
        setDialogClose();
        submitParams.id && setDialogViewDetail(submitParams.id);
      });
      return;
    }
    await postEvent(submitParams)
      .then(() => {
        setDialogClose();
      })
      .catch((e) => {
        console.error(e);
      });
  };
  return (
    <div
      style={{
        width: 700,
        height: 700,
        padding: 20,
        boxSizing: "border-box",
      }}
    >
      <h3>{state.type === "edit" ? "既存予定編集" : "新規予定作成"}</h3>
      <form
        style={{
          maxWidth: "100%",
        }}
        onSubmit={handleSubmit}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
            columnGap: 20,
            rowGap: 20,
            marginBottom: 20,
          }}
        >
          <TextField
            label="タイトル"
            value={event.title}
            onChange={handleChangeTitle}
            style={{ gridColumn: "1 / 3" }}
          />
          <div style={{ gridColumn: "1 / 3" }}>
            <strong>終日</strong>
            <Switch checked={event.allDay} onChange={handleChangeAllDay} />
          </div>
          <DatePicker
            format="YYYY/MM/DD"
            slotProps={{ calendarHeader: { format: "YYYY年MM月" } }}
            value={event.start}
            onChange={handleChangeStart}
            sx={{ gridColumn: !event.allDay ? "" : "1 / 3" }}
          />
          {!event.allDay && (
            <TimePicker
              label="開始時間"
              ampm={false}
              value={event.start}
              onChange={handleChangeStart}
            />
          )}
          <DatePicker
            format="YYYY/MM/DD"
            slotProps={{ calendarHeader: { format: "YYYY年MM月" } }}
            value={event.end}
            onChange={handleChangeEnd}
            sx={{ gridColumn: !event.allDay ? "" : "1 / 3" }}
            shouldDisableDate={isNotValidEnd}
          />
          {!event.allDay && (
            <TimePicker
              label="開始時間"
              ampm={false}
              shouldDisableTime={isNotValidEnd}
              value={event.end}
              onChange={handleChangeEnd}
            />
          )}
          <FormControl style={{ gridColumn: "1 / 3" }}>
            <InputLabel id="genre-select-label">種別</InputLabel>
              <Select
                labelId="genre-select-label"
                label="genre"
                value={event.genre}
                onChange={handleChangeGenre}
                renderValue={(selected) => {
                  const selectedColor = genres.find(
                    (genre) => genre.genres === selected
                  )?.color;
                  return (
                    <div style={{ display: "flex", alignItems: "center" }}>
                      <Box
                        sx={{
                          width: 10,
                          height: 10,
                          borderRadius: "50%",
                          backgroundColor: selectedColor,
                          marginRight: 1,
                        }}
                      ></Box>
                      {selected}
                    </div>
                  );
                }}
              >
                {genres.map((genre) => (
                  <MenuItem key={genre.genres} value={genre.genres}>
                    {genre.genres}
                  </MenuItem>
                ))}
              </Select>
          </FormControl>
        </div>
        <Button type="submit" variant="contained">
          保存
        </Button>
      </form>
    </div>
  );
};

export default EventFormDialog;
