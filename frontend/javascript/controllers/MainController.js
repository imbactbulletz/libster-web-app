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
        // smesta query u localStorage
        $scope.storeQuery();

        let clonedEntries = JSON.parse(JSON.stringify($rootScope.entries));

        delete clonedEntries[Object.keys(clonedEntries)[Object.keys(clonedEntries).length - 1]].operator;

        Service.getBooks(clonedEntries).then(function (response) {
            $rootScope.books = response.data;
            $rootScope.tableVisible = true;
        });
    };


    // dijalog koji sadrzi informacije o knjizi u  JSON formatu
    $scope.showFullInformation = function (ev, book) {

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

    // dijalog koji sadrzi informacije o istoriji upita
    $scope.showQueryHistory = function (ev) {
        $rootScope.queries_entered = [];

        Object.keys(localStorage).forEach(function(key){
            $rootScope.queries_entered.push({"name": key, "value": localStorage.getItem(key)});
        });

        $mdDialog.show({
            controller: 'MainController',
            templateUrl: '/frontend/views/query_history_dialog.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
        })
    };

    $scope.cancelDialog = function () {
        $mdDialog.cancel();
    };


    //localstorage operacije

    $scope.storeQuery = function () {
        var today = new Date();

        var min = today.getMinutes();
        var hh = today.getHours();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();


        if (dd < 10) {
            dd = '0' + dd
        }

        if (mm < 10) {
            mm = '0' + mm
        }


        $rootScope.queries_stored += 1;
        var query_name = yyyy + "/" + mm + "/" + dd + " - Unos " + $rootScope.queries_stored;

        localStorage.setItem(query_name, JSON.stringify($rootScope.entries))
    };

    $scope.setEntries = function(selectedEntries){
        $rootScope.entries = JSON.parse(selectedEntries);

        $scope.cancelDialog();
    };
}]);