document.addEventListener('DOMContentLoaded', function () {
    // CSRF対策
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ja',
        dayCellContent: function (e) {
            e.dayNumberText = e.dayNumberText.replace('日', '');
        },

        selectable: true,
        select: function (info) {
            const time = prompt("希望シフト開始-終了時間を入力してください ex)1000-1700");
            var ST = time.substring(0,4);
            var ET = time.substring(5);
            let st = Number(ST);
            let et = Number(ET);
            if (isNaN(st) || isNaN(et)){
                alert("正しく入力してください ex)1000-1700")
            }
            else if(st >= et){
                alert("開始時間は終了時間より前に設定してください");
            }
            else if(st/100 > 24 || et/100 > 24){
                alert("時刻は0:00以上24:00未満で設定してください");
            }
            else if(st%100 >= 60 || et%100 >= 60){
                alert("分数は0~59で設定してください")
            }
            else {

                // 登録処理の呼び出し
                axios
                    .post("/shift/addShift/", {
                        
                        date: info.start.valueOf(),
                        time: time, 
                    })
                    .then(() => {
                        // イベントの追加


                        var SH = String(Math.floor(st/100));
                        
                        if(st%100 == 0){
                            var SM = '00';
                        }else{
                            var SM = String(st%100);
                        }
                        var EH = String(Math.floor(et/100));
                        if(et%100 == 0){
                            var EM = '00';
                        }else{
                            var EM = String(et%100);
                        }
                        
                        var Title = SH + ':' + SM + '-' + EH + ":" + EM; 
                        calendar.addEvent({
                            title: Title,
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