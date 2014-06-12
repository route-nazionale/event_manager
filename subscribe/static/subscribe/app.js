jQuery.event.props.push('dataTransfer');

var EventSubscribeApp = angular.module('EventSubscribeApp', ['ngRoute', 'ngTable', 'lvl.directives.dragdrop']);
EventSubscribeApp.config([
    '$routeProvider',
    function($routeProvider) {
        $routeProvider.
          when('/home', {
              templateUrl: '/static/subscribe/partials/events.html',
              controller: 'EventController'
          }).
          otherwise({
              redirectTo: '/home'
          });
    }]);
EventSubscribeApp.controller('EventController', [
    '$scope', '$http', '$filter', 'ngTableParams',
    function($scope, $http, $filter, ngTableParams) {
        $http.defaults.headers.post = {'X-CSRFToken': CSRF_TOKEN};
        $scope.events = [];
        $scope.order = 'name';
        $scope.alert = null;
        $scope.reverse = false;
        $scope.selectedEvent = null;

        $scope.findEvent = function(id) {
            for (var e in $scope.events) {
                var event = $scope.events[e];
                if (event.num === id) {
                    return event;
                }
            }
        };
        $scope.showAlert = function(title, message) {
            $scope.alert = {title: title, message: message};
        };
        $scope.closeAlert = function() {
            $scope.alert = null;
        };
        $scope.selectEvent = function(event) {
            $scope.selectedEvent = event;
        };
        $scope.reload = function() {
            $scope.table.reload();
        };
        $scope.getEventById = function(happening_id) {
            for (var e in $scope.events) {
                if ($scope.events[e].happening_id === happening_id) {
                    return $scope.events[e];
                }
            }
            return null;
        };
        $scope.districtFilter = '';
        $scope.heartbeatFilter = '';
        $scope.handicapFilter = '';
        $scope.chiefonlyFilter = '';
        $scope.notChiefonlyFilter = '';
        $scope.kindFilter = '';

        function customFilter(data){
                var filtered = [];
                var districtFilter = $scope.districtFilter;
                var heartbeatFilter = $scope.heartbeatFilter;
                var handicapFitler = $scope.handicapFilter;
                var chiefonlyFilter = $scope.chiefonlyFilter;
                var notChiefonlyFilter = $scope.notChiefonlyFilter;
                var kindFilter = $scope.kindFilter;
                if( !districtFilter 
                    && !heartbeatFilter 
                    && !handicapFitler 
                    && !chiefonlyFilter
                    && !notChiefonlyFilter
                    && !kindFilter ){
                    return data;
                }
                for( var d in data ){
                    if( districtFilter ){
                        if( data[d].district.match(new RegExp(districtFilter)) ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( heartbeatFilter ){
                        if( data[d].heartbeat && data[d].heartbeat.match(new RegExp(heartbeatFilter)) ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( handicapFitler ){
                        if( data[d].state_handicap === 'ENABLED' ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( chiefonlyFilter ){
                        if( data[d].state_chief === 'RESERVED' ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( notChiefonlyFilter ){
                        if( data[d].state_chief === 'DISABLED' ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( kindFilter ){
                        if( data[d].kind.match(new RegExp(kindFilter)) ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                }
                return filtered;
        }
        
        $scope.subscribe = function() {
        };

        $scope.edit = false;
        $scope.table = new ngTableParams({
                page: 1,
                count: 5, // 25 
                sorting: {name: 'asc'}
            }, {
                total: $scope.events.length,
                getData: function($defer, params) {
                    var data = $scope.events;
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

        $http.get('/events/').success(function(data) {
            $scope.events = data;
            $scope.table.reload();
        });
    }
]
  );
