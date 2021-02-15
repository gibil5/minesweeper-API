

// Init from Dom - is called after the DOM has been loaded
document.addEventListener('DOMContentLoaded', function(){
    

/* Globals -------------------------------------------------------------------*/
    var game_over = false;
    var game_pause = false;
    var state_msg = ["created", "started", "paused", "end win", "end loose"];
    var month_msg = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
    var board_glob = false;


/* Tools ---------------------------------------------------------------------*/
    function get_board_id() {
      return document.getElementById("board_id").innerHTML;      
    }

    function get_flag() {
      const flag_cell = document.getElementById('flag_cell_chk');
      var flag = 0;
      if (flag_cell.checked) {
        flag = 1;
        flag_cell.checked = false;
      } else {
        flag = 0;
      }
      return flag;
    }

    function get_state() {
      return document.getElementById("state").innerHTML;      
    }

    // Change the style of the grid, in function of the nr of columns
    var rows = document.getElementById("rows").innerHTML;
    var style_value = `repeat(${rows},1fr)`
    console.log(style_value);
    document.querySelectorAll('[id=grid]').forEach(element=> {
        element.style.setProperty('grid-template-columns', style_value);
    });

    // Capitalize
    String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }



/* Game funcs ----------------------------------------------------------------------*/

    // Update Stats 
    function update_stats(board) {
      console.log('update_stats');
      console.log(board);

      // Game over
      if (board.game_over) {

        // Globals
        game_over = true;

        // Stats
        let label = '';
        let color = '';
        if (board.game_win) { 
          color = 'lightgreen';
          label = 'Game over - You won !';
        } else {        
          color = 'red';
          label = 'Game over - You lost !';
        }        
        // Game over
        document.getElementById('game_over_banner').innerHTML = label;
        document.getElementById('game_over_banner').style.color = color;

        // Date end
        //const date_fmt = formatDate(board.end)
        const date_fmt = formatDateAmpm(board.end)
        document.getElementById('end').innerHTML = `End: ${date_fmt}`;

        // Buttons
        document.getElementById('return_btn').style.visibility = 'visible';
        document.getElementById('return_btn').style.display = 'block';
        document.getElementById('pause_btn').style.visibility = 'hidden';
        document.getElementById('pause_btn').style.display = 'none';

        // Board
        end_game(board.game_win);
      }


      // Labels
      document.getElementById('state').innerHTML = `State: ${state_msg[board.state_sm].capitalize()}`;
      document.getElementById('game_over').innerHTML = `Game over: ${board.game_over.toString().capitalize()}`;
      document.getElementById('game_win').innerHTML = `Success: ${board.game_win.toString().capitalize()}`;

      // Nr ofs
      //document.getElementById('nr_mines').innerHTML = `Nr mines = ${board.nr_mines}`;
      //document.getElementById('nr_hidden').innerHTML = `Nr hidden = ${board.nr_hidden}`;
      document.getElementById('nr_flags').innerHTML = `Nr flags = ${board.flags.length}`;
    }


    // End the game - Board visuals
    //function end_game(board) {
    function end_game(game_win) {

      // Init
      let color = '';
      //if (board.game_win) { 
      if (game_win) { 
        color = 'lightgreen';
      } else {        
        color = 'red';
      }

      document.querySelectorAll('button').forEach(button => {

          if ((button.id != 'pause_btn') && (button.id != 'return_btn') ){

            button.style.backgroundColor = color;
            let mined = button.dataset.mined;
            if (mined === 'True') {
              button.style.size = '40px';
              button.innerHTML = 'M';
              console.log(mined);
            }
          }
      });
      document.querySelectorAll(".label_visible").forEach(button => {
        button.style.backgroundColor = color;
      });
    }


    // update cell
    function update_cell(item) {
      document.getElementById(item.name).style.backgroundColor = "silver";
      document.getElementById(item.name).style.visibility = "visible";
      document.getElementById(item.name).display = "block";
      document.getElementById(`cell_label_${item.name}`).innerHTML = `${item.label}`;
      document.getElementById(`cell_label_${item.name}`).style.visibility = "visible";
      document.getElementById(`cell_label_${item.name}`).style.display = "block"; 
      if (item.label === '.') {
        document.getElementById(`cell_label_${item.name}`).style.color = "silver";
      }
    }

    // Flag cell
    function flag_cell(item) {
      console.log('flag_cell func');
      console.log(item.name);
      document.getElementById(`cell_label_${item.name}`).style.visibility = 'visible';
      document.getElementById(`cell_label_${item.name}`).innerHTML = item.label;
    }


    // Game loop
    function game_loop(data) {
      let hit_mine = false;
      let game_success = false;
      let end = '';
      data.forEach((item, i) => {        
        if (! item.success) {                
          if (item.visible) {
            if (!item.mined) {
              update_cell(item);
            } 
          } else if (item.flagged) {
              flag_cell(item);
          }
        }
      });
    }

    // Add zero
    function add_zero(item) {      
      if (item.length < 2) {        
        item = '0' + item;
      }
      return item
    }

    // Format date ampm
    function formatDateAmpm(date) {
      var d = new Date(date),
        day = '' + d.getDate(),
        month = '' + (d.getMonth() + 1),
        year = d.getFullYear();
      var hours = d.getHours();
      var minutes = d.getMinutes();
      day = add_zero(day);
      minutes = add_zero(minutes);
      var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
          hours = hours % 12;
          hours = hours ? hours : 12; // the hour '0' should be '12'
      var strTime = hours + ':' + minutes + ' ' + ampm;
      return [day, month_msg[month-1], year].join(' ') + ' - ' + strTime;
    }

    // Format date
    function formatDate(date) {        
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();
        var hour = '' + d.getHours(), 
            minutes = '' + d.getMinutes(), 
            seconds = '' + d.getSeconds();
        day = add_zero(day);
        hour = add_zero(hour);
        minutes = add_zero(minutes);
        seconds = add_zero(seconds);
        return [day, month, year].join('-') + ' ' + [hour, minutes, seconds].join(':');
    }

/* Fetches -------------------------------------------------------------------*/

    // Fetch Chain - Game update
    function fetch_chain_update(board_id, cell_name, flag) {
      console.log('fetch_chain_update');
      console.log(cell_name);
      console.log(flag);
      // First fetch
      //const url_cells = `https://minesweeper-api-jr.herokuapp.com:8000/rest/board_update/?board_id=${board_id}&cell_name=${cell_name}&flag=${flag}`;
      //const url_cells = `http://localhost:8000/rest/board_update/?board_id=${board_id}&cell_name=${cell_name}&flag=${flag}`;
      const url_cells = `/rest/board_update/?board_id=${board_id}&cell_name=${cell_name}&flag=${flag}`;
      var result = fetch(url_cells, {
          method: 'get',
        }).then(function(response) {
          return response.json();
        }).then(function(data) {
          // Game loop
          game_loop(data);
          // Second fetch
          //const url_board = `https://minesweeper-api-jr.herokuapp.com:8000/rest/boards/${board_id}/`;
          //const url_board = `http://localhost:8000/rest/boards/${board_id}/`;
          const url_board = `/rest/boards/${board_id}/`;
          return fetch(url_board); 
        })
        .then(function(response) {
          return response.json();
        })
        .catch(function(error) {
          console.log('Request failed', error)
        })
      // Use the last result
      result.then(function(board) {
        // Globals 
        board_glob = board;
        // Stats 
        update_stats(board);
      });
    }

/* Time -------------------------------------------------------------------*/

    // Time tracking
    var startDate = new Date().getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {

      //console.log(game_over);
      //if (! game_over && !game_pause) {
      if (!game_over && !(get_state() === 'State: pause')) {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = now - startDate;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="duration"
        document.getElementById("duration").innerHTML = 'Duration: ' + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        // If the count down is finished, write some text
        if (distance < 0) {
          clearInterval(x);
          document.getElementById("duration").innerHTML = "EXPIRED";
        }        
      }
    }, 1000);



/* Testing -------------------------------------------------------------------*/

    function testing() {
      console.log('testing');

      //end_game(true);
      //end_game(false);

      console.log(board_glob);
      board_glob.game_over = true;
      update_stats(board_glob);
    }


/* Buttons -------------------------------------------------------------------*/

    // All buttons - Add event listener
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
          let cell = button.dataset.cell;
          // If board cell
          if (cell) {
            const is_visible = document.getElementById(`cell_label_${cell}`).style.visibility;
            if (!is_visible) {
              // Update board
              board_id = get_board_id();
              flag = get_flag();
              fetch_chain_update(board_id, cell, flag);
            }
          }
        }
    })

    // Testing
    const button = document.getElementById('test_btn')
    button.onclick = function() {
      testing();
    }

});
