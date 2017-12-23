function checkPositive(arg) {
	if (arg < 0)
		throw new Error('arg must be positive');
	return true;
}

module.exports = checkPositive
