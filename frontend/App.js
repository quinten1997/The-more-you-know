<!DOCTYPE html>
<html>
<head>
    <title>Fun Facts App</title>
</head>
<body>
    <button onclick="getLocation()">Get Fun Fact</button>
    <p id="funFact"></p>

    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                document.getElementById("funFact").innerHTML = "Geolocation is not supported by this browser.";
            }
        }

        function showPosition(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            fetch(`http://127.0.0.1:5000/get_fun_fact?lat=${lat}&lon=${lon}`)
                .then(response => response.json())
                .then(data => {
                    if (data.fun_fact) {
                        document.getElementById("funFact").innerHTML = data.fun_fact;
                    } else {
                        document.getElementById("funFact").innerHTML = "No fun facts found.";
                    }
                })
                .catch(error => {
                    document.getElementById("funFact").innerHTML = "Error fetching fun fact.";
                });
        }
    </script>
</body>
</html>
