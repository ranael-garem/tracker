var HttpClient = function() {
    this.get = function(Url, Callback) {
        var HttpRequest = new XMLHttpRequest();
        HttpRequest.onreadystatechange = function() { 
            if (HttpRequest.readyState == 4 && HttpRequest.status == 200)
                Callback(HttpRequest.responseText);
        }

        HttpRequest.open( "GET", Url, true );            
        HttpRequest.send( null );
    }
}

document.onreadystatechange = function () {
     if (document.readyState == "complete") {
     	Client = new HttpClient();
		Client.get('http://127.0.0.1:8000/load/1/', function(response) {
			console.log(response);
		});
   }
 }

window.onclick = function() {
    Client = new HttpClient();
	Client.get('http://127.0.0.1:8000/click/1/', function(response) {
		console.log(response);
	});
}
