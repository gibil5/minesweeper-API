// 26 jan 2021


// Test fetches
const button = document.getElementById('test_btn')
button.onclick = function() {      
  console.log('jx');
  fetch_chain();
}


// Add event listener - To checkbox
const flag_cell_chk = document.getElementById('flag_cell_chk')
flag_cell_chk.onclick = function() {      
  if (flag_cell_chk.checked) {
    //console.log('flag cell');
  } else {
    //console.log('do not flag cell');
  }      
}



// Chain fetches - Test
function chain_fetches() {
  console.log('chain_fetches');
  var url = 'https://api.spacexdata.com/v2/launches/latest';
  var result = fetch(url, {
      method: 'get',
    }).then(function(response) {
      return response.json(); // pass the data as promise to next then block
    }).then(function(data) {
      var rocketId = data.rocket.rocket_id;
      console.log('First fetch');
      console.log(rocketId, '\n');
      return fetch('https://api.spacexdata.com/v2/rockets/' + rocketId); // make a 2nd request and return a promise
    })
    .then(function(response) {
      console.log('Second fetch');
      return response.json();
    //}).then(function(data) {
    //  console.log(data);
    })
    .catch(function(error) {
      console.log('Request failed', error)
    })
  // I'm using the result variable to show that you can continue to extend the chain from the returned promise
  result.then(function(r) {
    console.log('Result');
    console.log(r); // 2nd request result
  });
}



// Update board - Dep !
function update_board(board_id, cell_name, flag) {
  console.log('update_board');
  console.log(`cell_name: ${cell_name}`);
  console.log(`flag: ${flag}`);
  const url_cells = `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=update&cell_name=${cell_name}&flag=${flag}`;
  var result = fetch(url_cells)
    .then(response => response.json())
    .then(data => {
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
    })
  .catch(error => {
      console.log('Error', error);
  })
  // I'm using the result variable to show that you can continue to extend the chain from the returned promise
  result.then(function(r) {
    console.log(r); // 2nd request result
  })
}





// 25 jan 2021  

// Reset game
function reset_game() {
  document.querySelectorAll('button').forEach(button => {
      button.style.backgroundColor = 'gainsboro';
  })
}



// Get board

function get_board(board_id) {
  console.log('get_board');
  const url = `http://127.0.0.1:8000/boards/${board_id}/`;
  fetch(url)
  .then(response => response.json())
  .then(data => {
      console.log(url);
      console.log(data);
      console.log(data.mines);
      console.log(data.flags);
      console.log(data.game_over);
      console.log(data.success);
      if (data.game_over && data.success) {
        console.log('GAME OVER - SUCEESS !!!');
      }
  }
)};







// 21 jan 2021

// Get cells from board - Init - Called from views.py - Dep !
/*
function init_board(board_id) {
  const url_cells=  `http://127.0.0.1:8000/cells_from/?board_id=${board_id}&cmd=init`;
  fetch(url_cells)
  .then(response => response.json())
  .then(data => {
      //console.log(data);
      data.forEach((item, i) => {
        console.log(i, item);
      });          
  })
  .catch(error => {
      console.log('Error', error);
  })      
}
*/
// Init board
//init_board(board_id);




// before 

// Fetch - post
/*
const url_cells='http://127.0.0.1:8000/cells/';
fetch(url_cells,
{
    method: "POST",
    headers: {'Content-Type':'application/x-www-form-urlencoded'}, // this line is important, if this content-type is not set it wont work
    credentials: 'same-origin',
    body: `board_id=${board_id}&foo=bar&blah=1`
})
.then(response => response.json())
.then(data => {
    console.log(data);
})
.catch(error => {
    console.log('Error', error);
}) 
*/
