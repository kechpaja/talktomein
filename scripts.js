(function () {
    function addRemoveButton(row) {
        var removeButton = document.createElement("button");
        removeButton.className = "remove-button";
        removeButton.innerHTML = "-";
        removeButton.onclick = function () {
            row.parentElement.removeChild(row);
        };

        row.insertBefore(removeButton, row.childNodes[0]);

        // TODO extra borders, if we want them
    }

    var languageElements = document.getElementsByClassName("language");
    for (var i = 0; i < languageElements.length; i++) {
        addRemoveButton(languageElements[i].parentElement);
    }


    // Create and add the add language fields
    function createAddLanguageField(level, nextElement) {
        var row = document.createElement("tr");
        row.className = level;

        var button = document.createElement("button");
        button.innerHTML = "+";
        button.onclick = function () {
            var lang = document.getElementById("add" + level).value;

            var langtr = document.createElement("tr");
            langtr.id = lang;
            langtr.className = level;

            var inner = "<td class='left-column'>";
            if (level === "N") {
                inner += "&bigstar;";
            }
            inner += "</td><td class='language'>"+languages[lang]+"</td></tr>";
            langtr.innerHTML = inner;

            row.parentElement.insertBefore(langtr, row);
            addRemoveButton(langtr);
            
            // TODO remove selected language from selector?
        };

        var star = document.createElement("td");
        star.className = "left-column";
        if (level === "N") {
            star.innerHTML = "&bigstar;";
        }

        var field = document.createElement("td");
   //     field.innerHTML = "<input type='text' id='add" + level + "'></input>";

//        document.getElementById("add" + level).addEventListener(
 //           "keypress",
  //          function (e, msg) {
   //             if (e.keyCode == 13) {
    //                // TODO 
     //           }
      //  });

        // TODO wait on text field/autocomplete; just do selection list
        //
        var ddl = "<select id='add" + level + "'>";
        Object.keys(languages).forEach(function (l) {
            ddl += "<option value='" + l + "'>" + languages[l] + "</option>";
        });
        ddl += "</select>";
        field.innerHTML = ddl;

        row.appendChild(button);
        row.appendChild(star);
        row.appendChild(field);

       // var els = document.getElementsByClassName(level);
        
        //var table = document.getElementsByClassName("border")[0].parentElement;
        //if (nextElement) {
       //     table.insertBefore(row, nextElement);
       // } else {
       //     table.appendChild(row);
       // }
        return row;
    }

    var table = document.getElementsByTagName("tbody")[0];

    if (!table) {
        table = document.getElementsByTagName("table")[0];
    }

    table.appendChild(createAddLanguageField("A"));

    // B Languages
    var bRows = table.getElementsByClassName("B");
    if (bRows.length <= 0) {
        var border = document.createElement("tr");
        border.className = "border";
        border.innerHTML = "<td colspan='3'></td>";
        table.insertBefore(border, table.getElementsByClassName("A")[0]);
    }
    
    var borders = document.getElementsByClassName("border");
    table.insertBefore(createAddLanguageField("B"), borders[borders.length-1]);
    
    // C Languages
    var cRows = table.getElementsByClassName("C");
    if (cRows.length <= 0) {
        var border = document.createElement("tr");
        border.className = "border";
        border.innerHTML = "<td colspan='3'></td>";
        table.insertBefore(border, table.getElementsByClassName("B")[0]);
    }
    
    var borders = document.getElementsByClassName("border");
    table.insertBefore(createAddLanguageField("C"), borders[0]);

    // N Languages
    table.insertBefore(createAddLanguageField("N"), 
                       table.getElementsByClassName("C")[0]);
    



    //var c = document.getElementsByClassName("C");

    //createAddLanguageField("N", document.getElementsByClassName("C")[0]);
    //createAddLanguageField("C", document.getElementsByClassName("border")[0]);
    //createAddLanguageField("B", document.getElementsByClassName("border")[1]);
    //createAddLanguageField("A", document.getElementsByClassName("border")[2]);

   // ["N", "C", "B", "A"].forEach(function (level) {
   //     createAddLanguageField(level);
   // });

    // Add password field
    //var passwordField = document.createElement("div");
    //passwordField.innerHTML = "Password: <input type='text' id='pwd'></input>";
    //document.body.appendChild(passwordField);

    // Add save button
    var saveButton = document.createElement("button");
    saveButton.id = "save-button";
    saveButton.innerHTML = "Save changes"; // TODO localize?
    saveButton.onclick = function () {
        var langs = {};
        var elements = document.getElementsByClassName("language");
        for (var i = 0; i < elements.length; i++) {
            var row = elements[i].parentElement;
            langs[row.id] = row.className; // TODO does this work?
        }

        //var password = document.getElementById("pwd").value;

        fetch(user, {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(langs)
        }); // TODO error checking? 
    };

    document.body.appendChild(saveButton);

    // TODO stuff for flipping through list of languages and selecting one to add


})();
