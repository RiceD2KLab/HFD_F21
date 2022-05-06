    var temptable = [[]];
    var risk;
    var insYear;
    var insStatus;
    var data;
        function readFile() {
            const myForm = document.getElementById("myForm");
            const csvFile = document.getElementById("csvFile");

            myForm.addEventListener("submit", function (e) {
                e.preventDefault();
                const input = csvFile.files[0];
                const reader = new FileReader();

                reader.onload = function (e) {
                    const text = e.target.result;
                    savetoTable(text);
                };
                reader.readAsText(input);
                alert("Success!");
            }); 
        }
        

        function savetoTable(str) {
            array = str.split("\r");
            array.shift();
            array.pop();
            count = 0;
            for (i = 0; i < array.length; i++) {
                var info = array[i].split(",");
                temptable[count] = info;
                count++;
            }
        }

        function Dist(Latitude, Longitude) {
            var scalar = Math.cos(Math.abs(Latitude * (2 * Math.PI) / 360));
            var dist = Math.sqrt(Math.pow(Latitude - myProp[0], 2) + Math.pow(Longitude - myProp[1], 2)) * scalar * lenEquator / 360;
            return dist;
        }

        function HeatMap() {
            const Prop = new google.maps.LatLng(29.756, -95.366);
            const map = new google.maps.Map(document.getElementById("map"), {
                center: Prop, 
                zoom: 10,
                mapTypeId: "satellite",
              });
            var points = [Prop];
            var risk = document.getElementById("risk").value;
            var insYear = document.getElementById("insYear").value;
            var insStatus = document.getElementById("insStatus").value;
            for (i = 0; i < temptable.length; i++) {
                if (temptable[i][34] >= risk) {
                    if (insYear == -1 || temptable[i][insYear] == 1) {
                        if (insStatus == -1 || temptable[i][1] == insStatus) {
                            var pp = new google.maps.LatLng(temptable[i][35], temptable[i][36]);
                            points.push(pp);
                        }
                    }
                }
            }
            var heatmap = new google.maps.visualization.HeatmapLayer({
                data: points
              });
            heatmap.set("radius", heatmap.get("radius") ? null : 20);
            heatmap.setMap(map);

        }

        function Search() {
            const Prop = new google.maps.LatLng(29.756, -95.366);
            var map = new google.maps.Map(document.getElementById("map"), {
                center: Prop, 
                zoom: 10,
                mapTypeId: "roadmap",
              });
            risk = document.getElementById("risk").value;
            insYear = document.getElementById("insYear").value;
            insStatus = document.getElementById("insStatus").value;

            for (i = 0; i < temptable.length; i++) {
                if (temptable[i][34] >= risk) {
                    if (insYear == -1 || temptable[i][insYear] == 1) {
                        if (insStatus == -1 || temptable[i][1] == insStatus) {
                            var myLatlng = new google.maps.LatLng(temptable[i][35], temptable[i][36]);
                            var marker = new google.maps.Marker({
                                position: myLatlng,
                                map: map,
                                title: "#incident: " + temptable[i][3] + "\n" + "#violation: " + temptable[i][4]
                            })
                        }
                    }
                }
            }
        }