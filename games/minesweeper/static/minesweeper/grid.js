

// Init from Dom - is called after the DOM has been loaded
document.addEventListener('DOMContentLoaded', function(){
    
    // Globals
    var game_over = false;


    // Change the style of the grid, in function of the nr of columns
    var rows = document.getElementById("rows").innerHTML;
    var style_value = `repeat(${rows},1fr)`
    console.log(style_value);
    document.querySelectorAll('[id=grid]').forEach(element=> {
        element.style.setProperty('grid-template-columns', style_value);
    });


    // End the game - called from update_board
    function end_game(game_success) {
      game_over = true;
      let color = '';
      let label = '';
      if (game_success) { 
        color = 'lightgreen';
        label = 'game_over_success';
      } else {        
        color = 'red';
        label = 'game_over_defeat';
      }
      document.getElementById(label).style.visibility = 'visible';
      document.getElementById(label).style.display = 'block';
      document.querySelectorAll('button').forEach(button => {
          button.style.backgroundColor = color;
          let mined = button.dataset.mined;
          if (mined === 'True') {
            button.style.size = '40px';
            button.innerHTML = 'M';
            console.log(mined);
          }
      })
    }


    // Update cell
    function update_cell(item) {
      // button
      document.getElementById(item.name).style.backgroundColor = 'silver';
      document.getElementById(item.name).style.visibility = 'visible';
      document.getElementById(item.name).display = 'block'; 
      // label
      document.getElementById(`cell_label_${item.name}`).innerHTML = `${item.label}`;
      document.getElementById(`cell_label_${item.name}`).style.visibility = 'visible';
      document.getElementById(`cell_label_${item.name}`).style.display = 'block'; 
      if (item.label === '.') {        
        document.getElementById(`cell_label_${item.name}`).style.color = 'silver';      
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
      // loop
      data.forEach((item, i) => {        
        if (! item.success) {                
          if (item.visible) {
            if (item.mined) {
              hit_mine = true;                
            } else {
              update_cell(item);
            } 
          } else if (item.flagged) {
              flag_cell(item);
          }
        } else {

          game_success = true;

        }
      });
      // end loop
      if (game_success) {
        console.log('end_game');
        end_game(true);            
      } 
      if (hit_mine) {
        end_game(false);            
      }       
    }


    // Chain fetches - Game update
    function fetch_chain_update(board_id, cell_name, flag) {
      console.log('fetch_chain_update');
      const url_cells = `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=update&cell_name=${cell_name}&flag=${flag}`;

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
        document.getElementById('nr_mines').innerHTML = `Nr mines = ${board.nr_mines}`;
        document.getElementById('nr_flags').innerHTML = `Nr flags = ${board.flags.length}`;
        document.getElementById('nr_hidden').innerHTML = `Nr hidden = ${board.nr_hidden}`;
      });
    }


    // Add event listener - To all buttons
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            let cell = button.dataset.cell;
            const flag_cell = document.getElementById('flag_cell_chk');
            var flag = 0;
            if (flag_cell.checked) {
              flag = 1;
              flag_cell.checked = false;
            } else {
              flag = 0;
            }
            if (cell != undefined) {
              const is_visible = document.getElementById(`cell_label_${cell}`).style.visibility;
              if (!is_visible) {
                const board_id = document.getElementById("board_id").innerHTML;
                console.log(board_id);
                // Update board
                fetch_chain_update(board_id, cell, flag);
              }
            } else if (button.id === 'reset') {
              console.log('reset');
              reset_game();
            }
        }
    })


    // Time tracking
    var startDate = new Date().getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {

      console.log(game_over);
      if (! game_over) {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = now - startDate;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
          document.getElementById("demo").innerHTML = 'Duration: ' + days + "d " + hours + "h "
          + minutes + "m " + seconds + "s ";

        // If the count down is finished, write some text
        if (distance < 0) {
          clearInterval(x);
          document.getElementById("demo").innerHTML = "EXPIRED";
        }        
      }
    }, 1000);


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

        //if (month.length < 2) 
        //    month = '0' + month;
        //if (day.length < 2) 
        //    day = '0' + day;

        month = add_zero(month);
        day = add_zero(day);
        hour = add_zero(hour);
        minutes = add_zero(minutes);
        seconds = add_zero(seconds);

        return [day, month, year].join('-') + ' ' + [hour, minutes, seconds].join(':');
    }

    // Reset
    function reset() {      
      console.log('Reset');
      
      // Init startDate
      game_over = false;

      startDate = new Date();
      const date_fmt = formatDate(startDate)
      document.getElementById('start').innerHTML = 'Start: ' + date_fmt;

      return 5;
    }
    // Reset button
    const button = document.getElementById('reset_btn')
    button.onclick = function() {      
      ret = reset();
      console.log(ret);
    }


});
