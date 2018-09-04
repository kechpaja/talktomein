(function () {
    // Enable remove buttons
    function enableRemoveButton(button) {
        var row = button.parentElement;
        button.onclick = function () { 
            row.parentElement.removeChild(row); 
        };
    }

    var removeButtons = document.getElementsByClassName("remove-button");
    for (var i = 0; i < removeButtons.length; i++) {
        enableRemoveButton(removeButtons[i]);
    }


    // Enable add language fields
    var addButtons = document.getElementsByClassName("add-button");
    for (var i = 0; i < addButtons.length; i++) {
        var row = addButtons[i].parentElement;
        var level = row.className;
        addButtons[i].onclick = function () {
            var lang = document.getElementById("add" + level).value;

            var langtr = document.createElement("tr");
            langtr.id = lang;
            langtr.className = level;

            var inner = "<button class='remove-button'>-</button>";
            inner += "<td class='left-column'>" + (level==="N"?"&bigstar;":"");
            inner += "</td><td class='language'>"+languages[lang]+"</td></tr>";
            langtr.innerHTML = inner;

            row.parentElement.insertBefore(langtr, row);
            enableRemoveButton(langtr);
        };
    }


    // Enable save button
    document.getElementById("save-button").onclick = function () {
        var langs = {};
        var elements = document.getElementsByClassName("language");
        for (var i = 0; i < elements.length; i++) {
            var row = elements[i].parentElement;
            langs[row.id] = row.className; // TODO does this work?
        }

        fetch("/nyelv/update", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(langs)
        }); // TODO error checking? 
    };
})();
