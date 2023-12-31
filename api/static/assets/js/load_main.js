
/* Load image name */
var urlParams = new URLSearchParams(window.location.search);
// var image = urlParams.get('image');
document.getElementById("myImg").src = "static/assets/images/inference_output/" + image;

console.log(dictionary);

console.log(image);

var key_instruction = {
    "actuation-operation": "Designs that enable using different body parts or motions to operate objects, simplifying the process (e.g., using elbows instead of palms).",
    "actuation-reach": "Designs extending parts to access objects in inaccessible positions, assisting users in reaching items.",
    "constraint": "Designs preventing specific groups from accessing or operating objects (e.g., cabinet locks), useful for cognitive impairments or child-proof products.",
    "indication-visual": "Designs with clear visual cues aiding identification or function (e.g., labeled switches), particularly beneficial for those with sensory impairments.",
    "indication-tactile": "Similar to Indication-Visual, offering tactile feedback for users with visual impairments, aiding in identifying purpose or function through touch."
};

/* Load designs */
function load_design(design_element){

    var design_div = document.createElement('div');
    design_div.className = "design-element";
    design_div.style = "display: inline-block;"

    var a = document.createElement('a');
    a.href = design_element['design_url'];
    
    var img = document.createElement("img");
    img.src = design_element["image_url"];
    // img.src = "https://cdn.thingiverse.com/assets/2a/24/a1/7f/62/card_preview_90085844_211047486634488_3888945027983867904_n.jpg";
    img.classList.add('design-element');
    // img.setAttribute("onclick", 'window.open("'+designs[design_id]['design_url']+'"');
    img.onclick = document.getElementById('suggestion').scrollIntoView();
    a.appendChild(img);

    title = document.createElement('p');
    title.style = 'text-align: center; font-size: 15px; padding: -10px; width:100%; overflow:hidden;white-space:nowrap;text-overflow:ellipsis;';
    title.innerHTML = design_element['title'];

    design_div.appendChild(a);
    design_div.appendChild(title);

    return design_div;

}

/* Update suggestion upon clicking on object */
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
                key_div.innerHTML += key_instruction[key] + "<br>";

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

}


/* Load object thumbnail (either representative or random instance if multiple occurence) */
function load_image(object_name){
    var img_div = document.createElement('div');
    img_div.className = "detected-object"
    img_div.style = "display: inline-block;height:170px";
    var img = document.createElement("img");
    img.src = 'static/assets/images/object/' + image + "/" + object_name + '.png';
    img.name = object_name;
    img.classList.add('detected-object');
    img.setAttribute("onclick", "update_suggestion(this.name);");
    img.setAttribute("alt", object_name)

    title = document.createElement('p');
    title.style = 'text-align: center; font-size: 15px; padding: -10px;';
    title.innerHTML = object_name;

    img_div.appendChild(img);
    img_div.appendChild(title);
    return img_div
}

var detection = document.getElementById("detection");

for(var i=0;i<objects.length;i++){
    detection.appendChild(load_image(objects[i]));
}

