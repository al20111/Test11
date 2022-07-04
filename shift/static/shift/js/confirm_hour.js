function TimeTableView(USER, YEAR, MONTH, DATE, S_TIME, E_TIME) {
  var timetable = new Timetable();
  timetable.setScope(9, 22); // optional, only whole hours between 0 and 23
  timetable.useTwelveHour(); //optional, displays hours in 12 hour format (1:00PM)
  timetable.addLocations([USER]);

  S_time_hour = Math.floor(S_TIME / 100);
  S_time_min = S_TIME % 100;
  E_time_hour = Math.floor(E_TIME / 100);
  E_time_min = E_TIME % 100;
  timetable.addEvent('承認済み', USER, new Date(YEAR, MONTH, DATE, S_time_hour, S_time_min), new Date(YEAR, MONTH, DATE, E_time_hour, E_time_min));
  var renderer = new Timetable.Renderer(timetable);
  renderer.draw('.timetable'); // any css selector
  //
}

function TimeTableAuthor(LIST) {
  var timetable = new Timetable();
  timetable.setScope(9, 22); // optional, only whole hours between 0 and 23
  timetable.useTwelveHour(); //optional, displays hours in 12 hour format (1:00PM)

  var num = LIST.length;
  var user = [LIST[0].user];
  for (let i = 1; i < num; i++) {
    user.push(LIST[i].user);
  }
  timetable.addLocations(user);
  for (let i = 0; i < num; i++) {
    S_time_hour = Math.floor(LIST[i].start / 100);
    S_time_min = LIST[i].start % 100;
    E_time_hour = Math.floor(LIST[i].end / 100);
    E_time_min = LIST[i].end % 100;
    timetable.addEvent('承認済み', LIST[i].user, new Date(LIST[i].year, LIST[i].month, LIST[i].date, S_time_hour, S_time_min), new Date(LIST[i].year, LIST[i].month, LIST[i].date, E_time_hour, E_time_min));
  }
  var renderer = new Timetable.Renderer(timetable);
  renderer.draw('.timetable'); // any css selector
}