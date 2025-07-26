export type Event = {
  id: string;
  title: string;
  start: string;
  end: string;
  genre: string;
  allDay: boolean;
  users?: string[];
};
