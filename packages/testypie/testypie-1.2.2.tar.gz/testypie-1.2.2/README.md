# Testypie

A test helper service that autogenerates your fixtures by recording real HTTP
requests in order to replay them.

The main advantage is that it is agnostic to what underlying HTTP library you
are using (or even what programming language you are using).

It works as a distinct proxy but can also be used as a library in Python tests,
e.g. combined with [HTTPretty](https://github.com/gabrielfalcao/HTTPretty).

## Usage

### Standalone

To run standalone (suitable for testing in any language):

```bash
$ pip install testypie
$ testypie
 * Serving Flask app "testypie" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Then run your tests with `HTTP_PROXY` set:

```bash
$ export HTTP_PROXY=http://127.0.0.1:5000
$ run-my-tests.sh # e.g. mocha mytests.js or pytest mytests.py
```

## How it works

Whether used as a proxy or as an intercept within Python tests, the idea is
that you follow the given workflow:

* Write unit tests that exercise your code without even attempting to mock
* Your code will result in an HTTP request that is allowed to happen over the
  real network _on first run only_
* A realistic fixture from this real request is stored in `$PWD/fixtures`
* On the next test run, testypie will respond with the fixture on disk rather
  than allow the real request to happen
* Now your tests work fine offline
* You are free to modify fixtures (see fixture format below) to make it replay
  an altered or stub version of the response
* At any time, you can delete individual or all fixtures to "refresh" them
  (e.g. if the upstream API changes) -- no need to maintain manual mocks to
  keep them aligned with upstreams


## Use cases and motivation

This project came out of writing tests for code in domains involving a lot of
data. For example, working with data from DBPedia or other large data sources.

With testypie, you can simply write tests pointing at real data URLs and
worry less about having to generate (and maintain) a collection of mocks, stubs
or full fixtures.

It is especially useful when using libraries that do HTTP under the hood, but
the precise HTTP library used is abstracted away from you, so it is difficult
to mock effectively. Examples of this are
[rdflib](https://github.com/RDFLib/rdflib) or
[boto](https://github.com/boto/boto3).

In the case of boto and AWS, testypie is useful in capturing exactly what boto
and AWS do and replaying it rather than having to reverse engineer a fairly
complex API so that you can mock it.

## Fixture Format

Fixtures are a model of the HTTP response (code, headers, body) serialised to
YAML files. The use of YAML was a deliberate choice such that the multiline
string support allows for a clear, intuitive way to capture the response body
exactly as it was (including all newlines) such that it can be easily edited.

Even in cases where an upstream responded with e.g. JSON with no newlines, you
are pretty to alter the fixture to respond instead with pretty-printed JSON
for easier editing.

The file names for fixtures are based on the HTTP method then a percent-encoded
form of the URL that was fetched. This both allows for different responses for
different methods (e.g. PUT vs. DELETE) and also keeps the file names
understandable enough such that it would be possible to generate fixtures up
front with a script (or manually).


## Limitations

The main limitation is the lack of mocking HTTPS in standalone mode. It works
fine when used as a helper library in Python though.

Additionally, fixtures are currently keyed against HTTP method and URL only, so
there is no way to temporarily mock a service to respond with e.g. HTTP 503 and
then mock is back to a healthy HTTP 200 response. For this use case, traditional
mocking may be more appropriate as testypie is focused on use cases where you
are mocking data sources or capturing more complex APIs (e.g. AWS APIs) where
recreating and maintaining mocks would be a lot of effort.

This also means that there is no support for content negotiation or other cases
where a response would vary according to request headers.
