
/* Load image name */
var urlParams = new URLSearchParams(window.location.search);
var name = urlParams.get('name');
document.getElementById("myImg").src = "static/assets/images/input/" + name;



/* Load designs */
function load_design(design_element){

    var a = document.createElement('a');
    a.href = design_element['design_url'];
    
    var img = document.createElement("img");
    img.src = design_element["image_url"];
    // img.src = "https://cdn.thingiverse.com/assets/2a/24/a1/7f/62/card_preview_90085844_211047486634488_3888945027983867904_n.jpg";
    img.classList.add('design-element');
    // img.setAttribute("onclick", 'window.open("'+designs[design_id]['design_url']+'"');

    a.appendChild(img);

    return a

}

function update_suggestion(object){
    
    suggestion_title = document.getElementById('suggestion-title');
    suggestion = document.getElementById('suggestion');

    
    if(object.includes("__")){
        suggestion_title.innerHTML = "<h2>" + object.split("__")[0] + " - " + object.split("__")[1].replace("_", " ")  + "</h2>";
    }
    else{
        suggestion_title.innerHTML = "<h2>" + object + "</h2>";
    }

    while (suggestion.hasChildNodes()) {
        suggestion.removeChild(suggestion.lastChild);
    }

    if(Object.keys(dictionary).includes(object)){
        var object_designs = dictionary[object];

        var root_object_designs = [];

        // If it has IC (type)
        if(object.includes("__") && Object.keys(dictionary).includes(object.split("__")[0])){
            root_object_designs = dictionary[object.split("__")[0]];
        }

        var keys = Object.keys(object_designs);

        for(var i=0;i<keys.length;i++){
            var key = keys[i];
            
            if(object_designs[key].length != 0){
                var key_div = document.createElement('div');
                key_div.innerHTML = "<h3>" + key + "</h3>";

                for(var j=0;j<object_designs[key].length;j++){
                    key_div.appendChild(load_design(object_designs[key][j])); // dict object
                }

                if(root_object_designs.length != 0){
                    for(var j=0;root_object_designs[key].length;j++){
                        key_div.appendChild(load_design(root_object_designs[key][j]));
                    }
                }

                suggestion.appendChild(key_div);
            }
        }

        

    }


    // // suggestion.innerHTML = "<h4>" + object + "</h4>";

    // // open ul element
    // // suggestion.innerHTML = ""
    // suggestion.innerHTML = suggestion.innerHTML + "<ul>\n";


    // // add list component
    // design_title = "title1"
    // design_img = "static/assets/images/design/design.jpg"
    // design_full_link = "https://www.thingiverse.com/thing:2271048"
    // suggestion.innerHTML = suggestion.innerHTML + "<li>" + design_title + "<br><img class='design' src=" + design_img + "></li>\n";

    // // close ul element
    // suggestion.innerHTML = suggestion.innerHTML + "</ul>";


}


/* Load object thumbnail (either representative or random instance if multiple occurence) */
function load_image(object_name){
    var img = document.createElement("img");
    img.src = 'static/assets/images/object/' + name + "/" + object_name + '.png';
    img.name = object_name;
    img.classList.add('detected-object');
    img.setAttribute("onclick", "update_suggestion(this.name);");

    return img
}

var detection = document.getElementById("detection");

for(var i=0;i<objects.length;i++){
    detection.appendChild(load_image(objects[i]));
}

