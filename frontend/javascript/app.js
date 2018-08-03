var app = angular.module("libster-app", ["ngRoute", "ngMaterial", "md.data.table"]);

app.run(function ($rootScope, Service) {
    $rootScope.entries = {1: {}, 2: {}}; // predstavlja model koji sadrzi vrednost selektovanog prefiksa, parametar i selektovani logicki operator (skup ove 3 vrednosti smatram pod entry-jem)
    $rootScope.presentEntries = 2; // sadrzi podatak o tome koliko je entry-ja trenutno prisutno na ekranu
    $rootScope.tableVisible = false;

    $rootScope.tempEntry = {}; // predstavlja model za entry koji korisnik dodaje


    // Zovemo servis koji vraca prefikse a zatim te prefikse smestamo u rootScope.
    Service.getPrefixes().then(function (response) {
        $rootScope.availablePrefixes = response.data["prefixes"];


        // sortira prefikse leksikografski
        $rootScope.availablePrefixes.sort(function (first, second) {

            if (second["value"] > first["value"])
                return -1;

            if (second["value"] == first["value"])
                return 0;

            return 1;

        });
    });


});