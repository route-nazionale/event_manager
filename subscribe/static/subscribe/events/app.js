jQuery.event.props.push('dataTransfer');

var EventSubscribeApp = angular.module('EventSubscribeApp', ['ngRoute', 'ngTable', 'lvl.directives.dragdrop']);
EventSubscribeApp.config([
    '$routeProvider',
    function($routeProvider) {
        $routeProvider.
          when('/home', {
              templateUrl: '/static/subscribe/events/partials/events.html',
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
        $scope.createNew = function() {
            $scope.selectedEvent = {
                seats_n_boys: 0,
                seats_n_chiefs: 0,
                state_chief: 'ENABLED',
                state_handicap: 'ENABLED',
                min_age: 1,
                max_age: 99,
                max_boys_seats: 30,
                max_chiefs_seats: 5,
                state_activation: 'CREATING',
                state_subscription: 'OPEN',
                topic: $scope.topics[0],
                district: $scope.districts[0],
                timeslot: $scope.timeslots[0],
                kind: 'LAB'
            };
            $scope.edit = true;
            $scope.isNew = true;
            $scope.editCapiSpalla = false;
            $scope.listA = [];
            $scope.listB = [];
            $scope.items = []; 
        };
        $scope.selectEvent = function(event) {
            $scope.selectedEvent = angular.copy(event);
            var name = $scope.selectedEvent.name.split(' - ')[1];
            $scope.selectedEvent.name = name.split(' - ')[1];
            if (!$scope.selectedEvent.name) {
                $scope.selectedEvent.name = name;
            }
            $scope.edit = false;
            $scope.isNew = false;
            $scope.editCapiSpalla = false;

            $http.get('/chiefs/').success(function(data) {
                $scope.items = data;
                $scope.listA = angular.copy(data);
                $scope.listB = [];
                $http.get('/subscribedChiefs/' + $scope.selectedEvent.id).success(function(data) {
                    $scope.listB = _.filter($scope.items, function(x) { return data.indexOf(x.code) != -1; });
                    $http.get('/freeChiefs/' + $scope.selectedEvent.id).success(function(data) {
                        $scope.listA = _.filter($scope.items, function(x) { return data.indexOf(x.code) != -1; });
                    });
                });
            });

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
        $scope.printcodeFilter = '';
        $scope.handicapFilter = '';
        $scope.chiefonlyFilter = '';
        $scope.notChiefonlyFilter = '';
        $scope.kindFilter = '';

        function customFilter(data){
                var filtered = [];
                var districtFilter = $scope.districtFilter;
                var heartbeatFilter = $scope.heartbeatFilter;
                var printcodeFilter = $scope.printcodeFilter;
                var handicapFitler = $scope.handicapFilter;
                var chiefonlyFilter = $scope.chiefonlyFilter;
                var notChiefonlyFilter = $scope.notChiefonlyFilter;
                var kindFilter = $scope.kindFilter;
                if( !districtFilter 
                    && !printcodeFilter
                    && !heartbeatFilter 
                    && !handicapFitler 
                    && !chiefonlyFilter
                    && !notChiefonlyFilter
                    && !kindFilter ){
                    return data;
                }
                for( var d in data ){
                    if( printcodeFilter ){
                        if (! data[d].print_code.match(new RegExp(printcodeFilter,'i'))){
                            continue
                        }
                    }

                    if( districtFilter ){
                        if(!data[d].district.match(new RegExp(districtFilter,'i'))){
                            continue;
                        }
                    }
                    if( heartbeatFilter ){
                        if(!data[d].heartbeat || !data[d].heartbeat.match(new RegExp(heartbeatFilter,'i')) ){
                            continue;
                        }
                    }
                    if( handicapFitler ){
                        if(! data[d].state_handicap === 'ENABLED' ){
                            continue;
                        }
                    }
                    if( chiefonlyFilter ){
                        if( ! data[d].state_chief === 'RESERVED' ){
                            continue;
                        }
                    }
                    if( notChiefonlyFilter ){
                        if( ! data[d].state_chief === 'DISABLED' ){
                            continue;
                        }
                    }
                    if(kindFilter ){
                        if( ! data[d].kind.match(new RegExp(kindFilter,'i')) ){
                            continue;
                        }
                    }
                    
                    filtered.push(data[d]);
                }
                return filtered;
        }
        
        $scope.editForm = function() {
            $scope.edit = true;
            $scope.selectedEvent = angular.copy($scope.selectedEvent);
            $scope.old = angular.copy($scope.selectedEvent);
        };
        $scope.cancelEdit = function() {
            $scope.edit = false;
            $scope.selectedEvent = $scope.old;
        };
        $scope.save = function() {
            if ($scope.isNew) {
                $http.post('/createEvent', $scope.selectedEvent).success(function(data) {
                    // reload
                    $http.get('/events/').success(function(data) {
                        $scope.events = data;
                        $scope.table.reload();
                    });
                });
            } else {
                $http.post('/storeEvent', $scope.selectedEvent).success(function(data) {
                    // reload
                    $http.get('/events/').success(function(data) {
                        $scope.events = data;
                        $scope.table.reload();
                    });
                });
            }
        };
        $scope.edit = false;
        $scope.table = new ngTableParams({
                page: 1,
                count: 25, 
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
        $scope.capiSpalla = function() {
            $scope.editCapiSpalla = true;
        };

        $scope.closeCapiSpalla = function() {
            $scope.editCapiSpalla = false;
        };

        $http.get('/events/').success(function(data) {
            $scope.events = data;
            $scope.table.reload();
        });

        $http.get('/districts/').success(function(data) {
            $scope.districts = data;
        });
        
        $http.get('/timeslots/').success(function(data) {
            $scope.timeslots = data;
        });
        
        $http.get('/topics/').success(function(data) {
            $scope.topics = data;
        });

        // ----------------------------------------------------------------------------------------------
        // selezione capi

        $scope.selectedA = [];
        $scope.selectedB = [];
        $scope.checkedA = false;
        $scope.checkedB = false;

        $scope.listA = []; // not subscribed chiefs
        $scope.listB = []; // subscribed chiefs
        $scope.items = []; // chiefs list

        function arrayObjectIndexOf(myArray, searchTerm, property) {
            for(var i = 0, len = myArray.length; i < len; i++) {
                if (myArray[i][property] === searchTerm) return i;
            }
            return -1;
        }

        $scope.addChief = function() {
            var cb = function(data) {};
            for (var i in $scope.selectedA) {
                $http.get('/event/' + $scope.selectedEvent.id + '/subscribe/' + $scope.selectedA[i]).success(cb);
                var moveId = arrayObjectIndexOf($scope.items, $scope.selectedA[i], "code"); 
                $scope.listB.push($scope.items[moveId]);
                var delId = arrayObjectIndexOf($scope.listA, $scope.selectedA[i], "code"); 
                $scope.listA.splice(delId,1);
            }
            reset();
        };

        $scope.removeChief = function() {
            var cb = function(data) {};
            for (var i in $scope.selectedB) {
                $http.get('/event/' + $scope.selectedEvent.id + '/unsubscribe/' + $scope.selectedB[i]).success(cb);
                var moveId = arrayObjectIndexOf($scope.items, $scope.selectedB[i], "code"); 
                $scope.listA.push($scope.items[moveId]);
                var delId = arrayObjectIndexOf($scope.listB, $scope.selectedB[i], "code"); 
                $scope.listB.splice(delId,1);
            }
            reset();
        };

        function reset(){
            $scope.selectedA=[];
            $scope.selectedB=[];
            $scope.toggle=0;
        }

        $scope.toggleA = function() {
            if ($scope.selectedA.length>0) {
                $scope.selectedA=[];
            } else {
                for (var i in $scope.listA) {
                    $scope.selectedA.push($scope.listA[i].code);
                }
            }
        };

        $scope.toggleB = function() {
            if ($scope.selectedB.length>0) {
                $scope.selectedB=[];
            } else {
                for (var i in $scope.listB) {
                    $scope.selectedB.push($scope.listB[i].code);
                }
            }
        };

        $scope.drop = function(dragEl, dropEl, direction) {
            var drag = angular.element(dragEl);
            var drop = angular.element(dropEl);
            var id = drag.attr("data-id");
            var el = document.getElementById(id);

            if (!angular.element(el).attr("checked")){
                angular.element(el).triggerHandler('click');
            }

            direction();
            $scope.$digest();
        };

    }
]);
