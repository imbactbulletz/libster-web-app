var app = angular.module("libster-app");

app.config(function ($routeProvider) {

    $routeProvider
        .when("/", {
            templateUrl: "frontend/views/main.html"
        })
        .otherwise({
            redirectTo: "/"
        });
});