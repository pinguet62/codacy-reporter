const fs = require('fs')
const parser = require('./node_modules/codacy-coverage/lib/impl/lcov')

let pathPrefix = ''
let lcovString = fs.readFileSync('coverage/lcov.info').toString()

parser
	.parse(pathPrefix, lcovString)
	.then(data => {
		data = JSON.stringify(data, null, 4);
		data = data.replace(/\\\\/g, '/');
		fs.writeFileSync('coverage/codacy.json', data);
	})
