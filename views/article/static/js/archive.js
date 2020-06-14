function allDate(start, end) {
  start = start.split("-");
  var res = [],
    year = +start[0],
    month = +start[1],
    date = new Date(year, month, 0),
    endTime = new Date(end).getTime();
  while (date.getTime() <= endTime) {
    res.push(year + "-" + month.toString().replace(/^(\d)$/, "0$1"));
    //加一天，强制到下一月份
    date = new Date(date.getTime() + 24 * 60 * 60 * 1000);
    year = date.getFullYear();
    month = date.getMonth() + 1;
    date = new Date(year, month, 0);
  }
  res.push(end);
  return res.reverse();
}
function getEnd(list, item) {
  // list1 = list.reverse();
  if (!list[list.indexOf(item) - 1]) {
    return "2099-12";
  } else {
    console.log(list[list.indexOf(item) - 1]);
    return list[list.indexOf(item) - 1];
  }
}
