var tracker_id = 1;
var title = document.title
var url = window.location.href
var pathname = window.location.pathname


var HttpClient = function() {
    this.get = function(Url, Callback) {
        var HttpRequest = new XMLHttpRequest();
        HttpRequest.onreadystatechange = function() {
            if (HttpRequest.readyState == 4 && HttpRequest.status == 200)
                Callback(HttpRequest.responseText);
        }

        HttpRequest.open("GET", Url, true);
        HttpRequest.send(null);
    }
}


document.onreadystatechange = function() {
    Client = new HttpClient();

        if (window.location.href.indexOf("heatmapx") > -1) {
            var html = document.getElementsByTagName("HTML")[0];
            html.setAttribute("id", "heatmapContainer");

            Client.get('http://127.0.0.1:8000/reports/heatmap/' + tracker_id + '/' + pathname, function(response) {
                var heatmap = h337.create({
                    container: html,
                    maxOpacity: .6,
                    radius: 20,
                    blur: .90,
                    // backgroundColor with alpha so you can see through it
                    backgroundColor: 'rgba(0, 0, 58, 0)'
                });
                var clicks = JSON.parse(response).clicks;
                var dict = [];
                var x = 0;
                for (x in clicks) {
                    dict.push({ x: clicks[x][1], y: clicks[x][0], value: 100 })
                }
                var data = {
                    max: 10000,
                    min: 0,
                    data: dict,
                };
                heatmap.setData(data);
                heatmap.repaint();
                if (window.location.href.indexOf("heatmapxy") == -1) {
                    window.location.hash = window.location.hash + 'y';
                    window.location.reload();
                }
            });
        }
    else if (document.readyState == "complete") {
        Client.get('http://127.0.0.1:8000/load/' + tracker_id + '/' + pathname, function(response) {
            console.log(response);
        });

    }
}

window.onclick = function(e) {
    var x = e.layerX;
    var y = e.layerY;
    if (e.touches) {
        x = e.touches[0].pageX;
        y = e.touches[0].pageY;
    }
    Client = new HttpClient();
    Client.get('http://127.0.0.1:8000/click/' + tracker_id + '/' + x + '/' + y + '/' + pathname, function(response) {

    });
}