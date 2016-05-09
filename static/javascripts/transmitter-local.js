var tracker_id = 1;
var scripts = document.getElementsByTagName('script');
// for (i = 0; i < scripts.length; i++) {
//     if (scripts[i].src.indexOf('http://127.0.0.1:8000/static/javascripts/transmitter.js') > -1) {
//         tracker_id = scripts[i].src.replace(/^[^\?]+\??/, '').split('=')[1];
//         break;
//     }
// }
// // <!-- Remove this when deployed 
// if (tracker_id == undefined){
//     tracker_id = 29;
// }
// //-->

var title = document.title;
var href = window.location.href;
var pathname = window.location.pathname;
var page_load_id = 0;
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


function mouseClickHeatMap() {
    var div = document.createElement('div');
    div.setAttribute("style", "background-color: white;");
    var html = document.getElementsByTagName("HTML")[0];
    var body = document.getElementsByTagName("BODY")[0];
    // body.setAttribute("id", "heatmapContainer");
    // div.innerHTML = '<header class="whitebar" style="background: #fff;">';
    // div.innerHTML += '<div class="row">'
    // div.innerHTML +=        '<div class="large-10 columns">'
    // div.innerHTML +=            '<div class="item choosed first"><a href="" class="overview">Overview</a></div>'
    // div.innerHTML +=            '<div class="item "><a href="/panel/heatmaps" class="heatmaps">Heatmaps</a></div>'
    // div.innerHTML +=        '</div>'
    // div.innerHTML +=    '</div>'
    // div.innerHTML +='</header>';
    // html.insertBefore(div, html.firstChild);
    Client.get('http://127.0.0.1:8000/reports/heatmap/' + tracker_id + '/' + pathname, function(response) {
        var heatmap = h337.create({
            container: body,
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
}

function mouseClickHeatMapDeployed() {
    var body = document.getElementsByTagName("BODY")[0];

    $.ajax({
        url: 'http://127.0.0.1:8000/reports/heatmap/' + pathname + '/tracker_id' + '/' + tracker_id + '/',
        dataType: 'jsonp',
        success: function(response) {
            console.log(response);
            heatMapCanvas(response.clicks, body);
        },
        error: function(error) {
            console.log(error);
            heatMapCanvas(JSON.parse(error.responseText).clicks, body);
        }
    });
}

function sendMouseMoves() {
    var movesToSend = mouse_moves;
    mouse_moves = [];
    // Client.post('http://127.0.0.1:8000/mouse/move/' + tracker_id + '/' + pathname, movesToSend, function(response) {

    // });
    var img = document.createElement("img");
    img.src = 'http://127.0.0.1:8000/mouse/move/' + tracker_id + '/pathname/x' + pathname + '/href/' + window.location.href + '/coordinates/' + movesToSend;
    img.width = 1;
    img.height = 1;
    var html = document.getElementsByTagName("HTML")[0];
    html.appendChild(img);
}

document.onreadystatechange = function() {
    Client = new HttpClient();
    // console.log(document.referrer);
    if (document.readyState == "complete" && window.location.href.indexOf("heatmapx") > -1) {
        mouseClickHeatMapDeployed();
    } else if (document.readyState == "complete" && document.referrer.indexOf("/reports/scroll/heatmap/") > -1) {
        // screenShot();

    } else if (document.readyState == "complete") {
        // screenShot();
        Client.get('http://ip-api.com/json/?fields=country,countryCode,regionName,city,query', function(response) {
            var data = JSON.parse(response);
            var demographics = '/demographics/' + data.country + '/' + data.countryCode + '/' + data.city + '/' + data.regionName + '/' + data.query;
            var body = document.body,
                html = document.documentElement;

            var height = Math.max(body.scrollHeight, body.offsetHeight,
                html.clientHeight, html.scrollHeight, html.offsetHeight);
            Client.get('http://127.0.0.1:8000/load/' + tracker_id + '/' + height + '/pathname/x' + pathname + demographics + '/' + navigator.language + '/href/' + window.location.href, function(response) {
                console.log(response);
                page_load_id = JSON.parse(response).page_load;
            });
        })



    }
}

window.onscroll = function() {
    scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    if (scroll_height > max_scroll_height) {
        max_scroll_height = scroll_height;
        Client.get('http://127.0.0.1:8000/api/scroll/' + max_scroll_height + '/', function(response) {});
    }
}

// window.onclick = function(e) {
//     sendMouseMoves();
//     var x = e.layerX;
//     var y = e.layerY;
//     if (e.touches) {
//         x = e.touches[0].pageX;
//         y = e.touches[0].pageY;
//     }
//     console.log(x,y);
//     // Client = new HttpClient();
//     // Client.get('http://127.0.0.1:8000/click/' + tracker_id + '/' + x + '/' + y + '/' + pathname, function(response) {

//     // });
//     var img = document.createElement("img");
//     img.src = 'http://127.0.0.1:8000/click/' + tracker_id + '/' + x + '/' + y  + '/pathname/x' + pathname + '/href/' + window.location.href;
//     img.width = 1;
//     img.height = 1;
//     var html = document.getElementsByTagName("HTML")[0];
//     html.appendChild(img);
// }
window.onclick = function(e) {
    sendMouseMoves();
    var coordinates = findDocumentCoords(e);
    x = coordinates[0];
    y = coordinates[1];
    var img = document.createElement("img");
    img.src = 'http://127.0.0.1:8000/click/' + tracker_id + '/' + x + '/' + y + '/pathname/x' + pathname + '/href/' + window.location.href;
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
    var coordinates = findDocumentCoords(e);
    x = coordinates[0];
    y = coordinates[1];
    mouse_moves.push(x + ',' + y);
}

function findDocumentCoords(mouseEvent) {
    var xpos
    var ypos;
    if (mouseEvent) {
        //FireFox
        xpos = mouseEvent.pageX;
        ypos = mouseEvent.pageY;
    } else {
        //IE
        xpos = window.event.x + document.body.scrollLeft - 2;
        ypos = window.event.y + document.body.scrollTop - 2;
    }

    return [xpos, ypos]
}
