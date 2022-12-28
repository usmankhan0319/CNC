// While load testing is primarily concerned with performance assessment, and stress testing is concerned with system stability under extreme conditions, soak testing is concerned with reliability over a longer period of time.

// A soak test uncovers performance and reliability issues stemming from a system being under pressure for an extended period.


// https://k6.io/docs/test-types/soak-testing/



import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 400 }, // ramp up to 400 users
    // { duration: '3h56m', target: 400 }, // stay at 400 for ~4 hours
    { duration: '25m', target: 400 }, // stay at 400 for ~4 hours
    { duration: '2m', target: 0 }, // scale down. (optional)
  ],
};

const API_BASE_URL = 'https://test-api.k6.io';

export default function () {
  http.batch([
    ['GET', `${API_BASE_URL}/public/crocodiles/1/`],
    ['GET', `${API_BASE_URL}/public/crocodiles/2/`],
    ['GET', `${API_BASE_URL}/public/crocodiles/3/`],
    ['GET', `${API_BASE_URL}/public/crocodiles/4/`],
  ]);

  sleep(1);
}
