import { fetchApi, getBackendUrl } from "@/features/api";
import { Event } from "@/types/type";

export const fetchEvents = () =>
  fetchApi<Event[]>(getBackendUrl("/api/events").toString(), {});

export const fetchEvent = (id: string) =>
  fetchApi<Event>(getBackendUrl(`/api/events/${id}`).toString(), {});

export const postEvent = (event: Omit<Event, "id">) => {
  return fetchApi<null>(getBackendUrl("/api/events").toString(), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(event),
  });
};

export const putEvent = (event: Event) => {
  return fetchApi<null>(getBackendUrl(`/api/events/${event.id}`).toString(), {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(event),
  });
};

export const deleteEvent = (id: string) => {
  return fetchApi<null>(getBackendUrl(`/api/events/${id}`).toString(), {
    method: "DELETE",
  });
};
