
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
            button.style.size = '40px';
            button.innerHTML = 'M';
            console.log(mined);
          }
      })
    }


    // Update board
    //function update_board(cell_name) {
    function update_board(cell_name, flag) {

      console.log('update_board');
      console.log(cell_name);
      const is_visible = document.getElementById(`cell_label_${cell_name}`).style.visibility;
      console.log(is_visible);

      if (is_visible != 'visible') {

        //const url_cells=  `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=update&cell_name=${cell_name}`;
        const url_cells=  `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=update&cell_name=${cell_name}&flag=${flag}`;

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
                  //document.getElementById(item.name).innerHTML = `${item.value}`;

                  document.getElementById(item.name).style.backgroundColor = 'silver';

                  //document.getElementById(`cell_label_${item.name}`).innerHTML = `${item.value}`;
                  document.getElementById(`cell_label_${item.name}`).innerHTML = `${item.label}`;

                  //document.getElementById(`cell_label_${item.name}`).style.size = '40px';
                  document.getElementById(`cell_label_${item.name}`).style.visibility = 'visible';
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
    }
    

    // Add event listener - To checkbox
    /*
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
    */
    
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
            
            let cell = button.dataset.cell
            if (cell != undefined) {
              update_board(cell, 0);              
            } else if (button.id === 'reset') {
              console.log('reset');
              reset_game();
            }
        }
    })

    // Capture right click - for flag
    //el.addEventListener('contextmenu', function(ev) {
    //document.getElementById('lorem').addEventListener('contextmenu', function(ev) {
    document.addEventListener('contextmenu', function(ev) {
        ev.preventDefault();
        alert('success!');
        return false;
    }, false);



    //window.oncontextmenu = function ()
    //{
    //    update_board(cell, 1);              
    //    console.log('Flag !');
        //showCustomMenu();
    //    return false;     // cancel default menu
    //}

    //window.oncontextmenu = function () {
      //alert('Right Click')
    //  const cell = '0_0'
    //  update_board(cell, 1);              
    //}

    //document.body.onclick = function (e) {
    //    var isRightMB;
    //    e = e || window.event;
    //    console.log('Flag 1 !');
    //    if ("which" in e)  // Gecko (Firefox), WebKit (Safari/Chrome) & Opera
    //        isRightMB = e.which == 3; 
    //    else if ("button" in e)  // IE, Opera 
    //        isRightMB = e.button == 2; 
    //    console.log(isRightMB);
        //alert("Right mouse button " + (isRightMB ? "" : " was not") + "clicked!");
    //}

    //$("#myId").mousedown(function(ev){
    //      console.log(ev);
    //      if(ev.which == 3)
    //      {
    //            alert("Right mouse button clicked on element with id myId");
    //      }
    //});

});
