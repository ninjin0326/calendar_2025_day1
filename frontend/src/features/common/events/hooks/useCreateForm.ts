import { genres } from "@/features/const";
import { Event } from "@/types/type";
import { ceilDate, ceilFiveMinutes } from "@/utils/dayjsUtils";
import dayjs, { Dayjs } from "dayjs";
import { useEffect, useReducer, useState } from "react";

type CreateEventState = Omit<Event, "id" | "users" | "start" | "end"> & {
  id: string | null;
  start: Dayjs;
  end: Dayjs;
};

type Action =
  | { type: "SET_TITLE"; payload: string }
  | { type: "SET_START"; payload: Dayjs }
  | { type: "SET_END"; payload: Dayjs }
  | { type: "SET_GENRE"; payload: string }
  | { type: "SET_ALL_DAY"; payload: boolean }
  | { type: "RESET" }
  | { type: "SET_EVENT"; payload: CreateEventState };

const initialState = () => {
  const start = ceilFiveMinutes(ceilDate(dayjs(), "minute"));
  return {
    id: null,
    title: "",
    start: start,
    end: start.add(1, "hour"),
    genre: genres[0].genres,
    allDay: false,
  };
};

const eventReducer = (
  state: CreateEventState,
  action: Action
): CreateEventState => {
  switch (action.type) {
    case "SET_TITLE":
      return { ...state, title: action.payload };
    case "SET_START":
      // start と end の差を計算して、差を維持するように end を更新する
      return {
        ...state,
        start: action.payload,
        end: action.payload.add(state.end.diff(state.start)),
      };
    case "SET_END":
      return { ...state, end: action.payload };
    case "SET_GENRE":
      return { ...state, genre: action.payload };
    case "SET_ALL_DAY":
      return { ...state, allDay: action.payload };
    case "RESET":
      return initialState();
    case "SET_EVENT":
      return action.payload;
    default:
      return state;
  }
};

const useCreateForm = (initialEvent?: CreateEventState) => {
  initialEvent = initialEvent || initialState();
  const [state, dispatch] = useReducer(eventReducer, initialEvent);
  const [canSubmit, setCanSubmit] = useState(false);

  const setTitle = (title: string) =>
    dispatch({ type: "SET_TITLE", payload: title });

  const setStart = (start: Dayjs) =>
    dispatch({ type: "SET_START", payload: start });

  const setEnd = (end: Dayjs) => dispatch({ type: "SET_END", payload: end });

  const setGenre = (genre: string) =>
    dispatch({ type: "SET_GENRE", payload: genre });

  const setAllDay = (allDay: boolean) =>
    dispatch({ type: "SET_ALL_DAY", payload: allDay });

  const resetEvent = () => dispatch({ type: "RESET" });

  const setEvent = (event: CreateEventState) =>
    dispatch({ type: "SET_EVENT", payload: event });

  useEffect(() => {
    // TODO: タイトルのバリデーション機能を追加してください
    setCanSubmit(state.title !== "");
  }, [state]);

  return {
    event: state,
    setTitle,
    setStart,
    setEnd,
    setGenre,
    setAllDay,
    resetEvent,
    setEvent,
    canSubmit,
  };
};

export default useCreateForm;
