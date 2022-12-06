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