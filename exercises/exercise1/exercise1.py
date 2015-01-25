from __future__ import division
import scipy.stats as spst


#create class  LandAllocation()

class LandAllocation():
	""" Current class only applies to mean-variance utility 
	within choice of 2 crops. """
	
	def __init__(self,crop1,crop2,alpha,beta):
		"""enter crop info as 
		('distribution name used in scipy.stats', parameters separated by ',')
		The distribution name can be found in 
			http://docs.scipy.org/doc/scipy/reference/stats.html """		
		self.crop1=crop1	
		self.crop2=crop2
		self.alpha=alpha
		self.beta=beta
	
	# Obtain mean and variance from a given distribution.
	def mean_var(self, crop):
		return getattr(spst,crop[0]).stats(*crop[1:], moments = 'mv')
	
	# Calculate the optimal allocation between two crops.
	def best_allocation(self, crop1, crop2, alpha, beta):
		mean1, var1 = self.mean_var(crop1)
		mean2, var2 = self.mean_var(crop2)
		alloc1 = ((mean1-mean2)/beta+2*var2)/(2*var1+2*var2)
		alloc2 = 1-alloc1
		if alloc1 >= 0:
			if alloc2 >= 0:
				return (alloc1, alloc2)
			else:
				return (1, 0)
		else:
			return (0,1)
	
	# Calculate the optimal utility (from the optimal allocation).
	def utility(self, crop1,crop2, alpha, beta):
		t = self.best_allocation(crop1, crop2, alpha, beta)
		expect = t[0]*self.mean_var(crop1)[0] + t[1]*self.mean_var(crop2)[0]
		var = t[0]**2*self.mean_var(crop1)[1] + t[1]**2*self.mean_var(crop2)[1]
		return alpha*expect-beta*var
		
		
		
#simple test
crop1 = ['norm',2,3]
crop2 = ['bernoulli',0.1]
alpha = 1
beta = 0.5
result = LandAllocation(crop1, crop2, alpha, beta)
print("Crop 1 has a %s distribution with parameter %s."%(result.crop1[0], result.crop1[1:])) 
print("Crop 2 has a %s distribution with parameter %s."%(result.crop2[0], result.crop2[1:])) 
print("alpha = %s .   beta = %s ."%(result.alpha, result.beta))
print("The best allocation is: Crop1 %f; Crop2 %f."%(result.best_allocation(crop1, crop2, alpha, beta)))
print("The optimal utility is %f."%(result.utility(crop1, crop2, alpha, beta)))
