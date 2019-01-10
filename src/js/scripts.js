(function () {
    function updateDatabase(lang, speak, listen, read, write, then, orElse) {
        var langs = {
                        "language" : lang,
                        "speaking" : speak,
                        "listening" : listen,
                        "reading" : read,
                        "writing" : write
                    };

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
                then();
                //row.className = row.classList[0];
            } else {
                orElse();
                // TODO handle error response
            }
        });
    }

    function insertIndex(collection, item, getSortByText) {
        var array = [].slice.call(collection);
        array.push(item);
        array.sort(function (x, y) {
            return getSortByText(x).localeCompare(getSortByText(y));
        });
        return array.indexOf(item);
    }

    function removeRow(row) {
        row.parentElement.removeChild(row);

        var optrow = document.createElement("option");
        optrow.value = row.id;
        var content = row.getElementsByClassName("language")[0].textContent;
        optrow.innerHTML = content;

        var dropdown = document.getElementById("add");
        var index = insertIndex(dropdown.options, optrow, function (x) {
            return x.textContent;
        });

        if (index + 1 >= dropdown.options.length) {
            dropdown.appendChild(optrow);
        } else {
            dropdown.insertBefore(optrow, dropdown.options[index]);
        }
    }

    // Enable remove buttons
    function enableRemoveButton(button) {
        var row = button.parentElement.parentElement;
        var remove = function () {
            button.removeEventListener("click", remove);
            row.classList.add("unsaved");
            updateDatabase(row.id, null, null, null, null, function () {
                removeRow(row); 
            }, function () {
                button.addEventListener("click", remove);
                row.className = row.classList[0];
            });
        };

        button.addEventListener("click", remove);
    }

    var removeButtons = document.getElementsByClassName("remove-button");
    for (var i = 0; i < removeButtons.length; i++) {
        enableRemoveButton(removeButtons[i]);
    }

    // Enable add buttons
    function enableAddButton(button, before) {
        button.addEventListener("click", function () {
            var dropdown = document.getElementById("lang-selector");
            var lang = dropdown.value;
            var langname = dropdown.options[dropdown.selectedIndex].text;

            if (!lang) {
                return; // skip null element in selector
            }

            var levels = ["-", "|", "||", "|||", "||||", "|||||"];

            var speaking = document.getElementById("speaking-selector").value;
            var listening = document.getElementById("listening-selector").value;
            var reading = document.getElementById("reading-selector").value;
            var writing = document.getElementById("writing-selector").value;

            var row = document.createElement("tr");
            row.className = "unsaved";

            var ac = "<td class='language'>" + langname + "</td>";
            ac += "<td class='level l"+speaking+"'>"+levels[speaking] + "</td>";
            ac += "<td class='level l"+listening+"'>"+levels[listening]+"</td>";
            ac += "<td class='level l"+reading+"'>" + levels[reading] + "</td>";
            ac += "<td class='level l"+writing+"'>" + levels[writing] + "</td>";
            ac += "<td><button class='remove-button'>X</button></td></tr>";
            row.innerHTML = ac;

            // TODO sort list of languages?
            var addRow = document.getElementById("add-row");
            addRow.parentElement.insertBefore(row, addRow);

            enableRemoveButton(row.getElementsByClassName("remove-button")[0]);
            dropdown.removeChild(dropdown.options[dropdown.selectedIndex]);

            updateDatabase(lang, speaking, listening, reading, writing, 
                           function () { row.className = ""; }, 
                           function () { removeRow(row); });
        });
    }

    var addButton = document.getElementById("add-button");
    enableAddButton(addButton);
})();
