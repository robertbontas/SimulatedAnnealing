# obiecte  0  1  2  3  4  5  6  7  8  9
# valori  79 32 47 18 26 85 33 40 45 59
# marime  85 26 48 21 22 95 43 45 55 52
# max(marime) = 101

from ctypes import resize
import numpy as np

#Valoarea si marimea totala a unei impachetari.
def total_valoare_marime(impachetare,valori,marimi,marime_maxima_admisa):
    #valoare
    v=0.0
    #marime
    m=0.0
    for i in range(len(impachetare)):
        if impachetare[i]==1:
            v+=valori[i]
            m+=marimi[i]
    #Prea mare ca sa fie pus in rucsac
    if m > marime_maxima_admisa:
        v=0.0
    return(v,m)

def vecin(impachetare,rnd):
    n=len(impachetare)
    rez=np.copy(impachetare)
    i=rnd.randint(n)
    if rez[i]==0:
        rez[i]=1
    elif rez[i]==1:
        rez[i]=0
    return rez

def rezolv_SA(nrObiecte, rnd, valori, marimi, marime_maxima,max_iter,temperatura_start,alpha):
    temperatura_curenta=temperatura_start
    impachetare_curenta= np.ones(nrObiecte,dtype=np.int64)
    print("impachetare initiala:")
    (valoare_curenta,marime_curenta)=total_valoare_marime(impachetare_curenta,valori,marimi,marime_maxima)
    iteratie=0
    interval=(int)(max_iter/10)
    while iteratie < max_iter:
        impachetare_vecin=vecin(impachetare_curenta,rnd)
        (vecinValoare,vecinMarime)=total_valoare_marime(impachetare_vecin,valori,marimi,marime_maxima)
        # Mai bine accepta vecin
        if vecinValoare > valoare_curenta:
            impachetare_curenta=impachetare_vecin;
            valoare_curenta=vecinValoare;
        #Impachetarea vecina nu este o solutie buna
        else:
            probabilitateDeAcceptareVecin=np.exp((vecinValoare-valoare_curenta)/temperatura_curenta)
            p=rnd.random()
            #Accepta totusi vecin cu impachetare mai slaba
            if p < probabilitateDeAcceptareVecin:
                impachetare_curenta=impachetare_vecin
                valoare_curenta=vecinValoare
        
        if iteratie%interval==0:
            print("iteratia: %6d : Valoare impachetare curenta (%7.0f) la temperatura (%10.2f)" % (iteratie,valoare_curenta,temperatura_curenta))
        
        if temperatura_curenta < 0.00001:
            temperatura_curenta=0.00001
        else:
            temperatura_curenta*=alpha
            iteratie +=1
    
    return impachetare_curenta


def main():
    valori=([])
    marimi=([])
    print("\n Problema rucsacului folosind Simulated Annealing")
    print("Goal-ul este de a maximiza valoarea obiectelor la marimea maxima impusa.")

    print("\nInitial problema are urmatoarele seturi de date definite")
    print("\n Numarul de obiecte - 10 ")
    print("\n Valori: 79, 32, 47, 18, 26, 85, 33, 40, 45, 59 ")
    print("\n Marimi: 85, 26, 48, 21, 22, 95, 43, 45, 55, 52 ")
    print("\n Marimea maxima - 101 ")  
    numarObiecte=10
    inputAlegereSetDeDate= input("\nDoresti sa schimbi aceste valori? Daca nu, scrie 'nu', daca da, scrie orice.\n")
    if(inputAlegereSetDeDate=="nu"):
        valori=np.array([79, 32, 47, 18, 26, 85, 33, 40, 45, 59])
        marimi = np.array([85, 26, 48, 21, 22, 95, 43, 45, 55, 52])
        marime_maxima = 101

        print("\Valoare obiecte: ")
        print(valori)
        print("\Marime obiecte: ")
        print(marimi)
        print("\nMarimea maxima admisa a rucsacului = %d " % marime_maxima)
    else:
        numarObiecte=int(input("\nIntrodu cate obiecte sa aiba rucsacul: "))
        for i in range(numarObiecte):
            valori.append(float(input("\nValoare["+str(i)+"] ")))
            marimi.append(float(input("\nMarime["+str(i)+"] ")))
        marime_maxima=int(input("\n Introdu marimea maxima a rucsacului: "))
        


        print("\Valoare obiecte: ")
        print(valori)
        print("\Marime obiecte: ")
        print(marimi)
        print("\nMarimea maxima admisa a rucsacului = %d " % marime_maxima)

    rnd=np.random.RandomState(5)
    max_iter=1000
    temperatura_start=10000.0
    alpha=0.98

    print("\nSetari:")
    print("Iteratie maxima = %d " % max_iter)
    print("Temperatura de start= %0.1f " % temperatura_start)
    print("Alpha = %0.2f " % alpha)

    print("\nIncepe rezolvarea problemei rucsacului cu valorile date. ")
    impachetare=rezolv_SA(numarObiecte,rnd,valori,marimi,marime_maxima,max_iter,temperatura_start,alpha)
    print("\nRezolvarea a luat sfarsit!!!")
    print("\nCea mai buna impachetare gasita este: ")
    print(impachetare)
    (v,s) = total_valoare_marime(impachetare, valori, marimi, marime_maxima)
    print("\nValoarea totala a impachetarii = %0.1f " % v)
    print("Marimea totala a impachetarii = %0.1f " % s)

    print("\nIncheiere program.")


if __name__ == "__main__":
  main()
