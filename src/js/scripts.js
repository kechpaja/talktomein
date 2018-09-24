(function () {
    // Enable remove buttons
    function enableRemoveButton(button) {
        var row = button.parentElement.parentElement;
        button.onclick = function () { 
            row.parentElement.removeChild(row);

            var optrow = document.createElement("option");
            optrow.value = row.id;
            var content = row.getElementsByClassName("language")[0].textContent;
            optrow.innerHTML = content;
            document.getElementById("add").appendChild(optrow);

            document.getElementById("save-button").disabled = false;
        };
    }

    var removeButtons = document.getElementsByClassName("remove-button");
    for (var i = 0; i < removeButtons.length; i++) {
        enableRemoveButton(removeButtons[i]);
    }


    // Enable add buttons
    function enableAddButton(button, level, before) {
        button.onclick = function () {
            var dropdown = document.getElementById("add");
            var lang = dropdown.value;
            var langname = dropdown.options[dropdown.selectedIndex].text;

            if (!lang) {
                return; // skip null element in selector
            }

            var langtr = document.createElement("tr");
            langtr.id = lang;
            langtr.className = level;

            var inner = "<td class='level'>" + level + "</td>";
            inner += "<td class='language'>" + langname + "</td>";
            inner += "<td></td><td></td>"
            inner += "<td><button class='remove-button'>X</button></td></tr>";
            langtr.innerHTML = inner;

            var row = document.getElementsByClassName(before)[0];
            row.parentElement.insertBefore(langtr, row);
            var button = langtr.getElementsByClassName("remove-button")[0];
            enableRemoveButton(button);

            dropdown.removeChild(dropdown.options[dropdown.selectedIndex]);

            document.getElementById("save-button").disabled = false;
        };

    }

    var addButtons = document.getElementsByClassName("add-button");
    var levels = ["A", "B", "C"];
    var buttonBefores = ["add-row", "A", "B"];
    for (var i = 0; i < addButtons.length; i++) {
        enableAddButton(addButtons[i], levels[i], buttonBefores[i]);
    }


    // Enable save button
    document.getElementById("save-button").onclick = function () {
        var langs = {};
        var elements = document.getElementsByClassName("language");
        for (var i = 0; i < elements.length; i++) {
            var row = elements[i].parentElement;
            langs[row.id] = row.className; // TODO does this work?
        }

        fetch("/update", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(langs)
        }).then(function (response) {
            return response.json();
        }).then(function (jsonResponse) {
            if (jsonResponse["ok"]) {
                document.getElementById("save-button").disabled = true;
            } else {
                // TODO handle error response
            }
        });
    };
})();
