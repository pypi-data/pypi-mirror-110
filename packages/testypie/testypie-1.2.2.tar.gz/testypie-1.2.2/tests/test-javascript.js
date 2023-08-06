const http = require('http');
const globalAgent = require('global-agent');
globalAgent.bootstrap();


function exampleFunctionNeedingTesting(callback) {
  return new Promise(function(resolve, reject) {
    http.get('http://dbpedia.org/data/Elephant.json', (resp) => {
      let data = '';

      // A chunk of data has been recieved.
      resp.on('data', (chunk) => {
        data += chunk;
      });

      // The whole response has been received. Print out the result.
      resp.on('end', () => {
        resolve(data.length);
      });

    }).on("error", (error) => {
      reject(error)
    });
  });
}


var assert = require('assert');

describe('Example', function() {
  it('should measure length of responses', function() {

    return exampleFunctionNeedingTesting()
      .then(function(length) {
        assert.equal(length, 59754);
      });

  });
});
