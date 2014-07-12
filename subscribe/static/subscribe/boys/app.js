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

RoverSubscribeApp.directive('ngAutocomplete', [function() {
        return function($scope, $element, $attrs) {
            $element.autocomplete({
                search: function() {
                    $element.autocomplete('close');
                },
                source: function(request, response) {
                    var sourceFunction = $scope[$attrs['ngAutocompleteSource']];
                    $element.trigger('autocomplete-started');
                    sourceFunction(request, function(data) {
                        $element.trigger('autocomplete-completed');
                        response(data);
                    });
                },
                select: function(event, ui) {
                    if ('ngAutocompleteCallback' in $attrs
                            && $attrs['ngAutocompleteCallback'] in $scope) {
                        $scope[$attrs['ngAutocompleteCallback']](ui.item);
                        $scope.$apply();
                    }
                }
            });
        };
    }]);

RoverSubscribeApp.controller('SubscribtionController', [
    '$scope', '$http', '$filter', 'ngTableParams',
    function($scope, $http, $filter, ngTableParams) {
        $scope.loadEvents = function() {
            $http.get('/events').success(function(events) {
                $scope.events = {};
                for (var e in events) {
                    $scope.events[events[e].code] = events[e];
                }
            });
        };
        $scope.cancelRover = function(){
            $scope.loadRovers();
        };
        $scope.customFilter = function(data) {
            if ($scope.searchFilter) {
                data = $filter('filter')(data, $scope.searchFilter);
            }
            if (!$scope.notFullBoys && !$scope.soddisfacimentoFilter) {
                return data;
            }
            var filtered = [];
            for (var d in data) {
                if ($scope.notFullBoys && ( !data[d].turno1 || !data[d].turno2 || !data[d].turno3 ) ) {
                    filtered.push(data[d]);
                    continue;
                }
                else if ($scope.soddisfacimentoFilter && data[d].soddisfacimento == $scope.soddisfacimentoFilter) {
                    filtered.push(data[d]);
                }
            }
            return filtered;
        };
        $scope.loadRovers = function() {
            $http.get('/boys').success(function(boys) {

                $scope.boys = boys;
                if (!angular.isDefined($scope.table)) {
                    $scope.table = new ngTableParams({
                        page: 1,
                        count: 25,
                        sorting: {cognome: 'asc'}
                    }, {
                        total: $scope.boys.length,
                        getData: function($defer, params) {
                            var data = $scope.boys;
                            var filteredData = $scope.customFilter(data);
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
                } else {
                    $scope.table.reload();
                }
            });
        };
        $scope.selectRover = function(rover) {
            $scope.currentRover = rover;
        };
        $scope.saveRover = function(rover) {
            $http.post('/validate-assignement', rover)
                    .success(function(resp) {
                        var msg = 'Validazione: "' + resp + '"\nProcedere?';
                        if (confirm(msg)) {
                            $http.post('/modifyBoy', rover)
                                    .success(function(resp) {
                                        alert('Salvataggio completato con successo');
                                    })
                                    .error(function(resp) {
                                        alert('Impossibile effettuare il salvataggio: ' + resp);
                                        $scope.cancelRover();
                                    });
                        }
                    })
                    .error(function() {
                        alert('Impossibile effettuare la validazione dei dati!');
                        $scope.cancelRover();
                    });
            ;
        };
        $scope.searchEvent = function(request, response) {
            var result = [];
            angular.forEach($scope.events, function(event) {
                if (event.name.match(new RegExp(request.term, 'i'))) {
                    result.push({
                        label: event.name + ' ('+event.seats_n_boys+'/'+event.max_boys_seats+')',
                        value: event.code
                    });
                }
            });
            response(result);
        };
        
        $scope.soddisfacimentoFilter = '';
        $scope.loadRovers();
        $scope.loadEvents();
    }
]);
