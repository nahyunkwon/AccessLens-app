function update_suggestion(object){
    suggestion_title = document.getElementById('suggestion-title');
    suggestion = document.getElementById('suggestion');

    suggestion_title.innerHTML = "<h3>" + object + "</h3>"

    // suggestion.innerHTML = "<h4>" + object + "</h4>";

    // open ul element
    // suggestion.innerHTML = ""
    suggestion.innerHTML = suggestion.innerHTML + "<ul>\n";


    // add list component
    design_title = "title1"
    design_img = "static/assets/images/design/design.jpg"
    design_full_link = "https://www.thingiverse.com/thing:2271048"
    suggestion.innerHTML = suggestion.innerHTML + "<li>" + design_title + "<img class='design' src=" + design_img + "></li>\n";

    // close ul element
    suggestion.innerHTML = suggestion.innerHTML + "</ul>";
       


}

