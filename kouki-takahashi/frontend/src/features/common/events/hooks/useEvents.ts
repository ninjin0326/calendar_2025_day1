import { fetchApi, getBackendUrl } from "@/features/api";
import { Event } from "@/types/type";
import { useEffect, useState } from "react";
import { genres } from "../../../const";

/**
 * 予定一覧を取得するカスタムフック
 * @returns schedules 予定一覧
 * @returns updateSchedules 予定一覧を更新する関数
 */
export const useEvents = () => {
  const [events, setEvents] = useState<Event[]>([]);

  const updateEvents = () => {
    fetchApi<Event[]>(getBackendUrl("/api/events").toString(), {}).then(
      (events) => {
        if (!events) return;
        // color情報がないため付与
        const eventsWithColor = events.map(e => ({
          ...e,
          color: getGenreColor(e.genre)
        }));
        setEvents(eventsWithColor);
      }
    );
  };

  useEffect(() => {
    updateEvents();
  }, []);

  return { events, updateEvents };
};

const getGenreColor = (genreName: string) => {
  const matchingGenre = genres.find(genre => genre.genres === genreName);
  return matchingGenre?.color || '#3788d8'
}
