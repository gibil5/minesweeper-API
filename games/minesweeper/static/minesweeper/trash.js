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
