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

            //if (time) {

                // シフト時間表示処理,給料情報の呼び出し
                axios
                    .post("/shift/ShiftMine/", {
                        date: info.start.valueOf(),
                    })
                    .then((response) => {
                        //選択された日付のシフト時間を表示
                        YEAR, MONTH, DATE, S_TIME, E_TIME, USER , MONEY = response.data 
                    })
                    .catch(() => {
                        // バリデーションエラーなど
                        alert("シフトがありません");
                    });
        //    }
        },
        events: function (info, successCallback, failureCallback) {

            axios
                .post("/shift/confirmShift/", {
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
