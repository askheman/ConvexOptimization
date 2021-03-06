import numpy as np, read_data, prob_grad, random
from scipy.optimize import check_grad

l = 10
data = read_data.read_train_sgd()

def func(params, *args):
#computes function value for a single example

	W, T = params[:26*129].reshape((26, 129)),\
		params[26*129:].reshape((26, 26))
	x, y = args[0]
	l = args[1]

	log_p = prob_grad.compute_log_p(x, y, W, T)
	
	return -1*log_p + 0.5*l*(\
		np.sum(np.square(W)) +\
		np.sum(np.square(T)))


def func_prime(params, *args):
#computes the derivative of a single example

	W, T = params[:26*129].reshape((26, 129)),\
		params[26*129:].reshape((26, 26))
	x, y = args[0]
	l = args[1]

	log_grad = np.zeros(26*129+26*26)

	l_gw, l_gt = log_grad[:26*129].reshape((26, 129)),\
	log_grad[26*129:].reshape((26, 26))

	#compute first part of objective
	np.multiply(prob_grad.log_p_wgrad(W, x, y, T), -1, out=l_gw)
	np.multiply(prob_grad.log_p_tgrad(T, x, y, W), -1, out=l_gt)

	#add regularizers
	np.add(log_grad, np.multiply(l, params), out=log_grad)

	return log_grad

#params = np.random.rand((26*129+26*26))
params = np.multiply(0.1, np.ones((26*129+26*26)))

print(check_grad(func, func_prime, params, random.choice(data), l))
