var tracker_id;
var scripts = document.getElementsByTagName('script');
for (i = 0; i < scripts.length; i++) {
    if (scripts[i].src.indexOf('http://tracker.juniorgeorgy.webfactional.com/static/javascripts/transmitter.js') > -1) {
        tracker_id = scripts[i].src.replace(/^[^\?]+\??/, '').split('=')[1];
        break;
    }
}

var title = document.title
var url = window.location.href
var pathname = window.location.pathname

var max_scroll_height = 0;
var mouse_moves = [];
var invoke = false;

function invertInvoke() {
    invoke = !invoke;
}

var myVar = setInterval(function() { invertInvoke() }, 500);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var HttpClient = function() {
    this.get = function(Url, Callback) {
        var HttpRequest = new XMLHttpRequest();
        HttpRequest.onreadystatechange = function() {
            if (HttpRequest.readyState == 4 && HttpRequest.status == 200)
                Callback(HttpRequest.responseText);
        }

        HttpRequest.open("GET", Url, true);
        HttpRequest.setRequestHeader("Access-Control-Allow-Origin", "*");
        HttpRequest.setRequestHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        HttpRequest.send(null);
    }

    this.post = function(Url, Parameters, Callback) {
        var HttpRequest = new XMLHttpRequest();
        HttpRequest.onreadystatechange = function() {
            if (HttpRequest.readyState == 4 && HttpRequest.status == 200)
                Callback(HttpRequest.responseText);
        }

        HttpRequest.open("POST", Url, true);
        HttpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        var csrftoken = getCookie('csrftoken');
        HttpRequest.setRequestHeader("X-CSRFToken", csrftoken);
        HttpRequest.send("data=" + Parameters + "");
    }
}


function heatMapCanvas(clicks, body) {
    var heatmap = h337.create({
        container: body,
        maxOpacity: .6,
        radius: 20,
        blur: .90,
        // backgroundColor with alpha so you can see through it
        backgroundColor: 'rgba(0, 0, 58, 0)'
    });
    var dict = [];
    var x = 0;
    for (x in clicks) {
        dict.push({ x: clicks[x][1], y: clicks[x][0], value: 200 })
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
}

function mouseClickHeatMap() {
    var body = document.getElementsByTagName("BODY")[0];

    $.ajax({
        url: 'http://tracker.juniorgeorgy.webfactional.com/reports/heatmap/' + pathname + '/tracker_id' + '/' + tracker_id + '/',
        dataType: 'jsonp',
        success: function(response) {
            console.log(response);
            heatMapCanvas(response.clicks, body);
        },
        error: function(error) {
            // console.log(error);
            console.log(JSON.parse(error.responseText));
            heatMapCanvas(JSON.parse(error.responseText).clicks, body);
        }
    });
}

function screenShot() {
    setTimeout(function() {
        html2canvas(document.body, {
            allowTaint: 'false',
            onrendered: function(canvas) {
                var data = canvas.toDataURL();
                console.log(data);
                document.body.innerHTML = '';
                var img = document.createElement('img');
                img.id = "image";
                img.src = data;
                document.body.appendChild(img);
                // scrollHeatMap();
                Client = new HttpClient();
                Client.post('http://127.0.0.1:8000/reports/scroll/screenshot/', data, function(response) {
                    var data = JSON.parse(response);
                    pathname = pathname.substring(1, pathname.length)
                    tracker_id = String(tracker_id).replace('+', '');
                    window.location.href = 'http://127.0.0.1:8000/reports/scroll/heat/map/' + data.screenshot_id + '/' + tracker_id + '/' + pathname;
                })
            }
        });
    }, 2000);
}

function sendMouseMoves() {
    var movesToSend = mouse_moves;
    mouse_moves = [];
    var img = document.createElement("img");
    img.src = 'http://tracker.juniorgeorgy.webfactional.com/mouse/move/' + tracker_id + '/pathname/x' + pathname + '/href/' + window.location.href + '/coordinates/' + movesToSend;
    img.width = 1;
    img.height = 1;
    var html = document.getElementsByTagName("HTML")[0];
    html.appendChild(img);
}

document.onreadystatechange = function() {
    Client = new HttpClient();
    // console.log(document.referrer);
    if (document.readyState == "complete" && window.location.href.indexOf("heatmapx") > -1) {
        mouseClickHeatMap();
    } else if (document.readyState == "complete" && document.referrer.indexOf("/reports/scroll/heatmap/") > -1) {
        screenShot();

    } else if (document.readyState == "complete") {
        $.ajax({
            url: "http://ip-api.com/json/?fields=country,countryCode,regionName,city,query",
            dataType: 'jsonp',
            success: function(response) {
                var demographics = '/demographics/' + response.country + '/' + response.countryCode + '/' + response.city + '/' + response.regionName + '/' + response.query;
                var body = document.body,
                    html = document.documentElement;

                var height = Math.max(body.scrollHeight, body.offsetHeight,
                    html.clientHeight, html.scrollHeight, html.offsetHeight);
                console.log(height);
                var img = document.createElement("img");
                img.src = 'http://tracker.juniorgeorgy.webfactional.com/load/' + tracker_id + '/' + height + '/pathname/x' + pathname + demographics + '/' + navigator.language + '/href/' + window.location.href;
                img.width = 1;
                img.height = 1;
                var html = document.getElementsByTagName("HTML")[0];
                html.appendChild(img);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
}

window.onscroll = function() {
    scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    if (scroll_height > max_scroll_height) {
        max_scroll_height = scroll_height;
        // Client.get('http://127.0.0.1:8000/api/scroll/' + max_scroll_height + '/', function(response) {});
    }
}

window.onclick = function(e) {
    sendMouseMoves();
    var x = e.layerX;
    var y = e.layerY;
    if (e.touches) {
        x = e.touches[0].pageX;
        y = e.touches[0].pageY;
    }

    var img = document.createElement("img");
    img.src = 'http://tracker.juniorgeorgy.webfactional.com/click/' + tracker_id + '/' + x + '/' + y + '/pathname/x' + pathname + '/href/' + window.location.href;
    img.width = 1;
    img.height = 1;
    var html = document.getElementsByTagName("HTML")[0];
    html.appendChild(img);
}

window.onbeforeunload = function(e) {
    sendMouseMoves();
    // Client.get('http://127.0.0.1:8000/reports/scroll/' + tracker_id + '/' + pathname, function(response) {});
};

window.onmousemove = function(e) {
    if (mouse_moves.length == 200) {
        sendMouseMoves();
    }
    if (!invoke) {
        return;
    }
    var x = e.layerX;
    var y = e.layerY;
    mouse_moves.push(x + ',' + y);
}
