def process_covariates(factor, value):
	if factor == 'allele_freq':
		return log(value)
	else:
		return value

def compute_survival(baseline, coef, data):
	return baseline*math.exp(coef*data)
