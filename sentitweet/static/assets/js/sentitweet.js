function filterSearchAll() {
    var input, filter, i;
    input = document.getElementById("searchAllInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("searchAllDropdown");
    options = div.getElementsByTagName("li");
    for (i = 0; i < options.length; i++) {
      txtValue = options[i].textContent || options[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        options[i].style.display = "";
      } else {
        options[i].style.display = "none";
      }
    }
  }

// function filterTable() {
//   var input, filter, i;
//   input = document.getElementById("searchTable");
//   filter = input.value.toUpperCase();
//   table = document.getElementById("listAllTable");
//   options = table.getElementsByTagName("tr");
// }


$("#searchTable").on("keyup", function() {
  var value = $(this).val().toLowerCase();
  $("#listAllTable tr").filter(function() {
      $(this).toggle($(this).text()
      .toLowerCase().indexOf(value) > -1)
  });
});