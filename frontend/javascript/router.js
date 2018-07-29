var app = angular.module("libster-app");

app.config(function ($routeProvider) {

    $routeProvider
        .when("/", {
            templateUrl: "frontend/views/main.html",
            controller: "MainController"
        })
        .otherwise({
            redirectTo: "/"
        });
});