import { useContext } from 'react';

import { AuthContext } from './authContext';
import { tokenName } from '../settings';


/**
 * The hook to interact with the backend API.
 * @returns {object} The functions of the hook.
 */
export default function useApi() {
  const [, setIsAuthenticated] = useContext(AuthContext);

  // Encodes an object in a query string
  const serialize = obj => {
    var str = [];
    for (var p in obj)
      if (obj.hasOwnProperty(p)) {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
    return str.join("&");
  }

  /**
   * Returns the response for a backend API call.
   * @param {string} endpoint The endpoint for the API request.
   * @param {string} method The HTTP method to use.
   * @param {object} body The body of the request.
   * @returns {object} The backend response.
   */
  const apiCall = async (endpoint, method, body, defaultResult=[]) => {
    endpoint = 'http://127.0.0.1:5000' + endpoint;
    method = method.toUpperCase();

    let headers = {
      'Authorization': 'Bearer ' + sessionStorage.getItem(tokenName),
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    let request_input = {
      method: method,
      headers
    };

    if (body && method === 'GET') {
      endpoint = endpoint + '/' + serialize(body);

    } else if (body) {
      request_input.body = JSON.stringify(body);
    }

    console.info(
      'API endpoint:\n',
      endpoint,
      '\nAPI request:\n',
      request_input
    );

    let apiResponse = await fetch(endpoint, request_input)
      .then(response => {
        if (response.ok) {
          return response.json().then(json => {
            console.info('API result:', json);
            return json;
          });
        
        } else {
          throw new Error(response.status);
        }
      })
      .catch(error => {
        error = String(error).replace('Error: ', '');

        if (error === '401') {
          setIsAuthenticated(false);
        }

        return {
          'result': defaultResult,
          'error': {
            'type': 'HTTPException',
            'message': 'API fetch failed'
          }
        };
      });

    return apiResponse;
  };

  return { apiCall };
}