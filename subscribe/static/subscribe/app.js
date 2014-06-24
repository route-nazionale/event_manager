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



var userData = [
  {id:1,firstName:'Mary',lastName:'Goodman',role:'manager',approved:true,points:34},
  {id:2,firstName:'Mark',lastName:'Wilson',role:'developer',approved:true,points:4},
  {id:3,firstName:'Alex',lastName:'Davies',role:'admin',approved:true,points:56},
  {id:4,firstName:'Bob',lastName:'Banks',role:'manager',approved:false,points:14},
  {id:5,firstName:'David',lastName:'Stevens',role:'developer',approved:false,points:100},
  {id:6,firstName:'Jason',lastName:'Durham',role:'developer',approved:false,points:0},
  {id:7,firstName:'Jeff',lastName:'Marks',role:'manager',approved:true,points:8},
  {id:8,firstName:'Betty',lastName:'Abercrombie',role:'manager',approved:true,points:18},
  {id:9,firstName:'Krista',lastName:'Michaelson',role:'developer',approved:true,points:10},
  {id:11,firstName:'Devin',lastName:'Sumner',role:'manager',approved:false,points:3},
  {id:12,firstName:'Navid',lastName:'Palit',role:'manager',approved:true,points:57},
  {id:13,firstName:'Bhat',lastName:'Phuart',role:'developer',approved:false,points:314},
  {id:14,firstName:'Nuper',lastName:'Galzona',role:'admin',approved:true,points:94}
];




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

// -------------

        // init
        $scope.selectedA = [];
        $scope.selectedB = [];
        
        $scope.listA = userData.slice(0,5);
        $scope.listB = userData.slice(6,10);
        $scope.items = userData;
        
        $scope.checkedA = false;
        $scope.checkedB = false;
        
        function arrayObjectIndexOf(myArray, searchTerm, property) {
            for(var i = 0, len = myArray.length; i < len; i++) {
                if (myArray[i][property] === searchTerm) return i;
            }
            return -1;
        }
        
        $scope.aToB = function() {
            for (i in $scope.selectedA) {
            var moveId = arrayObjectIndexOf($scope.items, $scope.selectedA[i], "id"); 
            $scope.listB.push($scope.items[moveId]);
            var delId = arrayObjectIndexOf($scope.listA, $scope.selectedA[i], "id"); 
            $scope.listA.splice(delId,1);
            }
            reset();
        };
        
        $scope.bToA = function() {
            for (i in $scope.selectedB) {
            var moveId = arrayObjectIndexOf($scope.items, $scope.selectedB[i], "id"); 
            $scope.listA.push($scope.items[moveId]);
            var delId = arrayObjectIndexOf($scope.listB, $scope.selectedB[i], "id"); 
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
            }
            else {
            for (i in $scope.listA) {
                $scope.selectedA.push($scope.listA[i].id);
            }
            }
        }
        
        $scope.toggleB = function() {
            
            if ($scope.selectedB.length>0) {
            $scope.selectedB=[];
            }
            else {
            for (i in $scope.listB) {
                $scope.selectedB.push($scope.listB[i].id);
            }
            }
        }
        
        $scope.drop = function(dragEl, dropEl, direction) {
            
            var drag = angular.element(dragEl);
            var drop = angular.element(dropEl);
            var id = drag.attr("data-id");
            var el = document.getElementById(id);
            
            if(!angular.element(el).attr("checked")){
            angular.element(el).triggerHandler('click');
            }
            
            direction();
            $scope.$digest();
        };
  




    }
]
  );
