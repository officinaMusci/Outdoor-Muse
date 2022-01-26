import { useNavigate } from 'react-router-dom';


/**
 * The hook to interact with the backend API.
 * @returns {object} The functions of the hook.
 */
export default function useApi() {
  const navigate = useNavigate();

  // Checks if the user has to login again
  const checkAuth = response => {
    if ([401, 403].includes(response.status)) {
      sessionStorage.removeItem('outdoor_muse_jwt');
      navigate('/login');

      return false;
    }

    return true;
  }

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
    let token = sessionStorage.getItem('outdoor_muse_jwt');

    endpoint = 'http://127.0.0.1:5000' + endpoint;
    method = method.toUpperCase();

    let headers = {
      'Authorization': 'Bearer ' + token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    let request_input = {
      method: method,
      headers
    };

    let defaultResponse = {
      'result': defaultResult,
      'error': {
        'type': 'HTTPException',
        'message': 'API fetch failed'
      }
    };

    if (body && method === 'GET') {
      endpoint = endpoint + '/' + serialize(body);

    } else if (body) {
      request_input.body = JSON.stringify(body);
    }

    console.info(request_input);

    let apiResponse = await fetch(endpoint, request_input)
      .then(response => {
        if (checkAuth(response)) {
          return response.json().then(json => {
            console.info('API result:', json.result);
            return json.result;
          });
        
        } else {
          return defaultResponse;
        }
      })
      .catch(response => {
        console.error('API error:', response);
        return defaultResponse;
      });

    return apiResponse;
  };

  return { apiCall };
}