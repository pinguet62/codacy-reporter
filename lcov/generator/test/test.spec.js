const first = require('../src/first')
const second = require('../src/second')

describe('test', () => {
	it('first', () => {
		first(42);
	})
	it('second', () => {
		second('direct');
	})
})
