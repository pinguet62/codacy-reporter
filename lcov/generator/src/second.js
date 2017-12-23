function doNothing(arg) {
	if (typeof arg === 'number') {
		console.log('1...');
		console.log('2...');
		console.log('3...');
		console.log('4...');
		console.log('5...');
	}
	console.log('Ok');
}

module.exports = doNothing
