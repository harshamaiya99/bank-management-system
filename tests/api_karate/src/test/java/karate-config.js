function fn() {
  var config = {
    baseUrl: 'http://127.0.0.1:9000'
  };

  // 1. Execute the auth feature ONCE (Singleton pattern)
  // This prevents logging in 50 times if you have 50 scenarios.
  var result = karate.callSingle('classpath:examples/auth.feature', config);

  // 2. Create a global header object
  config.authHeader = { Authorization: 'Bearer ' + result.accessToken };

  return config;
}