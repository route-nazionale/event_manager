var RoverSubscribeApp = angular.module('RoverSubscribeApp', ['ngRoute', 'ngTable']);
RoverSubscribeApp.config([
    '$routeProvider',
    function($routeProvider) {
        $routeProvider.
                when('/home', {
                    templateUrl: '/static/subscribe/boys/partials/boys.html',
                    controller: 'SubscribtionController'
                }).
                otherwise({
                    redirectTo: '/home'
                });
    }]);


RoverSubscribeApp.controller('SubscribtionController', [
    '$scope', '$http', '$filter', 'ngTableParams',
    function($scope, $http, $filter, ngTableParams) {
        $scope.selectRover = function(rover){
            $scope.currentRover = rover;
        };
        $scope.saveRover = function(rover){
            alert('Che API si deve usare per salvare?');
        };
        
        $http.get('/events').success(function(events) {
            $scope.events = {};
            for( var e in events ){
                $scope.events[events[e].code] = events[e];
            }
        });
        $http.get('/boys').success(function(boys) {
            
            function customFilter(data){
                if( $scope.searchFilter ){
                    data = $filter('filter')(data, $scope.searchFilter);
                }
                if( !$scope.notFullBoys ){
                    return data;
                }
                var filtered = [];
                for( var d in data ){
                    if( !data[d].turno1 || !data[d].turno2 || !data[d].turno3 ){
                        filtered.push(data[d]);
                    }
                }
                return filtered;
            }
            
            $scope.boys = boys;

            $scope.table = new ngTableParams({
                page: 1,
                count: 25,
                sorting: {cognome: 'asc'}
            }, {
                total: $scope.boys.length,
                getData: function($defer, params) {
                    var data = $scope.boys;
                    var filteredData = customFilter(data);
                    var orderedData = params.sorting() ?
                            $filter('orderBy')(filteredData, params.orderBy()) :
                            filteredData;
                    var start = (params.page() - 1) * params.count();
                    var stop = params.page() * params.count();
                    var range = orderedData.slice(start, stop);
                    // params.total(range.length);
                    params.total(data.length);
                    $defer.resolve(range);
                }
            });
        });
    }
]);
