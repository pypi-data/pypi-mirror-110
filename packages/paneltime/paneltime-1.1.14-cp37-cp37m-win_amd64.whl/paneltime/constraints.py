#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import stat_functions as stat
import functions as fu
import calculus_functions as cf

MAX_COLLINEARITY=1e+7
EXTREEME_COLLINEARITY=1E+20
SMALL_COLLINEARITY=30



class constraint:
	def __init__(self,index,assco,cause,value, interval,names,category):
		self.name=names[index]
		self.intervalbound=None
		self.max=None
		self.min=None
		self.value=None
		self.value_str=None
		if interval is None:
			self.value=value
			self.value_str=str(round(self.value,8))
		else:
			if interval[0]>interval[1]:
				raise RuntimeError('Lower constraint cannot exceed upper')
			self.min=interval[0]
			self.max=interval[1]
			self.cause='user/general constraint'
		self.assco_ix=assco
		if assco is None:
			self.assco_name=None
		else:
			self.assco_name=names[assco]
		self.cause=cause
		self.category=category	
		
class constraints(dict):

	"""Stores the constraints of the LL maximization"""	
	def __init__(self,direction,args,its=0):
		dict.__init__(self)
		self.categories={}
		self.fixed={}
		self.intervals={}
		self.associates={}
		self.collinears={}
		self.args=args
		self.panel_args=direction.panel.args
		self.CI=None
		self.its=its
		self.pqdkm=direction.panel.pqdkm
		self.m_zero=direction.panel.m_zero

	def add(self,name,assco,cause,interval=None,replace=True,value=None,args=None):
		#(self,index,assco,cause,interval=None,replace=True,value=None)
		name,index=self.panel_args.get_name_ix(name)
		name_assco,assco=self.panel_args.get_name_ix(assco,True)
		for i in index:
			self.add_item(i,assco,cause, interval ,replace,value,args)
		
	def clear(self,cause=None):
		for c in list(self.keys()):
			if self[c].cause==cause or cause is None:
				self.delete(c)	

	def add_item(self,index,assco,cause,interval,replace,value,args):
		"""Adds a constraint. 'index' is the position
		for which the constraints shall apply.  \n\n

		Equality constraints are chosen by specifying 'minimum_or_value' \n\n
		Inequality constraints are chosen specifiying 'maximum' and 'minimum'\n\n
		'replace' determines whether an existing constraint shall be replaced or not 
		(only one equality and inequality allowed per position)"""
		
		if args is None:
			args=self.panel_args

		if not replace:
			if index in self:
				return False
		interval,value=test_interval(interval, value)
		if interval is None:#this is a fixed constraint
			if len(self.fixed)==len(args.names_v)-1:#can't lock all variables
				return False
			if value is None:
				value=self.args.args_v[index]
			if index in self.intervals:
				c=self[index]
				if not (c.min<value<c.max):
					return False
				else:
					self.intervals.pop(index)
		elif index in self.fixed: #this is an interval constraint, no longer a fixed constraint
			self.fixed.pop(index)

		eq,category,j=self.panel_args.positions_map[index]
		if not category in self.categories:
			self.categories[category]=[index]
		elif not index in self.categories[category]:
			self.categories[category].append(index)

		c=constraint(index,assco,cause,value, interval ,args.names_v,category)
		self[index]=c
		if value is None:
			self.intervals[index]=c
		else:
			self.fixed[index]=c
		if not assco is None:
			if not assco in self.associates:
				self.associates[assco]=[index]
			elif not index in self.associates[assco]:
				self.associates[assco].append(index)
		if cause=='collinear':
			self.collinears[index]=assco
		return True
		
	def delete(self,index):
		if not index in self:
			return False
		self.pop(index)
		if index in self.intervals:
			self.intervals.pop(index)
		if index in self.fixed:
			self.fixed.pop(index)		
		eq,category,j=self.panel_args.positions_map[index]
		c=self.categories[category]
		if len(c)==1:
			self.categories.pop(category)
		else:
			i=np.nonzero(np.array(c)==index)[0][0]
			c.pop(i)
		a=self.associates
		for i in a:
			if index in a[i]:
				if len(a[i])==1:
					a.pop(i)
					break
				else:
					j=np.nonzero(np.array(a[i])==index)[0][0]
					a[i].pop(j)
		if index in self.collinears:
			self.collinears.pop(index)
		return True
		

	def set_fixed(self,x):
		"""Sets all elements of x that has fixed constraints to the constraint value"""
		for i in self.fixed:
			x[i]=self.fixed[i].value
		
	def within(self,x,fix=False):
		"""Chekcs if x is within interval constraints. If fix=True, then elements of
		x outside constraints are set to the nearest constraint. if fix=False, the function 
		returns False if x is within constraints and True otherwise"""
		for i in self.intervals:
			c=self.intervals[i]
			if (c.min<=x[i]<=c.max):
				c.intervalbound=None
			else:
				if fix:
					x[i]=max((min((x[i],c.max)),c.min))
					c.intervalbound=str(round(x[i],8))
				else:
					return False
		return True
	
	def add_static_constraints(self,overflow_problem):
		pargs=self.panel_args
		p, q, d, k, m=self.pqdkm
		
		self.add_custom_constraints(pargs.user_constraints)
		if overflow_problem:
			general_constraints=[('rho',-0.5,0.5),('lambda',-0.5,0.5),('gamma',-0.5,0.5),('psi',-0.5,0.5)]
			self.add_custom_constraints(general_constraints)
		else:
			general_constraints=[('rho',-2,2),('lambda',-2,2),('gamma',-2,2),('psi',-2,2)]
			self.add_custom_constraints(general_constraints)
			
		if self.its==0 and p>0:
			if pargs.args_init.args_d['rho'][0]==0:
				self.add(pargs.positions['rho'][0],None,'Initial MA constr',value=0.0)
		if self.m_zero:
			self.add(pargs.positions['psi'][0],None,'GARCH input constr',value=0.05)
			
		if k*m==0:
			return
		if sum(self.args.args_v[pargs.positions['psi']]**2)==0:
			for i in pargs.positions['gamma']:
				self.add(i,None,'GARCH term cannot be positive if ARCH terms are zero',value=0)
	
	def add_dynamic_constraints(self,direction):
		ll=direction.ll
		k,k=direction.H.shape
		self.weak_mc_dict=dict()
		include=np.array(k*[True])
		include[list(direction.constr.fixed)]=False
		self.H_correl_problem=constraint_correl_cluster(direction,include)
		self.mc_problems=[]#list of [index,associate,condition index]
		self.CI=constraint_multicoll(k, direction, include, self.mc_problems)
		add_mc_constraint(direction,self.mc_problems,self.weak_mc_dict)
		select_arma(direction.constr, ll)
	
	def add_custom_constraints(self,constraints,replace=True,cause='user constraint',clear=False,args=None):
		"""Adds custom range constraints\n\n
			constraints shall be on the format [(name, minimum, maximum), ...]
			or
			a dictionary of the same form of an argument dictionary
			(a dictionary of dictonaries on the form dict[category][name]) 
			where items are lists of [minimum,maximum] or the fixing value
			
			name is taken from self.panel_args.names_v"""	
		
		if clear:
			self.clear(cause)
		if type(constraints)==list or type(constraints)==tuple:
			for c in constraints:
				self.add_custom_constraints_list(c,replace,cause,args)
		elif type(constraints)==dict:
			self.add_custom_constraints_dict(constraints,replace,cause,args)
		else:
			raise TypeError("The constraints must be a list, tuple or dict.")
	
	
	def add_custom_constraints_list(self,constraint,replace,cause,args):
		"""Adds a custom range constraint\n\n
			constraint shall be on the format (name, minimum, maximum)"""
		if type(constraint)==str or isinstance(constraint,int):
			name, value=constraint,None
			self.add(name,None,cause,replace=replace,value=value,args=args)
			return
		elif len(constraint)==2:
			name, minimum,maximum=list(constraint)+[None]
		elif len(constraint)==3:
			name, minimum, maximum=constraint
		else:
			raise TypeError("A constraint needs to be a string, integer or iterable with lenght no more than tree.")

		name,ix=self.panel_args.get_name_ix(name)
		m=[minimum,maximum]
		for i in range(2):
			if type(m[i])==str:
				try:
					m[i]=eval(m[i],globals(),self.direction.ll.__dict__)
				except:
					print(f"Custom constraint {name} ({m[i]}) failed")
					return
		[minimum,maximum]=m
		self.add(name,None,cause, [minimum,maximum],replace,args=args)
		
	def add_custom_constraints_dict(self,constraints,replace,cause,args):
		"""Adds a custom range constraint\n\n
		   If list, constraint shall be on the format (minimum, maximum)"""
		for grp in constraints:
			for name in constraints[grp]:	
				c=constraints[grp][name]
				if type(c)==list:
					self.add(name,None,cause, c,replace,args=args)
				else:
					self.add(name,None,cause, [c,None],replace,args=args)
	
	
def test_interval(interval,value):
	if not interval is None:
		if np.any([i is None for i in interval]):
			if interval[0] is None:
				value=interval[1]
			else:
				value=interval[0]
			interval=None	
	return interval,value

def append_to_ID(ID,intlist):
	inID=False
	for i in intlist:
		if i in ID:
			inID=True
			break
	if inID:
		for j in intlist:
			if not j in ID:
				ID.append(j)
		return True
	else:
		return False

def correl_IDs(p):
	IDs=[]
	appended=False
	x=np.array(p[:,1:3],dtype=int)
	for i,j in x:
		for k in range(len(IDs)):
			appended=append_to_ID(IDs[k],[i,j])
			if appended:
				break
		if not appended:
			IDs.append([i,j])
	g=len(IDs)
	keep=g*[True]
	for k in range(g):
		if keep[k]:
			for h in range(k+1,len(IDs)):
				appended=False
				for m in range(len(IDs[h])):
					if IDs[h][m] in IDs[k]:
						appended=append_to_ID(IDs[k],  IDs[h])
						keep[h]=False
						break
	g=[]
	for i in range(len(IDs)):
		if keep[i]:
			g.append(IDs[i])
	return g

def normalize(H,include):
	C=-H[include][:,include]
	d=np.maximum(np.diag(C).reshape((len(C),1)),1e-30)**0.5
	C=C/(d*d.T)
	includemap=np.arange(len(include))[include]
	return C,includemap
	
def decomposition(H,include=None):
	if include is None:
		include=[True]*len(H)
	C,includemap=normalize(H, include)
	c_index,var_prop=stat.var_decomposition(XXNorm=C)
	c_index=c_index.flatten()
	return c_index, var_prop,includemap
	
	
def multicoll_problems(direction,H,include,mc_problems):
	c_index, var_prop, includemap = decomposition(H, include)
	if c_index is None:
		return False,False
	mc_list=[]
	largest_ci=None
	for cix in range(1,len(c_index)):
		if ((np.sum(var_prop[-cix]>0.5)>1) or ((np.sum(var_prop[-cix]>0.3)>1) and (np.sum(var_prop[-cix]>0.99)>0))) and (c_index[-cix]>SMALL_COLLINEARITY):
			if largest_ci is None:
				largest_ci=c_index[-cix]
			var_prop_ix=np.argsort(var_prop[-cix])[::-1]
			var_prop_val=var_prop[-cix][var_prop_ix]
			j=var_prop_ix[0]
			j=includemap[j]
			done=var_prop_check(direction,var_prop_ix, var_prop_val, includemap,j,mc_problems,c_index[-cix],mc_list)
			if done:
				break
	if len(mc_list)==0:
		return  c_index[-1],mc_list
	return c_index[-1],mc_list

def var_prop_check(direction,var_prop_ix,var_prop_val,includemap,assc,mc_problems,cond_index,mc_list):
	if cond_index>EXTREEME_COLLINEARITY:
		lim=0.3
	else:
		lim=0.5
	for i in range(1,len(var_prop_ix)):
		if var_prop_val[i]<lim:
			return True
		index=var_prop_ix[i]
		index=includemap[index]
		mc_problems.append([index,assc,cond_index])
		mc_list.append(index)
		return False
		
def add_mc_constraint(direction,mc_problems,weak_mc_dict):
	"""Adds constraints for severe MC problems"""
	constr=direction.constr
	if len(mc_problems)==0:
		return
	no_check=get_no_check(direction)
	a=[i[0] for i in mc_problems]
	if no_check in a:
		mc=mc_problems[a.index(no_check)]
		mc[0],mc[1]=mc[1],mc[0]
	mc_limit=MAX_COLLINEARITY
	if direction.increment==0:
		mc_limit=SMALL_COLLINEARITY
	for index,assc,cond_index in mc_problems:
		if (not index in weak_mc_dict) and (cond_index>SMALL_COLLINEARITY) and (cond_index<=mc_limit) and (not index==no_check):
			weak_mc_dict[index]=[assc,cond_index]#contains also collinear variables that are only slightly collinear, which shall be restricted when calcuating CV-matrix.	
		if not ((index in constr.associates) or (index in constr.collinears)) and cond_index>mc_limit and (not index==no_check):
			constr.add(index,assc,'collinear')
		
def get_no_check(direction):
	no_check=direction.panel.options.do_not_constrain.value
	X_names=direction.panel.input.X_names
	if not no_check is None:
		if no_check in X_names:
			return X_names.index(no_check)
		print("A variable was set for the 'Do not constraint' option (do_not_constrain), but it is not among the x-variables")
			
	
		


def constraint_multicoll(k,direction,include,mc_problems):
	CI_max=0
	for i in range(k-1):
		CI,mc_list=multicoll_problems(direction,direction.H,include,mc_problems)
		CI_max=max((CI_max,CI))
		if len(mc_list)==0:
			break
		include[mc_list]=False
	return CI_max
		
def constraint_correl_cluster(direction,include):
	if int(direction.its/2)==direction.its/2 and direction.its>0:
		return False		
	H=direction.H
	dH=np.diag(H).reshape((len(H),1))
	corr=np.abs(H/(np.abs(dH*dH.T)+1e-100)**0.5)
	np.fill_diagonal(corr,0)
	problems=list(np.unique(np.nonzero((corr>1-1e-12)*(corr<1))[0]))
	if len(problems)==0:
		return False
	#not_problem=np.argsort(dH[problems].flatten())[0]
	#problems.pop(not_problem)
	allix=list(range(len(H)))
	for i in problems:
		allix.pop(allix.index(i))
	if len(allix)==0:
		return	False
	not_problem=np.argsort(dH[allix].flatten())[-1]
	allix.pop(not_problem)	
	for i in allix:
		include[i]=False
		if not i in direction.constr.fixed:
			direction.constr.add(i,None,'Perfect correlation in hessian')
	return True
		

	

def select_arma(constr,ll):
	for i in constr.collinears:
		if constr[i].category in ['rho','lambda', 'gamma','psi']:
			assc=constr.collinears[i]
			if not assc in constr.fixed:
				if abs(ll.args.args_v[assc])<abs(ll.args.args_v[i]):
					constr.delete(i)
					constr.add(assc,i,'collinear')
	
	
			
		


