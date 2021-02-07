

// Init from Dom - is called after the DOM has been loaded
document.addEventListener('DOMContentLoaded', function(){
    
/* Globals -------------------------------------------------------------------*/
    var game_over = false;
    var game_pause = false;


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


/* Game ----------------------------------------------------------------------*/

    // Stats 
    function update_stats(board) {
      // Globals
      game_over = true;

      var state_msg = ["created", "started", "paused", "ended"];

      // Labels
      document.getElementById('state').innerHTML = `State: ${state_msg[board.state_sm].capitalize()}`;
      document.getElementById('game_over').innerHTML = `Game over: ${board.game_over.toString().capitalize()}`;
      document.getElementById('game_win').innerHTML = `Success: ${board.game_win.toString().capitalize()}`;
      const date_fmt = formatDate(board.end)
      document.getElementById('end').innerHTML = `End: ${date_fmt}`;

      // Nr ofs
      //document.getElementById('nr_mines').innerHTML = `Nr mines = ${board.nr_mines}`;
      //document.getElementById('nr_flags').innerHTML = `Nr flags = ${board.flags.length}`;
      //document.getElementById('nr_hidden').innerHTML = `Nr hidden = ${board.nr_hidden}`;
    }


    // End the game - Board visuals
    function end_game(board) {
      // Init
      let color = '';
      let label = '';
      if (board.game_win) { 
        color = 'lightgreen';
        label = 'game_over_success';
      } else {        
        color = 'red';
        label = 'game_over_defeat';
      }
      document.getElementById(label).style.visibility = 'visible';
      document.getElementById(label).style.display = 'block';
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

      document.getElementById('return_btn').style.visibility = 'visible';
      document.getElementById('pause_btn').style.visibility = 'hidden';

      // Stats 
      update_stats(board);
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

    // Format date
    function formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();
        var hour = '' + d.getHours(), 
            minutes = '' + d.getMinutes(), 
            seconds = '' + d.getSeconds();
        month = add_zero(month);
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

      const url_cells = `http://127.0.0.1:8000/board_update/?board_id=${board_id}&cell_name=${cell_name}&flag=${flag}`;

      // First fetch
      var result = fetch(url_cells, {
          method: 'get',
        }).then(function(response) {
          return response.json();
        }).then(function(data) {

          // Game loop
          game_loop(data);          

          // Second fetch
          const url_board = `http://127.0.0.1:8000/boards/${board_id}/`;
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
        console.log('Board');
        console.log(board);

        // Game over
        if (board.game_over) {
          console.log('Update stats !')
          console.log(board.end);          

          // End game
          end_game(board);
        }
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

});
