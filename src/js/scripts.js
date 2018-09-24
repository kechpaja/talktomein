(function () {
    function updateDatabase(language, level, then, orElse) {
        var langs = {"language" : language};
        if (level) {
            langs["level"] = level; //row.classList[0];
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
            updateDatabase(row.id, null, function () { 
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
    function enableAddButton(button, level, before) {
        button.onclick = function () {
            var dropdown = document.getElementById("add");
            var lang = dropdown.value;
            var langname = dropdown.options[dropdown.selectedIndex].text;

            if (!lang) {
                return; // skip null element in selector
            }

            var row = document.createElement("tr");
            row.id = lang;
            row.className = level + " unsaved";

            var inner = "<td class='level'>" + level + "</td>";
            inner += "<td class='language'>" + langname + "</td>";
            inner += "<td></td><td></td>"
            inner += "<td><button class='remove-button'>X</button></td></tr>";
            row.innerHTML = inner;

            var rows = document.getElementsByClassName(level);
            var index = insertIndex(rows, row, function (x) {
                return x.getElementsByClassName("language")[0].textContent;
            });

            var nextRow;
            if (index + 1 >= rows.length) {
                nextRow = document.getElementsByClassName(before)[0];
            } else {
                nextRow = document.getElementsByClassName(level)[index];
            }

            nextRow.parentElement.insertBefore(row, nextRow);

            // TODO add remove button only after element add is confirmed
            enableRemoveButton(row.getElementsByClassName("remove-button")[0]);
            dropdown.removeChild(dropdown.options[dropdown.selectedIndex]);

            updateDatabase(lang, level, function () {
                row.className = level;
            }, function () {
                // TODO after unsuccessful add
                // TODO remove element again, and re-add to option list
                removeRow(row);
            });
        };

    }

    var addButtons = document.getElementsByClassName("add-button");
    var levels = ["A", "B", "C"];
    var buttonBefores = ["add-row", "A", "B"];
    for (var i = 0; i < addButtons.length; i++) {
        enableAddButton(addButtons[i], levels[i], buttonBefores[i]);
    }
})();
