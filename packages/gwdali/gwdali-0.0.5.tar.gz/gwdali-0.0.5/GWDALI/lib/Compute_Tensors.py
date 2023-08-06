import os, sys
import numpy as np
import GWDALI.lib.Waveforms as wf
import GWDALI.lib.Angles_lib as geo
import GWDALI.lib.Dictionaries as gwdict
import GWDALI.lib.Derivatives_Tensors as gwfunc
import GWDALI.lib.Symmetric_Indexies as sym

from itertools import permutations
from tqdm import trange

deg2rad = np.pi/180

Waveforms, PSD, labels_tex = gwdict.Load_Dictionaries()

def check_permutations(prmt0):
	prmt = []
	for i in range(len(prmt0)):
		p0 = list(prmt0[i])
		if(not p0 in prmt):
			prmt.append(p0)
	return prmt # list type

def Get_Tensors(FreeParams, gw_prms, detectors, dali_method, approximant, hide_info):
	
	#if(hide_info): sys.stdout = open(os.devnull, 'w')

	Np = len(FreeParams)
	rho2 = 0

	Fisher   = np.zeros([Np, Np])
	Doublet3 = np.zeros(Np**3)
	Doublet4 = np.zeros(Np**4)
	Triplet4 = np.zeros(Np**4)
	Triplet5 = np.zeros(Np**5)
	Triplet6 = np.zeros(Np**6)

	num_det = 1
	GwData = [] ; SNR = []
	for det in detectors:

		#-----------------------------------
		# Computing Signal to Noise 
		#-----------------------------------
		# from Derivative_Tensors.py
		h 	  = gwfunc.Signal(gw_prms, det, approximant)
		SNR2  = gwfunc.ScalarProduct(det['freq'], det['Sn'],h,h)
		rho2 += SNR2
		GwData.append(h) ; SNR.append(np.sqrt(SNR2))
		#------------------------------------------------------
		# Computing Fisher Matrix
		#------------------------------------------------------

		if(not hide_info): print("\n\n\t Computing Fisher %s(%d) ..." % (det['name'],num_det))
		for i in range(Np):
			for j in range(i+1):
				if(not hide_info): print('Fisher: [%d-%d]' % (i+1,j+1), end='\r')
				xj = FreeParams[j]
				xi = FreeParams[i]

				Fij = gwfunc.Fisher_ij(xi, xj, gw_prms, det, approximant)
				Fisher[i][j] += Fij
				if(i!=j): Fisher[j][i] += Fij

		brute_force = False
		if(brute_force):
			#------------------------------------------------------
			# Computing Doublet Coefficients (Brute Force)
			#------------------------------------------------------

			#*****************************#*****************************#*****************************
			#*****************************#*****************************#*****************************
			
			if(dali_method in ["Doublet","Triplet"]):
				if(not hide_info): print("\n\n\tComputing Doublet/Triplet Tensors %s(%d)..." % (det['name'],num_det))
				cont = 0
				for i in range(Np):
					xi = FreeParams[i]
					
					for j in range(Np):
						xj = FreeParams[j]
					
						for k in range(Np):
							xk = FreeParams[k]
							
							idx3 = i*Np**2 + j*Np + k
							Doublet3[idx3] += gwfunc.func_doublet3(xi,xj,xk, gw_prms, det, approximant) # [1,2]

							for l in range(Np):
								xl = FreeParams[l]
								if((not hide_info) and dali_method == 'Doublet'):
									print('Doublet: [%d-%d-%d-%d]' % (i+1,j+1,k+1,l+1), end='\r')

								idx4 = i*Np**3 + j*Np**2 + k*Np + l
								Doublet4[idx4] += gwfunc.func_doublet4(xi,xj,xk,xl, gw_prms, det, approximant) # [2,2]

								#*****************************#*****************************#*****************************
								#*****************************#*****************************#*****************************

								if(dali_method == 'Triplet'):
									Triplet4[idx4] += gwfunc.func_triplet4(xi,xj,xk,xl, gw_prms, det, approximant)

									for m in range(Np):
										xm = FreeParams[m]
										idx5 = i*Np**4 + j*Np**3 + k*Np**2 + l*Np + m
										Triplet5[idx5] += gwfunc.func_triplet5(xi,xj,xk,xl,xm, gw_prms, det, approximant)

										for n in range(Np):
											xn = FreeParams[n]
											if(not hide_info):
												print('Triplet: [%d-%d-%d-%d-%d-%d]' % (i+1,j+1,k+1,l+1,m+1,n+1), end='\r')
											
											idx6 = i*Np**5 + j*Np**4 + k*Np**3 + l*Np**2 + m*Np + n
											Triplet6[idx6] += gwfunc.func_triplet6(xi,xj,xk,xl,xm,xn, gw_prms, det, approximant)
								else:
									Triplet4, Triplet5, Triplet6 = None, None, None
			num_det+=1
			#*****************************#*****************************#*****************************
			#*****************************#*****************************#*****************************
			
		else:
			#------------------------------------------------------
			# Checking Symmetries
			#------------------------------------------------------
			idxs_doub, idxs_trip = sym.get_indep_indexies(Np, hide_info)

			if(dali_method in ["Doublet","Triplet"]):
				if(not hide_info): print("\n\n\tComputing Doublet/Triplet Tensors %s..." % det['name'])
				idxsD_12, idxsD_22 = idxs_doub

				for Idx2 in range(len(idxsD_12)):
					i, j, k = idxsD_12[Idx2]
					xi = FreeParams[i]
					xj = FreeParams[j]
					xk = FreeParams[k]
					value = gwfunc.func_doublet3(xi,xj,xk, gw_prms, det, approximant)
					prmt = check_permutations( list(permutations([j,k])) ) ; lenP = len(prmt)
					for p in range(lenP):
						j, k = list(prmt[p])
						IdxP = i*Np**2 + j*Np + k
						if((not hide_info)):
							print('Doublet(1,2): [%d-%d-%d]' % (i+1,j+1,k+1), end='\r')
						Doublet3[IdxP] += value

				if(not hide_info):print('\n')
				for Idx2 in range(len(idxsD_22)):
					i, j, k, l = idxsD_22[Idx2]
					xi = FreeParams[i]
					xj = FreeParams[j]
					xk = FreeParams[k]
					xl = FreeParams[l]
					value = gwfunc.func_doublet4(xi,xj,xk,xl, gw_prms, det, approximant)
					prmt1 = check_permutations( list(permutations([i,j])) ) ; len1 = len(prmt1)
					prmt2 = check_permutations( list(permutations([k,l])) ) ; len2 = len(prmt2)
					for n1 in range(len1):
						for n2 in range(len2):
							i, j, k, l = list(prmt1[n1])+list(prmt2[n2])
							IdxP = i*Np**3 + j*Np**2 + k*Np + l
							if(not hide_info):
								print('Doublet(2,2): [%d-%d-%d-%d]' % (i+1,j+1,k+1,l+1), end='\r')		
							Doublet4[IdxP] += value

				#*****************************#*****************************#*****************************
				if(dali_method == 'Triplet'):
					idxsT_13, idxsT_23, idxsT_33 = idxs_trip

					if(not hide_info):print('\n')
					for Idx3 in range(len(idxsT_13)):
						i, j, k, l = idxsT_13[Idx3]
						xi = FreeParams[i]
						xj = FreeParams[j]
						xk = FreeParams[k]
						xl = FreeParams[l]
						value = gwfunc.func_triplet4(xi,xj,xk,xl, gw_prms, det, approximant)
						prmt = check_permutations( list(permutations([j,k,l])) ) ; lenP = len(prmt)
						for idx in range(lenP):
							j, k, l = list(prmt[idx])
							if(not hide_info):
								print('Triplet(1,3): [%d-%d-%d-%d]' % (i+1,j+1,k+1,l+1), end='\r')
							IdxP = i*Np**3 + j*Np**2 + k*Np + l
							Triplet4[IdxP] += value

					if(not hide_info):print('\n')
					for Idx3 in range(len(idxsT_23)):
						i, j, k, l, m = idxsT_23[Idx3]
						xi = FreeParams[i]
						xj = FreeParams[j]
						xk = FreeParams[k]
						xl = FreeParams[l]
						xm = FreeParams[m]
						value = gwfunc.func_triplet5(xi,xj,xk,xl,xm, gw_prms, det, approximant)
						prmt1 = check_permutations( list(permutations([i,j]))   ) ; len1 = len(prmt1)
						prmt2 = check_permutations( list(permutations([k,l,m])) ) ; len2 = len(prmt2)
						for n1 in range(len1):
							for n2 in range(len2):
								i, j, k, l, m = list(prmt1[n1]) + list(prmt2[n2])
								if(not hide_info):
									print('Triplet(2,3): [%d-%d-%d-%d-%d]' % (i+1,j+1,k+1,l+1,m+1), end='\r')
								IdxP = i*Np**4 + j*Np**3 + k*Np**2 + l*Np + m
								Triplet5[IdxP] += value

					if(not hide_info):print('\n')
					for Idx3 in range(len(idxsT_33)):
						i, j, k, l, m, n = idxsT_33[Idx3]
						xi = FreeParams[i]
						xj = FreeParams[j]
						xk = FreeParams[k]
						xl = FreeParams[l]
						xm = FreeParams[m]
						xn = FreeParams[n]
						value = gwfunc.func_triplet6(xi,xj,xk,xl,xm,xn, gw_prms, det, approximant)
						prmt1 = check_permutations( list(permutations([i,j,k])) ) ; len1 = len(prmt1)
						prmt2 = check_permutations( list(permutations([l,m,n])) ) ; len2 = len(prmt2)
						for n1 in range(len1):
							for n2 in range(len2):
								i, j, k, l, m, n = list(prmt1[n1]) + list(prmt2[n2])
								if(not hide_info):
									print('Triplet(3,3): [%d-%d-%d-%d-%d-%d]' % (i+1,j+1,k+1,l+1,m+1,n+1), end='\r')
								IdxP = i*Np**5 + j*Np**4 + k*Np**3 + l*Np**2 + m*Np + n
								Triplet6[IdxP] += value
			#*****************************#*****************************#*****************************
			#*****************************#*****************************#*****************************

	SNR_sum = np.sqrt(rho2)
	if(not hide_info):
		print("\n >> SNR = ", SNR_sum)
		print(" >> 100/SNR = %.2e" % (100/SNR_sum) + '%\n')

	Doublet = [Doublet3, Doublet4]
	Triplet = [Triplet4, Triplet5, Triplet6]

	return [SNR, GwData, Fisher , Doublet, Triplet]