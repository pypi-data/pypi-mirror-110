#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pickle
import tempfile
import os
import zipfile

tdr=tempfile.gettempdir()
fname_args=os.path.join(tdr,'paneltime.args')
fname_data=os.path.join(tdr,'paneltime.data')
fname_key=os.path.join(tdr,'paneltime.key')
fname_temprec=os.path.join(tdr,'paneltime.temprec')
fname_image_temprec=os.path.join(tdr,'paneltime.tempimagerec')
fname_window=os.path.join(tdr,'paneltime.win')
fname_datasets=os.path.join(tdr,'paneltime.datasets')
max_sessions=20
file_name_list=[fname_args,fname_data,fname_key,fname_image_temprec,fname_window,fname_datasets]

class args_archive:

	def __init__(self,model_string,loadargs):
		"""Loads parameters if a similar model has been estimated before. Stored parameters are accessed by
		creating an instance of this class"""  
		
		self.model_key=model_string#perhaps add possibility for determening model based on data: get_model_key(X, Y, W)
		self.data=load_obj(fname_args)
		if self.data is None:
			(self.args,self.conv)=(None,None)
			return
		(d,a)=self.data
		if self.model_key in list(d.keys()) and loadargs==1:
			(self.args,self.conv)=d[self.model_key]
		elif 'last_args##' in list(d.keys()) and loadargs==2:
			(self.args,self.conv)=d['last_args##']
		else:
			(self.args,self.conv)=(None,None)

	def load(self):#for debugging
		data=load_obj(fname_args)
		(d,a)=data
		if self.model_key in d.keys():
			return d[self.model_key]
		else:
			return (None,None)		

	def save(self,args,conv):
		"""Saves the estimated parameters for later use"""
		if not self.data is None:
			d,a=self.data#d is d dictionary, and a is a sequental list that allows us to remove the oldest entry when the database is full
			if (len(a)>max_sessions) and (not self.model_key in d):
				d.pop(a.pop(0))
		else:
			d=dict()
			a=[]
		d[self.model_key]=(args,conv)
		d['last_args##']=d[self.model_key]
		if self.model_key in a:
			a.remove(self.model_key)
		a.append(self.model_key)		
		if len(a)!=len(d):
			a=list(d.keys())
		self.data=(d,a)
		save_obj(fname_args,self.data)



def loaddata(key):
	"""Loads data if a similar data was loaded before. """  
	
	key=' '.join(key.split())
	current_key=load_obj(fname_key)
	if key==current_key:
		return load_obj(fname_data)
	
	
def savedata(key,data):
	"""saves data  """
	key=' '.join(key.split())
	save_obj(fname_key,key)
	save_obj(fname_data,data)
	

def load_model(self):#for debugging
	data=load_obj(datafname)
	(d,a)=data
	if self.model_key in d.keys():
		return d[self.model_key]
	else:
		return (None,0,None,None)		

def load_obj(fname):
	for i in [0,1]:
		try:
			f=open(fname, "r+b")
			u= pickle.Unpickler(f)
			u=u.load()
			f.close()
			return u 
		except Exception as e:
			print(e)
			recreate_from_zip()
			if i==1:
				return
	
def save_zip():
	wdr=os.getcwd()
	zip_file_path=os.path.join(wdr,'data.paneltime')
	zip_arch=zipfile.ZipFile(zip_file_path,'w')	
	for f in file_name_list:
		if os.path.isfile(f):
			zip_arch.write(f,os.path.basename(f))
	for i in range(100):
		f=os.path.join(tdr,f'paneltime {i}.jpg')
		if os.path.isfile(f):
			zip_arch.write(f,os.path.basename(f))
	zip_arch.close()
	
def test_and_repair():
	ok=True
	for f in file_name_list:
		ok=ok and os.path.isfile(f)
		if not ok:
			a=0
	if not ok:
		recreate_from_zip()
	
def recreate_from_zip():
	wdr=os.getcwd()
	zip_file_path=os.path.join(wdr,'data.paneltime')
	try:
		zip_arch=zipfile.ZipFile(zip_file_path,'r')
	except:
		return
	for f in zip_arch.filelist:
		zf=zip_arch.read(f.filename)
		fl=open(os.path.join(tdr,f.filename),'wb')
		fl.write(zf)
		fl.close()
	zip_arch.close()
	
def save_obj(fname,obj):
	f=open(fname, "w+b")
	pickle.dump(obj,f)   
	f.flush() 
	f.close()	

def get_model_key(X,Y, IDs,W):
	"""Creates a string that is unique for the dataframe and arguments. Used to load starting values for regressions that
	have been run before"""
	s="%s%s%s%s" %(l(X),l(X**2),l(Y),l(Y**2))
	if not IDs is None:
		s+="%s%s" %(l(IDs),l(IDs**2))
	if not W is None:
		s+="%s%s" %(l(W),l(W**2))
	return s

def l(x):
	n=5
	x=str(np.sum(x))
	if len(x)>n:
		x=x[len(x)-n:]
	return x


class tempfile_manager:
	def __init__(self):
		#at initialization, all temporary files from previous sessions are deleted
		self.rec=load_obj(fname_temprec)
		if self.rec is None:
			self.rec=[]
		for f in self.rec:
			try:
				os.remove(f)
			except:
				pass
		save_obj(fname_temprec,[])
		
	def TemporaryFile(self):
		f=tempfile.NamedTemporaryFile()
		self.rec.append(f.name)
		save_obj(fname_temprec,self.rec)
		return f
	
	
class temp_image_manager:
	def __init__(self,used_imgs):
		if used_imgs is None:
			used_imgs=[]
		#at initialization, all temporary images from previous sessions that are not referenced are deleted
		self.rec=load_obj(fname_image_temprec)	
		if self.rec is None:
			self.rec=[]
		for f in self.rec:
			if not f in used_imgs:
				try:
					os.remove(f)
				except:
					pass
		save_obj(fname_image_temprec,[])		
		self.assigned_files=used_imgs
			
	def TemporaryFile(self):
		for i in range(10000):
			f=os.path.join(tdr,f'paneltime {i}.jpg')
			if (not os.path.isfile(f)) and (not f in self.assigned_files):
				self.assigned_files.append(f)
				self.rec.append(f)
				save_obj(fname_image_temprec,self.rec)				
				return f
		a=0
		raise RuntimeError("""You have over 10000 temporary image files. 
		There must be some problems with deleting them from your temporary folder""")
	

				
			
		
	