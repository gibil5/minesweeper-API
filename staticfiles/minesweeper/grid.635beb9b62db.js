

// Init from Dom - is called after the DOM has been loaded
document.addEventListener('DOMContentLoaded', function(){

/* Globals -------------------------------------------------------------------*/
    var game_over = false;
    var game_pause = false;
    var state_msg = ["created", "started", "paused", "end win", "end loose"];
    var month_msg = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
    var first_time = true;
    var flag_clicked = false;


/* Tools ---------------------------------------------------------------------*/
    function get_board_id() {
      return document.getElementById("board_id").innerHTML;      
    }

    function get_flag() {
      let flag = 0;
      if (flag_clicked) {
        flag = 1;
      }
      flag_clicked = false;
      return flag;
    }

    function get_state() {
      return document.getElementById("state").innerHTML;      
    }

    function get_rows() {
      return document.getElementById("rows_id").innerHTML;      
    }

    // Change the style of the grid, in function of the nr of columns
    var rows = get_rows();
    var style_value = `repeat(${rows},1fr)`
    console.log(style_value);
    document.querySelectorAll('[id=grid]').forEach(element=> {
        element.style.setProperty('grid-template-columns', style_value);
    });

    // Capitalize
    String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }


/* Datetime ------------------------------------------------------------------*/

    // Add zero
    function add_zero(item) {      
      if (item.length < 2) {        
        item = '0' + item;
      }
      return item
    }

    // Format date ampm
    function formatDateAmpm(date) {
      console.log('formatDateAmpm');
      var d = new Date(date),
        day = '' + d.getDate(),
        month = '' + (d.getMonth() + 1),
        year = d.getFullYear();
      var hours = d.getHours();
      var minutes = d.getMinutes();

      console.log(month);
      month = add_zero(month);
      console.log(month);

      day = add_zero(day);
      minutes = add_zero(minutes);
      var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
          hours = hours % 12;
          hours = hours ? hours : 12; // the hour '0' should be '12'
      var strTime = hours + ':' + minutes + ' ' + ampm;
      //return [day, month_msg[month-1], year].join(' ') + ' - ' + strTime;
      console.log([day, month, year].join('/') + ' - ' + strTime);
      return [day, month, year].join('/') + ' - ' + strTime;
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


/* Game funcs ----------------------------------------------------------------------*/

    // Update Stats 
    function update_stats(board) {
      //console.log('update_stats');
      //console.log(board);

      // Game over
      if (board.game_over) {

        // Globals
        game_over = true;

        // Stats
        let label = '';
        let color = '';
        let background_color = '';
        if (board.game_win) { 
          background_color = 'black';
          color = 'lightgreen';
          label = 'Win ';
        } else {
          background_color = 'black';
          color = 'red';
          label = 'Lost !';
        }
        
        // Date end
        const date_fmt = formatDateAmpm(board.end);
        document.getElementById('end').innerHTML = `${date_fmt}`;

        // Buttons
        document.getElementById('return_btn').style.visibility = 'visible';
        document.getElementById('return_btn').style.display = 'block';
        document.getElementById('pause_btn').style.visibility = 'hidden';
        document.getElementById('pause_btn').style.display = 'none';

        // Game over button
        document.getElementById('game_over_banner').style.background = background_color;
        document.getElementById('game_over_banner').style.color = color;
        document.getElementById('game_over_banner').innerHTML = label;
        document.getElementById('game_over_banner').style.display = 'block';
      }

      document.getElementById('state').innerHTML = `${state_msg[board.state_sm].capitalize()}`;
      document.getElementById('game_over').innerHTML = `${board.game_over.toString().capitalize()}`;
      document.getElementById('game_win').innerHTML = `${board.game_win.toString().capitalize()}`;
      document.getElementById('nr_flags').innerHTML = `${board.flags.length}`;
    }


    // Flag cell
    function flag_cell(item) {
      console.log('flag_cell');
      console.log(item);
      const lab = document.getElementById(`cell_label_${item.name}`);
      lab.style.visibility = "visible";
      lab.innerHTML = '?';
    }

    // Render
    function render(i, item, color, visibility) {
      //console.log('render');      
      //console.log(i);
      //console.log(item);
      
      const btn = document.getElementById(item.name);
      const lab = document.getElementById(`cell_label_${item.name}`);

      let txt = '';
      if (item.label === '-1') {
        txt = 'M';
      } else {
        txt = item.label;
      }

      btn.style.backgroundColor = color;
      btn.style.visibility = "visible";
      btn.display = "block";

      lab.innerHTML = txt;
      lab.style.visibility = visibility;
      lab.display = "block"; 

      if (item.label === '.') {
        lab.style.color = color;
      }
    }

    // Game loop
    function game_loop(data) {
      //console.log('game_loop');

      // render
      data.forEach((item, i) => {
        // Game over
        if (item.game_over) {
          if (item.success) {
            render(i, item, "lightgreen", "visible");    // success
          } else {
            render(i, item, "red", "visible");           // lose
          }
        // Play
        } else {
          if (item.visible) {
            render(i, item, "silver", "visible");        // normal
          } else if (item.flagged) {
            flag_cell(item);                             // flagged
          } else {
            render(i, item, "gainsboro", "hidden");      // hidden
          }
        }
      });
    }


/* Fetches -------------------------------------------------------------------*/

    // Fetch Chain - Game update
    function fetch_chain_update(board_id, cell_name, flag) {
      console.log('fetch_chain_update');
      //console.log(cell_name);
      //console.log(flag);
      // First fetch
      const url_cells = `/rest/board_update/?board_id=${board_id}&cell_name=${cell_name}&flag=${flag}`;
      var result = fetch(url_cells, {
          method: 'get',
        }).then(function(response) {
          return response.json();
        }).then(function(data) {

          // Game loop
          game_loop(data);

          // Second fetch
          const url_board = `/rest/boards/${board_id}/`;
          return fetch(url_board); 
        })
        .then(function(response) {
          return response.json();
        })
        .catch(function(error) {
          console.log('Request failed', error);
        })

      // Use the last result
      result.then(function(board) {
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
        document.getElementById("duration").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

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
          console.log('on click');

          let cell = button.dataset.cell;

          // Cell
          if (cell) {
            let board_id = get_board_id();
            let flag =  get_flag();
            // Update board
            fetch_chain_update(board_id, cell, flag);
          }
        }
    })

    // Flag
    const btn_flag = document.getElementById('btn_flag')
    btn_flag.onclick = function() {
      console.log('flag');
      flag_clicked = true;
    }


/* Test -------------------------------------------------------------------*/

    // Test
    const btn_test = document.getElementById('btn_test')
    btn_test.onclick = async function() {
      console.log('test');

      let nr_rows = get_rows();
      let cell = '';
      let board_id = get_board_id();
      let flag = 0;
      let i = 0;
      let x = 0;
      let y = 0;

      for (x = 0; x < nr_rows; x++) {
        for (y = 0; y < nr_rows; y++) {
          cell = `${x}_${y}`;
          console.log(cell);  
          if (!game_over) {            
            fetch_chain_update(board_id, cell, flag);
          } else {
            break;            
          }
          await new Promise(r => setTimeout(r, 1000));
        }
      }
      console.log('break !');
    }

});
