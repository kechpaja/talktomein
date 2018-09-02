(function () {
    var changes = [];

    function addLanguage(language) {
        if (changes[language] == "-") {
            delete changes[language];
        } else {
            changes[language] = "+";
        }
    }

    // TODO this and other functions should take into account whether or not
    // language already exists in user's list of languages. Maybe.
    function removeLanguage(language) {
        if (["A", "B", "C", "N"].indefOf(changes[language]) > -1) {
            delete changes[language];
        } else {
            changes[language] = "-";
        }
    }

    // TODO consider removing existing languages from list of choices. 
    // Put them back when they are removed.
    // TODO Alternatively, just send list of langs back to server, and sort it
    // out there. 


    // // TODO function to set up update page:
    // - Add extra borders between individual languages
    // - Possibly between native and fluent langs as well
    // - Add button to add another language after each group
    // - Add delete button to each language


    function setup() {
        // TODO add extra borders
        //
        
        var languageElements = document.getElementsByClassName("language");
        for (element in languageElements) {
            var row = element.parentElement;

            var removeButton = ""; // TODO create

            removeButton.onclick = function () {
                // TODO get language code of language to be removed
                var language = ""; // TODO (see above)
                removeLanguage(language);
                row.parentElement.removeChild(row);
            };

            row.insertBefore(removeButton, row.childNodes[0]);
        }


        // TODO create save button (which makes post request)
        // TODO sweep up languages
    }

    // TODO stuff for flipping through list of languages and selecting one to add


    setup();
})();
