import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import CssBaseline from "@mui/material/CssBaseline";

import dayjs from "dayjs";
import "dayjs/locale/ja";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";

import CalendarApp from "@/features/routes/CalendarApp";

dayjs.locale("ja");

dayjs.extend(utc);
dayjs.extend(timezone);

const JsonPlugin = (option: any, dayjsClass: any, dayjsFactory: any) => {
  // overriding existing API
  dayjsClass.prototype.toJSON = function () {
    return this.format();
  };
};
dayjs.extend(JsonPlugin);

function App() {
  return (
    <>
      <LocalizationProvider
        dateAdapter={AdapterDayjs}
        dateFormats={{ year: "YYYY年" }}
      >
        <CssBaseline />
        <CalendarApp />
      </LocalizationProvider>
    </>
  );
}

export default App;
