var ttt = {
  init: function() {
    $("td").click(ttt.cellClicked);
  },
  cellClicked: function() {
    $(this).addClass("player");
    ttt.submit();
  },
  submit: function() {
    var board = { board: JSON.stringify(ttt.getBoardData()) };
    console.log(board);
    $.post('/board', data=board, function(data) {
      ttt.drawBoard(JSON.parse(data));
    });
  },
  getBoardData: function() {
    var boardData = [];
    $("#board tr").each(function() {
      var row = [];
      $(this).find("td").each(function() {
        var val = 0;
        if($(this).hasClass('player')) {
          val = 2;
        } else if ($(this).hasClass('comp')) {
          val = 1;
        }
        row.push(val);
      });
      boardData.push(row);
    });
    return boardData;
  },
  drawBoard: function(data) {
    console.log(data);
    if(data.status != "Playing") {
      window.alert(data.status);
    }

    $("td").removeClass("player").removeClass("comp");
    $("tr").each(function(y, row) {
      $(row).find("td").each(function(x, cell) {
        if(data.board[y][x] == 1) {
          $(cell).addClass("comp");
        } else if(data.board[y][x] == 2) {
          $(cell).addClass("player");
        }
      });
    });
  }
};

$(ttt.init);
