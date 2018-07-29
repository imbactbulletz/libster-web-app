var app = angular.module("libster-app");

app.controller('MainController', ['$scope', 'Service', '$location', '$rootScope', function ($scope, Service, $location, $rootScope) {

    $scope.addEntry = function () {
        $rootScope.presentEntries += 1; // uvecavamo broj prisutnih entry-ja na ekranu

        // dodaje entry
        $rootScope.entries[$rootScope.presentEntries] = {
            "prefix": $rootScope.tempEntry.prefix,
            "parameter": $rootScope.tempEntry.parameter,
            "operator": $rootScope.tempEntry.operator
        };


    };

    $scope.removeEntry = function (key) {

        delete $rootScope.entries[key];

    }
}]);