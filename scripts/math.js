//calculation of power based on modes
function getPower(){
  let modeValue = document.getElementsByName("modes").value;
  let averagingTable = document.getElementsByName("convTable");
  for (var i = 0, row; row = averagingTable.rows[i]; i++) {
   //iterate through rows
   //rows would be accessed using the "row" variable assigned in the for loop
    for (var j = 0, col; col = row.cells[j]; j++) {
       //iterate through columns
       //columns would be accessed using the "col" variable assigned in the for loop
       console.log(table.rows[r].cells[c].innerHTML);
    }
  }
  return false
}
