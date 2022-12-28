// Smoke test is a regular load test, configured for minimal load. You want to run a smoke test as a sanity check every time you write a new script or modify an existing script.

// You want to run a smoke test to:
// --Verify that your test script doesn't have errors.
// --Verify that your system doesn't throw any errors when under minimal load.

// https://k6.io/docs/test-types/smoke-testing/



import http from 'k6/http';
import { check, group, sleep, fail } from 'k6';

export const options = {
  vus: 1, // 1 user looping for 1 minute
  duration: '1m',

  thresholds: {
    http_req_duration: ['p(99)<1500'], // 99% of requests must complete below 1.5s
  },
};

const BASE_URL = 'https://test-api.k6.io';
const USERNAME = 'TestUser';
const PASSWORD = 'SuperCroc2020';

export default () => {
  const loginRes = http.post(`${BASE_URL}/auth/token/login/`, {
    username: USERNAME,
    password: PASSWORD,
  });

  check(loginRes, {
    'logged in successfully': (resp) => resp.json('access') !== '',
  });

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${loginRes.json('access')}`,
    },
  };

  const myObjects = http.get(`${BASE_URL}/my/crocodiles/`, authHeaders).json();
  check(myObjects, { 'retrieved crocodiles': (obj) => obj.length > 0 });

  sleep(1);
};
