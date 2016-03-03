(function () {
  'use strict';

  angular
    .module('tracker', [
      'tracker.config',
      'tracker.routes',
      'tracker.authentication'
    ]);

  angular
    .module('tracker.routes', ['ngRoute']);
  angular
  	.module('tracker.config', []);

angular
	.module('tracker')
	.run(run);

	run.$inject = ['$http'];

	/**
	* @name run
	* @desc Update xsrf $http headers to align with Django's defaults
	*/
	function run($http) {
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';
	}
})();
