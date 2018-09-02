(function () {
    // - Add button to add another language after each group

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

        fetch("update/" + user, {
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
