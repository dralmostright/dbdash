import dayjs from "dayjs";

export const getRelativeTime = (date) => {
  return dayjs(date).fromNow();
};

export const formatDateTime = (value) => {
  if (!value) return value;

  const d = dayjs(value);
  if (!d.isValid()) return value;

  return d.format("YYYY/MM/DD HH:mm:ss");
};