const fs = require('fs')
const parser = require('./node_modules/codacy-coverage/lib/impl/lcov')

let pathPrefix = ''
let lcovString = fs.readFileSync(process.argv[2]).toString()

parser
	.parse(pathPrefix, lcovString)
	.then(data => {
		data = JSON.stringify(data, null, 4);
		data = data.replace(/\\\\/g, '/');
		console.log(data);
	})
