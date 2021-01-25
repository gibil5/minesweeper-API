

// Init from Dom
// Is called after the DOM has been loaded
document.addEventListener('DOMContentLoaded', function(){
    
    // Change the style of the grid, in function of the nr of columns
    var rows = document.getElementById("rows").innerHTML;
    var style_value = `repeat(${rows},1fr)`
    console.log(style_value);
    document.querySelectorAll('[id=grid]').forEach(element=> {
        element.style.setProperty('grid-template-columns', style_value);
    });


    // Board id
    var board_id = document.getElementById("board_id").innerHTML;
    console.log(board_id);


    // End game - called from update_board
    function end_game() {
      document.querySelectorAll('button').forEach(button => {
          button.style.backgroundColor = 'red';
          let mined = button.dataset.mined;
          if (mined === 'True') {
            button.style.size = '40px';
            button.innerHTML = 'M';
            console.log(mined);
          }
      })
    }


    // Update board
    function update_board(cell_name, flag) {
      console.log('update_board');
      console.log(`cell_name: ${cell_name}`);
      console.log(`flag: ${flag}`);
      const is_visible = document.getElementById(`cell_label_${cell_name}`).style.visibility;
      console.log(is_visible);
      if (is_visible != 'visible') {
        const url_cells=  `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=update&cell_name=${cell_name}&flag=${flag}`;
        fetch(url_cells)
        .then(response => response.json())
        .then(data => {
            console.log(url_cells);
            // loop
            let hit_mine = false;
            data.forEach((item, i) => {
              //console.log(i, item);
              // If visible
              if (item.visible) {
                if (item.mined) {
                  hit_mine = true;                
                } else {
                  // update 
                  document.getElementById(item.name).style.backgroundColor = 'silver';
                  document.getElementById(`cell_label_${item.name}`).innerHTML = `${item.label}`;
                  document.getElementById(`cell_label_${item.name}`).style.visibility = 'visible';
                } 
              } else if (item.flagged) {
                console.log('flagged');
                document.getElementById(`cell_label_${item.name}`).style.visibility = 'visible';
                document.getElementById(`cell_label_${item.name}`).innerHTML = 'F';                
              }
            });
            // end of game
            if (hit_mine) {
              console.log('*** END GAME !!!');
              end_game();            
            }  
        })
        .catch(error => {
            console.log('Error', error);
        })
      }
    }


    // Add event listener - To checkbox
    const flag_cell = document.getElementById('flag_cell')
    flag_cell.onclick = function() {      
      if (flag_cell.checked) {
        console.log('flag cell');
      } else {
        console.log('do not flag cell');
      }      
    }
    
    
    // Reset game
    function reset_game() {
      document.querySelectorAll('button').forEach(button => {
          button.style.backgroundColor = 'gainsboro';
      })
    }


    // Add event listener - To all buttons
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            console.log('onclick');
            let cell = button.dataset.cell;
            const flag_cell = document.getElementById('flag_cell');
            var flag = 0;
            if (flag_cell.checked) {
              console.log('flag cell');
              flag = 1;
              flag_cell.checked = false;
            } else {
              console.log('do not flag cell');
              flag = 0;
            }
            if (cell != undefined) {
              update_board(cell, flag);
            } else if (button.id === 'reset') {
              console.log('reset');
              reset_game();
            }
        }
    })
});
