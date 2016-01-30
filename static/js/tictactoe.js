var ttt = {
  init: function() {
    ttt.createTable();
    $("td").click(ttt.cellClicked);
  },

  createTable: function() {
    var table = $("<table>");
    for(var y=0;y<=2;y++) {
      var row = $("<tr>");
      for(var x=0;x<=2;x++) {
        $(row).append($("<td>").addClass("clickable"));
      }
      $(table).append(row);
    }
    $("#content").append(table);
  },

  cellClicked: function() {
    if ( ( !$(this).hasClass("clickable") ) || 
          $(this).hasClass("comp") || 
          $(this).hasClass("player")) {
      return false;
    }
    $(this).addClass("player");

    // fake some thinking time so the player thinks he has a chance
    $("td").removeClass("clickable");
    var thinkTime = Math.floor(Math.random() * 1000);
    window.setTimeout(ttt.submit, thinkTime);
  },

  submit: function() {
    var board = { board: JSON.stringify(ttt.getBoardData()) };
    $.post('/board', data=board, function(data) {
      ttt.drawBoard(JSON.parse(data));
    });
  },

  getBoardData: function() {
    var boardData = [];
    $("table tr").each(function() {
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
    $("tr").each(function(y, row) {
      $(row).find("td").each(function(x, cell) {
        if(data.board[y][x] == 1) {
          $(cell).addClass("comp");
        } else if(data.board[y][x] == 2) {
          $(cell).addClass("player");
        } else {
          $(cell).addClass("clickable");
        }
      });
    });
    if(data.status != "Playing") {
      window.alert(data.status);
    }
  }
};

$(ttt.init);
