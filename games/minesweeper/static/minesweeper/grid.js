
// Is called after the DOM has been loaded
document.addEventListener('DOMContentLoaded', function(){

// Init from Dom
    
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
            console.log(mined);
          }
      })
    }

    // Update board
    function update_board(cell_name) {
      console.log('update_board');
      console.log(cell_name);
      const url_cells=  `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=update&cell_name=${cell_name}`;
      fetch(url_cells)
      .then(response => response.json())
      .then(data => {
          console.log(url_cells);
          // loop
          let hit_mine = false;
          data.forEach((item, i) => {
            //console.log(i, item);

            if (item.visible) {
              if (item.mined) {
                hit_mine = true;                

              } else {
                // update color and text
                document.getElementById(item.name).style.backgroundColor = 'silver';                
                //document.getElementById(item.name).innerHTML = `${item.value}`;
              } 
            } else {
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
    

    // Add event listener - To checkbox
    const is_visible = document.getElementById('is_visible')
    is_visible.onclick = function() {      
      if (is_visible.checked) {
        console.log('unhide');
        document.querySelectorAll('[id=cell_label]').forEach(element=> {
            element.style.setProperty('visibility', 'visible');
        });
      } else {
        console.log('hide');
        document.querySelectorAll('[id=cell_label]').forEach(element=> {
            element.style.setProperty('visibility', 'hidden');
        });
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
            let cell = button.dataset.cell
            if (cell != undefined) {
              update_board(cell);              
            } else if (button.id === 'reset') {
              console.log('reset');
              reset_game();
            }
        }
    })
});
