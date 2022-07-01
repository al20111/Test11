document.addEventListener('DOMContentLoaded', function () {
    // CSRF対策
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        selectable: true,
        select: function (info) {
            //alert("selected " + info.startStr + " to " + info.endStr);

            // 入力ダイアログ

            //const eventName = prompt("イベントを入力してください");
            const time = prompt("希望シフト開始-終了時間を入力してください ex)1000-1700");
            //end_time = prompt("シフト終了時間を入力してください");
         //   var splitedTime = time.split('-');
         //   splitedTime[0] = parseInt(splitedTime[0],10);
         //   splitedTime[1] = parseInt(splitedTime[1],10);

            if (time) {

                // 登録処理の呼び出し
                axios
                    .post("/shift/addShift/", {
                        
                        date: info.start.valueOf(),
                      //  start_time: splitedTime[0],//start_date: info.start.valueOf(), 
                      //  end_time: splitedTime[1],//end_date: info.end.valueOf(), 
                        //event_name: eventName,
                        time: time, 
                    })
                    .then(() => {
                        // イベントの追加
                        calendar.addEvent({
                            title: time,
                            start: info.start,
                            end: info.end,
                            allDay: true,

                        });

                    })
                    .catch(() => {
                        // バリデーションエラーなど
                        alert("登録に失敗しました");
                    });
            }
        },
        events: function (info, successCallback, failureCallback) {

            axios
                .post("/shift/listShift/", {
                    //date: info.start.valueOf(),

                    //start_time: splitedTime[1],
                    //end_time: splitedTime[0],
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                     バリデーションエラーなど
                    alert("登録に失敗しました");
                });
        },

    });

    calendar.render();
});