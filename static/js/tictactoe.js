var ttt = {
    init: function () {
        ttt.createTable();
        $("td").click(ttt.cellClicked);
        $("#restart").click(ttt.init);
    },

    createTable: function () {
        var table = $("table").empty();
        $(".line").remove();
        $("h3").removeClass("doslidein").addClass("doslideout");
        for (var y = 0; y <= 2; y++) {
            var row = $("<tr>");
            for (var x = 0; x <= 2; x++) {
                var cell = $("<td>").attr("data-val", 0).attr("data-col", x);
                if(y==x) {
                    $(cell).attr("data-ltr", "1");
                }
                if((x==2 && y==0) || (y==1 && x==1) || (y==2 && x==0)) {
                    $(cell).attr("data-rtl", "1");
                }
                $(row).append(cell);
            }
            $(table).append(row);
        }
        $(table).removeClass("disabled");
    },

    cellClicked: function () {
        if ($("table").hasClass("disabled")) {
            return false;
        }

        if($(this).attr("data-val") != 0) {
            return false;
        }
        $(this).attr("data-val", 2);
        // fake some thinking time so the player thinks he has a chance
        $("table").addClass("disabled");
        var thinkTime = Math.floor(Math.random() * 1000);
        window.setTimeout(ttt.submit, thinkTime);
    },

    submit: function () {
        var board = {board: JSON.stringify(ttt.getBoardData())};
        $.post('board', data = board, function (data) {
            ttt.drawBoard(JSON.parse(data));
        });
    },

    getBoardData: function () {
        var boardData = [];
        $("table tr").each(function () {
            var row = [];
            $(this).find("td").each(function () {
                row.push(parseInt($(this).attr("data-val")));
            });
            boardData.push(row);
        });
        return boardData;
    },

    drawBoard: function (data) {
        $("tr").each(function (y, row) {
            $(row).find("td").each(function (x, cell) {
                $(cell).attr("data-val", data.board[y][x]);
            });
        });
        if (data.status != "Playing") {
            $("h3").removeClass("doslideout").addClass("doslidein").text(data.status);
            $("table").addClass("disabled");
            ttt.computeLine();
            if (data.status == 'Win') {
                // sore loser
                document.location.href="https://www.youtube.com/watch?v=dQw4w9WgXcQ";
            };
        } else {
            $("table").removeClass("disabled");
        }
    },

    computeLine: function() {
        // wow, making the line took way more effort than i thought :)
        for(var i=0;i<3;i++) {
            if($("tr:nth-child(" + i + ") td[data-val='1']").length == 3 ||
                $("tr:nth-child(" + i + ") td[data-val='2']").length == 3) {
                ttt.drawLine("row", i);
            }
            if($("td[data-col='" + i + "'][data-val='1']").length == 3 ||
                $("td[data-col='" + i + "'][data-val='2']").length == 3) {
                ttt.drawLine("col", i+1);
            }
        }
        if($("td[data-rtl='1'][data-val='1']").length == 3 ||
            $("td[data-rtl='1'][data-val='2']").length == 3) {
            ttt.drawLine("rtl", null);
        }
        if($("td[data-ltr='1'][data-val='1']").length == 3 ||
            $("td[data-ltr='1'][data-val='2']").length == 3) {
            ttt.drawLine("ltr", null);
        }
    },

    drawLine: function(lineType, index) {
        console.log("Drawing line of type: " + lineType + " at index: " + index);
        $(".line").remove();
        var line = $("<div>").addClass("line");
        if(lineType == 'row') {
            $("table tr:nth-of-type(" + index + ") td:first").append($("<div>").addClass("line hline"));
        } else if (lineType == 'col') {
            $("table tr:first td:nth-of-type(" + index + ")").append($("<div>").addClass("line vline"));
        } else if (lineType == 'ltr') {
            $("table tr:first td:first").append($("<div>").addClass("line ltrline"));
        } else if (lineType == 'rtl') {
            $("table tr:first td:nth-child(3)").append($("<div>").addClass("line rtlline"));
        }
    }
};

$(ttt.init);
