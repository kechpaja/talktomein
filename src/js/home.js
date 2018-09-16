(function () {
    "use strict";

    document.getElementById("newacct").addEventListener("click", function () {
        var buttons = document.getElementsByTagName("button");
        buttons[1].parentNode.removeChild(buttons[1]); // Remove new acct button
        buttons[0].innerHTML = "Submit";

        var input = document.createElement("input");
        input.type = "text";
        input.name = "email";
        input.placeholder = "Email";
        input.required = true; // TODO does this work?
        buttons[0].parentElement.insertBefore(input, buttons[0]);
    });
})();
