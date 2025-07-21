import { Dayjs } from "dayjs";

type Unit = "minute" | "hour" | "day" | "month" | "year";

export const ceilDate = (date: Dayjs, unit: Unit): Dayjs => {

  /**
   * 切り上げ時に1を加算するかどうかを判定する
   */
  const addUnit = (date: Dayjs, unit: Unit) => {
    switch (unit) {
      case "minute":
        return date.second() !== 0 || date.millisecond() !== 0;
      case "hour":
        return (
          date.minute() !== 0 || date.second() !== 0 || date.millisecond() !== 0
        );
      case "day":
        return (
          date.hour() !== 0 ||
          date.minute() !== 0 ||
          date.second() !== 0 ||
          date.millisecond() !== 0
        );
      case "month":
        return (
          date.date() !== 1 ||
          date.hour() !== 0 ||
          date.minute() !== 0 ||
          date.second() !== 0 ||
          date.millisecond() !== 0
        );

      case "year":
        return (
          date.month() !== 0 ||
          date.date() !== 1 ||
          date.hour() !== 0 ||
          date.minute() !== 0 ||
          date.second() !== 0 ||
          date.millisecond() !== 0
        );

      default:
        return false;
    }
  };
  switch (unit) {
    case "minute": {
      const addFlag = addUnit(date, "minute");
      return date
        .second(0)
        .millisecond(0)
        .add(addFlag ? 1 : 0, "minute");
    }
    case "hour": {
      const addFlagHour = addUnit(date, "hour");
      return date
        .minute(0)
        .second(0)
        .millisecond(0)
        .add(addFlagHour ? 1 : 0, "hour");
    }
    case "day": {
      const addFlagDay = addUnit(date, "day");

      return date
        .hour(0)
        .minute(0)
        .second(0)
        .millisecond(0)
        .add(addFlagDay ? 1 : 0, "day");
    }
    case "month": {
      const addFlagMonth = addUnit(date, "month");
      return date
        .date(1)
        .hour(0)
        .minute(0)
        .second(0)
        .millisecond(0)
        .add(addFlagMonth ? 1 : 0, "month");
    }
    case "year": {
      const addFlagYear = addUnit(date, "year");
      return date
        .month(0)
        .date(1)
        .hour(0)
        .minute(0)
        .second(0)
        .millisecond(0)
        .add(addFlagYear ? 1 : 0, "year");
    }
  }
};

export const floorDate = (date: Dayjs, unit: Unit): Dayjs => {
  switch (unit) {
    case "minute":
      return date.second(0).millisecond(0);
    case "hour":
      return date.minute(0).second(0).millisecond(0);
    case "day":
      return date.hour(0).minute(0).second(0).millisecond(0);
    case "month":
      return date.date(1).hour(0).minute(0).second(0).millisecond(0);
    case "year":
      return date.month(0).date(1).hour(0).minute(0).second(0).millisecond(0);
  }
};

export const ceilFiveMinutes = (date: Dayjs) => {
  const minute = date.minute();
  const diff = 5 - (minute % 5);
  return date.add(diff, "minute");
};
