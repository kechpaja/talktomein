(function () {
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "checkbox") {
            inputs[i].addEventListener("change", function (e) {
                var input = e.target;

                var data = {
                    "name" : input.name,
                    "value" : input.checked
                };

                input.disabled = true;

                fetch("/account/update", {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }).then(function (response) {
                    if (!response.ok) {
                        // TODO error case
                        input.checked = !data["value"]
                    }

                    input.disabled = false;
                });
            });
        }
    }
})();
