
var boot = require('../app').boot,
  shutdown = require('../app').shutdown,
  port = require('../app').port,
  superagent = require('superagent'),
  expect = require('expect.js');

describe('server', function () {
  before(function () {
    boot();
  });
  describe('homepage', function(){
    it('should respond to GET',function(done){
      superagent
        .get('http://localhost:'+port)
        .end(function(res){
          expect(res.status).to.equal(200);
          done()
      })
    })
  });
  after(function () {
    shutdown();
  });
});

// var assert = require('chai').assert;
// var boot = require('../app').boot,
// 	shutdown = require('../app').shutdown,
// 	port  = require('../app').port,
// 	superagent  = require('superagent'),
// 	expect = require('expect.js');

// describe('server', function() {
// 	before(function (){
// console.info('TEST: Starting up test server...')
// 		boot();
// 	})
// 	describe('homepage', function(){
// 		it('should respond to GET',function(done){
// 			var target = 'http://localhost:' + port;
// console.info('TEST: Querying test server at: ' + target);
// 			superagent
// 			.get(target)
// 			.end(function(res) {
// console.info('response: ' + res);
// 				expect(res.status).to.equal(200);
// 				done();
// 			})
// 		});
// 		after(function(){
// 			shutdown();
// 		});
// 	});
// 	after(function(){
// console.info('TEST: Shutting down test server...')
// 		shutdown();
// 	});
// });
