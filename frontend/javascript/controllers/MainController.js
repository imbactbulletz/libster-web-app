var app = angular.module("libster-app");

app.controller('MainController', ['$scope', 'Service', '$location', '$rootScope', '$mdDialog', function ($scope, Service, $location, $rootScope, $mdDialog) {

    $scope.addEntry = function () {
        $rootScope.presentEntries += 1; // globalni counter - cisto radi jedinstvenog naziva za html i scope elemente

        // dodaje entry
        $rootScope.entries[$rootScope.presentEntries] = {
            "prefix": $rootScope.tempEntry.prefix,
            "parameter": $rootScope.tempEntry.parameter,
            "operator": $rootScope.tempEntry.operator
        };


    };


    $scope.removeEntry = function (key) {
        delete $rootScope.entries[key];
    };


    $scope.getBooks = function () {

        let clonedEntries = JSON.parse(JSON.stringify($rootScope.entries));

        delete clonedEntries[Object.keys(clonedEntries)[Object.keys(clonedEntries).length - 1]].operator;

        Service.getBooks(clonedEntries).then(function (response) {
            $rootScope.books = response.data;
            $rootScope.tableVisible = true;
        });
    };

    $scope.showAdvanced = function (ev,book) {

        $rootScope.prettyfied_book = JSON.stringify(book, undefined, 2);

        $mdDialog.show({
            controller: 'MainController',
            templateUrl: '/frontend/views/full_display_dialog.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
        })
    };

    $scope.cancelDialog = function() {
        $mdDialog.cancel();
    }
}]);