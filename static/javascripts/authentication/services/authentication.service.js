(function() {
    'use strict';

    angular
        .module('tracker.authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies','$http'];


    function Authentication($cookies, $http) {

        var Authentication = {
            login: login,
            register: register,
            logout: logout,
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate
        };

        return Authentication;

        function register(username, email, password) {
            return $http.post('/api/users/', {
                username: username,
                password: password,
                email: email
            }).then(regSuccess, regError);


            function regSuccess(data, status, headers, config) {
                Authentication.login(email, password);
                // window.location = '/';
            }

            function regError(data, status, headers, config) {
                return data['data']
            }
        }

        function login(email, password) {
            return $http.post('/auth/login/', {
                email: email,
                password: password
            }).then(loginSuccess, loginError);


            function loginSuccess(data, status, headers, config) {
                Authentication.setAuthenticatedAccount(data.data);
                window.location = '/trackers';
            }

            function loginError(data, status, headers, config) {
                return data['data']['message'];
            }
        }



        function logout() {
            return $http.post('/auth/logout/')
                .then(logoutSuccess, logoutError);

            function logoutSuccess(data, status, headers, config) {
                Authentication.unauthenticate();
                window.location = '/';
            }

            function logoutError(data, status, headers, config) {
                console.error(data);
            }
        }

        function getAuthenticatedAccount() {
            if (!$cookies.getObject('authenticatedAccount')) {
                return;
            }

            return $cookies.getObject('authenticatedAccount');
        }

        function isAuthenticated() {
            return !!$cookies.getObject('authenticatedAccount');
        }

        function setAuthenticatedAccount(account) {
            $cookies.putObject('authenticatedAccount', JSON.stringify(account));
        }

        function unauthenticate() {
            delete $cookies.remove('authenticatedAccount');
        }

    }
})();
