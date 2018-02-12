//The Model 
var locations = [
    {title: 'Philae Temple', location: { lat: 24.01266, lng: 32.87754 },id:0},
    {title: 'Aswan Museum',location: { lat:  24.085228, lng: 32.887001 },id:1},
    {title: 'Seheil Island', location: { lat: 24.061354, lng: 32.871902 },id:2}, 
    {title: 'Nubian Museum', location: { lat: 24.079425, lng: 32.889175 },id:3},
    {title: 'Elephantine Island', location: { lat: 24.085652, lng: 32.885574 },id:4}
];

// The view model that connect model to the view
var ViewModel = function() {
    var self = this;
    var markers = [];
    var largeInfowindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    // function calls populateinfowindow
    wikiinfo = function() {
        populateInfoWindow(this, largeInfowindow);
    };

    // When clicked in the li data in the view it calls this function
    // which calls wiki info window function
    // Toke this code from 
    // *https://github.com/EsraaQandel/Neighborhood-Map/blob/master/js/app.js#L49*
    self.query = ko.observable('');
    self.showMarker = function(clickeditem) {
        for (var i = 0; i < markers.length; i++) {
            if (markers[i].id == clickeditem.id) {
                populateInfoWindow(markers[i], largeInfowindow);
            }
        }
    };

    // Filter the data depends on the filter search and put it in finlist
    // Toke this code from  
    // *https://github.com/EsraaQandel/Neighborhood-Map/blob/master/js/app.js#L49*
    self.finList = ko.computed(function() {
        var search = self.query().toLowerCase();
        return ko.utils.arrayFilter(locations, function(item) {
            return item.title.toLowerCase().indexOf(search) >= 0;
        });
    });


    // Put the marker in the postions that are inside the fin list
    // then call wiki info window
    for (var i = 0; i < self.finList().length; i++) {
        var position = self.finList()[i].location;
        var title = self.finList()[i].title;
        var id = self.finList()[i].id;
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            id: i
        });
        markers.push(marker);
        marker.addListener('click', wikiinfo);
        bounds.extend(markers[i].position);
    } // end of markers


    map.fitBounds(bounds);

    // When click in the marker show a window which can redirct to wiki 
    // page to know more informations about the location
    function populateInfoWindow(marker, infowindow) {
        if (infowindow.marker != marker) {
            infowindow.marker = marker;
            var wikiRequestTimeout = setTimeout(function() {
                infowindow.setContent('<div id=' + marker.id + '>' + marker.title + '</div><p>Wikipedia Failed</p>');
            }, 2000);
            var wikiURL = "https://en.wikipedia.org/w/api.php?action=opensearch&search=" + marker.title + "&format=json&callback=wikiCallback";
            $.ajax({
                url: wikiURL,
                dataType: "jsonp",
                success: function(response) {
                    var list = response[1];
                    var link = "https://en.wikipedia.org/wiki/" + list[0];
                    infowindow.setContent('<div id=' + marker.id + '>' + marker.title + '</div><br/><a href="' + link + '" target="_blank">' +
                        'visit wikipedia for more info!</h1>');
                    clearTimeout(wikiRequestTimeout);
                }
            });
            infowindow.open(map, marker);

            if (marker.getAnimation() !== null) marker.setAnimation(null);

            else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
                setTimeout(function() {
                    marker.setAnimation(null);
                }, 2000);
            }

            infowindow.addListener('closeclick', function() {
                infowindow.setMarker = null;
            });
        }
    } // End of wiki info window

    // To filter the map depndes on the search
    self.filterMap = function() {
        for (var x = 0; x < markers.length; x++) {
            markers[x].setMap(null);
            for (var y = 0; y < self.finList().length; y++)
                if (markers[x].id == self.finList()[y].id)
                    markers[x].setMap(map);
        }
    };


}; // End of viewmodel


// Function renders the app
function initMap() {
    function loadMap(loadLocations) {
        map = new google.maps.Map(document.getElementById('map'), {
            center: {
                lat: 24.113193,
                lng: 32.920774
            },
            zoom: 13
        });
        loadLocations();
    }
    // load the locations 
    loadMap(function() {
        ko.applyBindings(new ViewModel());
    });
}

//Handle the map error
function mapError() {
    document.getElementById('map').innerHTML = "Error loading the map";
}


/* Functions for handling the animated nav*/

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.body.style.backgroundColor = "white";
}