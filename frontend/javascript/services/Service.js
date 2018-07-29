var app = angular.module("libster-app");

app.factory('Service',['$http', function($http){
    var service = {};

    // Vraca sve prefikse sa backend-a
    service.getPrefixes = function(){
      return $http.get("http://localhost:5000/api/getPrefixes");
    };

    service.sendQuery = function(parameters){
      return $http({url:"http://localhost:5000/api/getBooks",
                    method: "GET",
                    params: parameters});
    };

    return service;
}]);