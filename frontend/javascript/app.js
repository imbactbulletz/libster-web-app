var app = angular.module("libster-app", ["ngRoute", "ngMaterial"]);

app.run(function ($rootScope, Service) {
    // Zovemo servis koji vraca prefikse a zatim te prefikse smestamo u rootScope.
    Service.getPrefixes().then(function (response) {
        $rootScope.availablePrefixes = response.data;
    });

    $rootScope.entries = {}; // predstavlja model koji sadrzi vrednost selektovanog prefiksa, parametar i selektovani logicki operator (skup ove 3 vrednosti smatram pod entry-jem)
    $rootScope.presentEntries = 2; // sadrzi podatak o tome koliko je entry-ja trenutno prisutno na ekranu


    $rootScope.tempEntry = {}; // predstavlja model za entry koji korisnik dodaje
});