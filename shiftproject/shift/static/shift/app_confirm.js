document.addEventListener('DOMContentLoaded', function () {
    // CSRF対策
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        selectable: true,
        select: function (info) {
            // 入力ダイアログ
            //const time = prompt("希望シフト開始-終了時間を入力してください ex)1000-1700");

            if (time) {

                // 登録処理の呼び出し
                axios
                    .post("/shift/confirmShift/", {
                        date: info.start.valueOf(),
                    })
                    .then((response) => {
                        // シフト時間を表示する処理の呼び出し
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