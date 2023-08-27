function update_suggestion(object){
    suggestion_title = document.getElementById('suggestion-title');
    suggestion = document.getElementById('suggestion');

    suggestion_title.innerHTML = "<h3>" + object + "</h3>"

    suggestion.innerHTML = "<h4>" + object + "</h4>"
        + "Test";

}