var app = angular.module("libster-app", ["ngRoute", "ngMaterial"]);

app.run(function ($rootScope, Service) {
    // Zovemo servis koji vraca prefikse a zatim te prefikse smestamo u rootScope.
    Service.getPrefixes().then(function (response) {
        $rootScope.availablePrefixes = response.data;
    });

    var choice = {"name": "asdf"};
    var choiceSet = [];

    choiceSet.push(choice.name);
    choice.name = "Stefan";

    alert(choiceSet[0]);
});