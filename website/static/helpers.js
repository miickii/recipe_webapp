// Function to check the width of the page and compare it with the previous width
// If the developer tools console gets resizes the width of page will change
let prev_curr_width;
function compareWidth() {
    let curr_width = document.getElementsByTagName("html")[0].clientWidth;
    if (curr_width != prev_curr_width) {
        console.log(curr_width);
    }

    prev_curr_width = curr_width;
}

// How to loop through each option of a select
/*
$("#categories option").each(function(){
    if ($(this).text() == "Easy") {
      $(this).attr("selected","selected");
      console.log($(this).text());
    }
});
*/