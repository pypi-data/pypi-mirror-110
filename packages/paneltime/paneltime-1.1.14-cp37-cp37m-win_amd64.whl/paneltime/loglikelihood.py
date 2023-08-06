#!/usr/bin/env python
# -*- coding: utf-8 -*-

#contains the log likelihood object
import sys
#sys.path.append(__file__.replace("paneltime\\loglikelihood.py",'build\\lib.win-amd64-3.5'))
#sys.path.append(__file__.replace("paneltime\\loglikelihood.py",'build\\lib.linux-x86_64-3.5'))
try:#only using c function if installed
	import cfunctions as c
except ImportError as e:
	c=None
import numpy as np
import functions as fu
import calculus_functions as cf
import stat_functions as stat
import random_effects as re
from scipy import sparse as sp
import scipy
import debug
import traceback
import model_parser


	

class LL:
	"""Calculates the log likelihood given arguments arg (either in dictonary or array form), and creates an object
	that store dynamic variables that depend on the \n
	If args is a dictionary, the ARMA-GARCH orders are 
	determined from the dictionary. If args is a vector, the ARMA-GARCH order needs to be consistent
	with the  panel object
	"""
	def __init__(self,args,panel,constraints=None,print_err=False):
		self.err_msg=''
		self.errmsg_h=''
		self.panel=panel
		
		#checking settings. If fixed_random_pre_ARIMA, the FE/RE is done on the data before LL
		gfre=panel.options.fixed_random_group_eff.value
		tfre=panel.options.fixed_random_time_eff.value
		vfre=panel.options.fixed_random_variance_eff.value
		
		self.re_obj_i=re.re_obj(panel,True,panel.T_i,panel.T_i,gfre)
		self.re_obj_t=re.re_obj(panel,False,panel.date_count_mtrx,panel.date_count,tfre)
		self.re_obj_i_v=re.re_obj(panel,True,panel.T_i,panel.T_i,gfre*vfre)
		self.re_obj_t_v=re.re_obj(panel,False,panel.date_count_mtrx,panel.date_count,tfre*vfre)
		
		self.LL_const=-0.5*np.log(2*np.pi)
		
		self.args=panel.args.create_args(args,panel,constraints)
		self.h_err=""
		self.LL=None
		#self.LL=self.LL_calc()
		try:
			self.LL=self.LL_calc()
			if np.isnan(self.LL):
				self.LL=None						
		except Exception as e:
			if print_err:
				traceback.print_exc()
				print(self.errmsg_h)
		
		


	def LL_calc(self):
		panel=self.panel
		X=panel.XIV
		matrices=set_garch_arch(panel,self.args.args_d)
		if matrices is None:
			return None		
		
		AMA_1,AMA_1AR,GAR_1,GAR_1MA=matrices
		(N,T,k)=X.shape
		#Idea for IV: calculate Z*u throughout. Mazimize total sum of LL. 
		u = panel.Y-cf.dot(X,self.args.args_d['beta'])
		if panel.options.fixed_random_pre_ARIMA.value:
			u_RE = (u+self.re_obj_i.RE(u)+self.re_obj_t.RE(u))*panel.included[3]
			e_RE = cf.dot(AMA_1AR,u_RE)
			e=e_RE
			lnv_ARMA = self.garch(GAR_1MA, e_RE)
		else:
			u_RE=None
			e = cf.dot(AMA_1AR,u)
			e_RE = (e+self.re_obj_i.RE(e)+self.re_obj_t.RE(e))*panel.included[3]
			if panel.options.fixed_random_in_GARCH.value:
				lnv_ARMA = self.garch(GAR_1MA, e_RE)
			else:
				lnv_ARMA = self.garch(GAR_1MA, e)			
		e_REsq = e_RE**2
		W_omega = cf.dot(panel.W_a, self.args.args_d['omega'])
		lnv = W_omega+lnv_ARMA# 'N x T x k' * 'k x 1' -> 'N x T x 1'
		#self.lnv0=lnv*1#debug
		grp = self.variance_RE(e_REsq)#experimental
		lnv+=grp
		self.dlnv_pos=(lnv<100)*(lnv>-100)
		lnv = np.maximum(np.minimum(lnv,100),-100)
		v = np.exp(lnv)*panel.a[3]
		v_inv = np.exp(-lnv)*panel.a[3]

		LL = self.LL_const-0.5*(lnv+(e_REsq)*v_inv)
		#self.LL_array=LL#debug
		self.tobit(panel,LL)
		LL=np.sum(LL*panel.included[3])
			
		self.add_variables(matrices, u, e, lnv_ARMA, lnv, v, W_omega, grp,e_RE,u_RE,e_REsq,v_inv)
		if abs(LL)>1e+100: 
			return None				
		return LL
		
	def add_variables(self,matrices,u,e,lnv_ARMA,lnv,v,W_omega,grp,e_RE,u_RE,e_REsq,v_inv):
		self.v_inv05=v_inv**0.5
		self.e_norm=e_RE*self.v_inv05	
		self.e_norm_centered=(self.e_norm-self.panel.mean(self.e_norm))*self.panel.included[3]
		self.AMA_1,self.AMA_1AR,self.GAR_1,self.GAR_1MA=matrices
		self.u,self.e, self.lnv_ARMA        = u,         e,       lnv_ARMA
		self.lnv,self.v                     = lnv,       v
		self.W_omega=W_omega
		self.grp=grp
		self.e_RE=e_RE
		self.u_RE=u_RE
		self.e_REsq=e_REsq
		self.v_inv=v_inv


	
	def tobit(self,panel,LL):
		if sum(panel.tobit_active)==0:
			return
		g=[1,-1]
		self.F=[None,None]	
		for i in [0,1]:
			if panel.tobit_active[i]:
				I=panel.tobit_I[i]
				self.F[i]= scipy.stats.norm.cdf(g[i]*self.e_norm[I])
				LL[I]=np.log(self.F[i])

	def garch(self,GAR_1MA,e):
		if self.panel.pqdkm[4]>0:
			if self.panel.z_active:
				h_res=self.h(e, self.args.args_d['z'][0])
			else:
				h_res=self.h(e, None)
			(self.h_val,     self.h_e_val,
			 self.h_2e_val,  self.h_z_val,
			 self.h_2z_val,  self.h_ez_val)=[cf.prod((i,self.panel.included[3])) for i in h_res]
			return cf.dot(GAR_1MA,self.h_val)
		else:
			(self.h_val,    self.h_e_val,
			 self.h_2e_val, self.h_z_val,
			 self.h_2z_val, self.h_ez_val,
			 self.avg_h)=(0,0,0,0,0,0,0)
			return 0			
	
	def variance_RE(self,e_REsq):
		"""Calculates random/fixed effects for variance."""
		panel=self.panel
		self.vRE,self.lnvRE,self.dlnvRE=panel.zeros[3],panel.zeros[3],panel.zeros[3]
		self.ddlnvRE,self.dlnvRE_mu,self.ddlnvRE_mu_vRE=panel.zeros[3],None,None
		self.varRE_input, self.ddvarRE_input, self.dvarRE_input = None, None, None
		if panel.options.fixed_random_variance_eff.value==0:
			return panel.zeros[3]
		if panel.N==0:
			return None

		meane2=panel.mean(e_REsq)
		self.varRE_input=(e_REsq-meane2)*panel.included[3]

		mine2=0
		mu=panel.options.variance_RE_norm.value
		self.vRE_i=self.re_obj_i_v.RE(self.varRE_input)
		self.vRE_t=self.re_obj_t_v.RE(self.varRE_input)
		self.meane2=meane2
		vRE=meane2*panel.included[3]-self.vRE_i-self.vRE_t
		self.vRE=vRE
		small=vRE<=mine2
		big=small==False
		vREbig=vRE[big]
		vREsmall=vRE[small]

		lnvREbig=np.log(vREbig+mu)
		lnvREsmall=(np.log(mine2+mu)+((vREsmall-mine2)/(mine2+mu)))
		lnvRE,dlnvRE,ddlnvRE=np.zeros(vRE.shape),np.zeros(vRE.shape),np.zeros(vRE.shape)
		
		lnvRE[big]=lnvREbig
		lnvRE[small]=lnvREsmall
		self.lnvRE=lnvRE*panel.included[3]

		dlnvRE[big]=1/(vREbig+mu)
		dlnvRE[small]=1/(mine2+mu)
		self.dlnvRE=dlnvRE*panel.included[3]
		
		ddlnvRE[big]=-1/(vREbig+mu)**2
		self.ddlnvRE=ddlnvRE*panel.included[3]
	
		return self.lnvRE
		


	def standardize(self,reverse_difference=False):
		"""Adds X and Y and error terms after ARIMA-E-GARCH transformation and random effects to self. 
		If reverse_difference and the ARIMA difference term d>0, the standardized variables are converted to
		the original undifferenced order. This may be usefull if the predicted values should be used in another 
		differenced regression."""
		if hasattr(self,'Y_st'):
			return		
		panel=self.panel
		m=panel.lost_obs
		N,T,k=panel.X.shape
		if model_parser.DEFAULT_INTERCEPT_NAME in panel.args.names_d['beta']:
			m=self.args.args_d['beta'][0,0]
		else:
			m=panel.mean(panel.Y)	
		#e_norm=self.standardize_variable(self.u,reverse_difference)
		self.Y_st,   self.Y_st_long   = self.standardize_variable(panel.Y,reverse_difference)
		self.X_st,   self.X_st_long   = self.standardize_variable(panel.X,reverse_difference)
		self.XIV_st, self.XIV_st_long = self.standardize_variable(panel.XIV,reverse_difference)
		self.Y_pred_st=cf.dot(self.X_st,self.args.args_d['beta'])
		self.Y_pred=cf.dot(panel.X,self.args.args_d['beta'])	
		self.e_norm_long=self.stretch_variable(self.e_norm)
		self.Y_pred_st_long=self.stretch_variable(self.Y_pred_st)
		self.Y_pred_long=cf.dot(panel.input.X,self.args.args_d['beta'])
		self.e_long=panel.input.Y-self.Y_pred_long
		
		Rsq, Rsqadj, LL_ratio,LL_ratio_OLS=self.goodness_of_fit(False)
		Rsq2, Rsqadj2, LL_ratio2,LL_ratio_OLS2=self.goodness_of_fit(True)
		a=0
				
	
	def standardize_variable(self,X,norm=False,reverse_difference=False):
		X=cf.dot(self.AMA_1AR,X)
		X=(X+self.re_obj_i.RE(X,False)+self.re_obj_t.RE(X,False))
		if (not self.panel.Ld_inv is None) and reverse_difference:
			X=cf.dot(self.panel.Ld_inv,X)*self.panel.a[3]		
		if norm:
			X=X*self.v_inv05
		X_long=self.stretch_variable(X)
		return X,X_long	

	def goodness_of_fit(self,standarized):
		panel=self.panel
		if standarized:
			s_res=panel.var(self.e_RE)
			s_tot=panel.var(self.Y_st)
		else:
			s_res=panel.var(self.u)
			s_tot=panel.var(panel.Y)		
		r_unexpl=s_res/s_tot
		Rsq=1-r_unexpl
		Rsqadj=1-r_unexpl*(panel.NT-1)/(panel.NT-panel.args.n_args-1)
		panel.args.create_null_ll(self.panel)
		LL_ratio_OLS=2*(self.LL-panel.args.LL_OLS)
		LL_ratio=2*(self.LL-panel.args.LL_null)
		return Rsq, Rsqadj, LL_ratio,LL_ratio_OLS		
	
	def stretch_variable(self,X):
		N,T,k=X.shape
		panel=self.panel
		m=panel.map
		NT=panel.total_obs
		X_long=np.zeros((NT,k))
		X_long[m]=X
		return X_long
		
		

	def copy_args_d(self):
		return fu.copy_array_dict(self.args.args_d)

	
	def h(self,e,z):
		return h(e, z, self.panel)
	
			
def h(e,z,panel):
	try:
		d=dict()
		exec(panel.h_def,globals(),d)
		return d['h'](e,z)
	except Exception as err:
		raise RuntimeError("Warning,error in the ARCH error function h(e,z): %s" %(err))
	

def set_garch_arch(panel,args):
	if c is None:
		m=set_garch_arch_scipy(panel,args)
	else:
		m=set_garch_arch_c(panel,args)
	return m
		
		
def set_garch_arch_c(panel,args):
	"""Solves X*a=b for a where X is a banded matrix with 1 or zero, and args along
	the diagonal band"""
	n=panel.max_T
	rho=np.insert(-args['rho'],0,1)
	psi=np.insert(args['psi'],0,0)

	r=np.arange(n)
	AMA_1,AMA_1AR,GAR_1,GAR_1MA=(
	    np.diag(np.ones(n)),
		np.zeros((n,n)),
		np.diag(np.ones(n)),
		np.zeros((n,n))
	)
	c.bandinverse(args['lambda'],rho,-args['gamma'],psi,n,AMA_1,AMA_1AR,GAR_1,GAR_1MA)
	return  AMA_1,AMA_1AR,GAR_1,GAR_1MA


def set_garch_arch_scipy(panel,args):

	p,q,d,k,m=panel.pqdkm
	nW,n=panel.nW,panel.max_T

	AAR=-lag_matr(-panel.I,args['rho'])
	AMA_1AR,AMA_1=solve_mult(args['lambda'], AAR, panel.I)
	if AMA_1AR is None:
		return
	GMA=lag_matr(panel.zero,args['psi'])	
	GAR_1MA,GAR_1=solve_mult(-args['gamma'], GMA, panel.I)
	if GAR_1MA is None:
		return
	return AMA_1,AMA_1AR,GAR_1,GAR_1MA
	
def solve_mult(args,b,I):
	"""Solves X*a=b for a where X is a banded matrix with 1  and args along
	the diagonal band"""
	n=len(b)
	q=len(args)
	X=np.zeros((q+1,n))
	X[0,:]=1
	X2=np.zeros((n,n))
	w=np.zeros(n)
	r=np.arange(n)	
	for i in range(q):
		X[i+1,:n-i-1]=args[i]
	try:
		X_1=scipy.linalg.solve_banded((q,0), X, I)
		if np.any(np.isnan(X_1)):
			return None,None			
		X_1b=cf.dot(X_1, b)
	except:
		return None,None

	return X_1b,X_1


def add_to_matrices(X_1,X_1b,a,ab,r):
	for i in range(0,len(a)):	
		if i>0:
			d=(r[i:],r[:-i])
			X_1[d]=a[i]
		else:
			d=(r,r)
		X_1b[d]=ab[i]	
	return X_1,X_1b

def lag_matr(L,args):
	k=len(args)
	if k==0:
		return L
	L=1*L
	r=np.arange(len(L))
	for i in range(k):
		d=(r[i+1:],r[:-i-1])
		L[d]=args[i]

	return L