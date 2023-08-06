import numpy as np
from itertools import permutations

def get_indep_indexies(Np,hide_info):
	if(not hide_info):
		print("#-------------------------------------")
		print("Getting Symmetric Indexies ...")

	Doub_12 = np.zeros([Np,Np,Np])
	Doub_22 = np.zeros([Np,Np,Np,Np])
	Trip_13 = np.zeros([Np,Np,Np,Np])
	Trip_23 = np.zeros([Np,Np,Np,Np,Np])
	Trip_33 = np.zeros([Np,Np,Np,Np,Np,Np])

	n3 = Np**3 ; v3 = np.linspace(1,n3,n3)
	n4 = Np**4 ; v4 = np.linspace(1,n4,n4)
	n5 = Np**5 ; v5 = np.linspace(1,n5,n5)
	n6 = Np**6 ; v6 = np.linspace(1,n6,n6)

	cont3, cont4, cont5, cont6 = 0, 0, 0, 0
	for i in range(Np):
		for j in range(Np):
			for k in range(Np):
				#-------------------------------------
				# Doublet
				#-------------------------------------
				Doub_12[i][j][k] = v3[cont3]
				Doub_12[i][k][j] = v3[cont3]

				cont3 += 1
				for l in range(Np):
					prmt1 = list( permutations([i,j]) )
					prmt2 = list( permutations([k,l]) )

					for P1 in range(len(prmt1)):
						for P2 in range(len(prmt2)):
							I, J, K, L = list(prmt1[P1])+list(prmt2[P2])
							Doub_22[I][J][K][L] = v4[cont4]
					
					#-------------------------------------
					# Triplet
					#-------------------------------------

					prmt3 = list( permutations([j,k,l]) )
					for P3 in range(len(prmt3)):
						J, K, L = list(prmt3[P3])
						Trip_13[i][J][K][L] = v4[cont4]

					cont4 += 1
					
					for m in range(Np):
						prmt1 = list( permutations([i,j]) )
						prmt2 = list( permutations([k,l,m]) )

						for P1 in range(len(prmt1)):
							for P2 in range(len(prmt2)):
								I, J, K, L, M = list(prmt1[P1])+list(prmt2[P2])
								Trip_23[I][J][K][L][M] = v5[cont5]

						cont5 += 1

						for n in range(Np):
							prmt1 = list( permutations([i,j,k]) )
							prmt2 = list( permutations([l,m,n]) )

							for P1 in range(len(prmt1)):
								for P2 in range(len(prmt2)):
									I, J, K, L, M, N = list(prmt1[P1])+list(prmt2[P2])
									Trip_33[I][J][K][L][M][N] = v6[cont6]

							cont6 += 1

	vals1, vals2, vals3, vals4, vals5 = [], [], [], [], []
	indepD_12 = []
	indepD_22 = []
	indepT_13 = []
	indepT_23 = []
	indepT_33 = []

	for i in range(Np):
		for j in range(Np):
			for k in range(Np):
				v1 = Doub_12[i][j][k]
				if(not v1 in vals1):
					vals1.append(v1)
					indepD_12.append([i,j,k])

				for l in range(Np):
					v2 = Doub_22[i][j][k][l]
					if(not v2 in vals2):
						vals2.append(v2)
						indepD_22.append([i,j,k,l])

					v3 = Trip_13[i][j][k][l]
					if(not v3 in vals3):
						vals3.append(v3)
						indepT_13.append([i,j,k,l])

					for m in range(Np):
						v4 = Trip_23[i][j][k][l][m]
						if(not v4 in vals4):
							vals4.append(v4)
							indepT_23.append([i,j,k,l,m])

						for n in range(Np):
							v5 = Trip_33[i][j][k][l][m][n]
							if(not v5 in vals5):
								vals5.append(v5)
								indepT_33.append([i,j,k,l,m,n])

	idxs_doub = [indepD_12, indepD_22]
	idxs_trip = [indepT_13, indepT_23, indepT_33]

	if(not hide_info):
		print("# [Ntot - Nindep]:\n")
		print('Doub(1,2): ', n3, len(indepD_12))
		print('Doub(2,2): ', n4, len(indepD_22))
		print('Trip(1,3): ', n4, len(indepT_13))
		print('Trip(2,3): ', n5, len(indepT_23))
		print('Trip(2,3): ', n6, len(indepT_33))
		print("#----------"*3)

	return idxs_doub, idxs_trip