"""
Author: Filippo Badalamenti
Python Version: 3.6.3
Summary: Il nostro modulo riceve le dimensioni degli alberi passate come parametri da terminale,
        poi verranno creati gli AVL stessi con valori generati (randomicamente o sequenzialmente)
        da due insiemi con valori tutti uno minori dell'altro. A questo punto abbiamo due
        strade per concatenare gli alberi:
        1) fare l'insert su quello di dimensione maggiore delle chiavi del più piccolo.
            T(n) = O(m*log(n)), con m e n il numero di chiavi dei due alberi.
        2) sfruttare il fatto che le chiavi di uno siano minori dell'altro, "affiancare" gli
            alberi ed utilizzare un nodo dell'albero con altezza minore per collegarli, e poi
            risalire fino alla radice per controllare il bilanciamento dell'albero.
            T(n) = O(log(n)), ovvero il tempo di scendere in profondità nell'albero maggiore.
"""

from dictionaryAVL import DictAVL
from time import time
from random import randint
import sys

def seqList(dim, dim_prevAVL):
    """Costruisco la lista che conterrà i valori, tutti diversi o uguali a seconda della variabile tmp scelta"""

    lis = []
    for i in range(0, dim):
        tmp = (i + dim_prevAVL, i + dim_prevAVL) # per semplicità di debug utilizzo gli stessi valori per key e value
        #tmp = (0,0) # per generare degli alberi con tutte le key (e quindi i value) uguali
        lis.append(tmp)
    #print(lis)
    return(lis)

def randList(dim,minValue,maxValue):
    """Costruisco la lista che conterrà i valori per l'AVL, generati a caso in un intervallo dato."""

    assert dim > 0 , "Dimensione dell'albero negativa o nulla, scegliere un intero positivo"

    lis = []
    for i in range(0, dim):
        n = randint(minValue, maxValue)
        tmp = (n, n) # tupla dato che non dobbiamo modificarla prima della creazione dell'albero
        lis.append(tmp)
    #print(lis)
    return lis

def randAVL(lis):
    """Con la lista passata, andiamo a creare un AVL per successivi inserimenti"""

    newAVL = DictAVL()
    # Creazione dell'albero date le liste di key-value
    for elem in lis:
        newAVL.insert(elem[0], elem[1])
    #newAVL.tree.stampa()
    return newAVL


def concatenation_dummy(avl_1,avl_2):
    """Con questa funzione andiamo ad unire gli alberi aggiungendo
        la coppia chiave-valore dell'albero di altezza minore
        (per risparmiare un po' di passaggi)"""

    # Vediamo quale albero sia più grande
    if avl_2.height(avl_2.tree.root) >= avl_1.height(avl_1.tree.root):
        avl_max, avl_min = avl_2, avl_1
    else:
        avl_max, avl_min = avl_1, avl_2

    # Inserisco gli elementi di un'albero nell'altro
    lis = avl_min.tree.DFS()
    for elem in lis:
        avl_max.insert(elem[0], elem[1])

    # Stampiamo l'albero bilanciato.
    #avl_max.tree.stampa()


def concatenation(avl_lit, avl_big):
    """In questa funzione, determiniamo l'altezza degli alberi: fatto ciò, andiamo a
    chiamare una delle funzioni in base al rapporto d'altezza tra i due alberi."""
    if avl_big.height(avl_big.tree.root) > avl_lit.height(avl_lit.tree.root):
        less_more_height(avl_lit,avl_big)
    elif avl_big.height(avl_big.tree.root) == avl_lit.height(avl_lit.tree.root):
        equal_height(avl_lit,avl_big)
    else:
        more_less_height(avl_lit,avl_big)


def less_more_height(avl_lit, avl_big):
    """Caso in cui l'albero a chiavi minori è il più piccolo"""

    maxSon = avl_lit.maxKeySon(avl_lit.tree.root)
    avl_lit.deleteNode(maxSon) #abbiamo cancellato il nodo maggiore e bilanciato
    #avl_lit.tree.stampa()
    print('') # per separare il print di più alberi
    tmp_nodeTree = DictAVL() # la foglia maggiore delle chiavi minori
    tmp_nodeTree.insert(maxSon.info[0], maxSon.info[1])
    #tmp_nodeTree.tree.stampa()
    #print('')

    rad = avl_big.tree.root
    while True:
        if avl_big.height(rad) > (avl_lit.height(avl_lit.tree.root) + 1):
            rad = rad.leftSon
        else:
            tmp_bigTreeSonLeft = avl_big.tree.cutLeft(rad) # sottoalbero delle chiavi maggiori
            avl_big.tree.insertAsLeftSubTree(rad,tmp_nodeTree.tree) # inserisco solo nodo foglia
            avl_big.tree.insertAsLeftSubTree(rad.leftSon,avl_lit.tree) # aggiungo AVL con chiavi minori a quello che prima era il massimo
            avl_big.tree.insertAsRightSubTree(rad.leftSon,tmp_bigTreeSonLeft) # aggiungo l'AVL tagliato in precedenza
            break

    # Una volta inseriti i nuovi rami, iniziamo a bilanciare verso l'alto
    rad = rad.leftSon
    while rad != None:
        avl_big.updateHeight(rad)
        avl_big.rotate(rad)
        rad = rad.father

    #Stampiamo l'albero bilanciato
    #avl_big.tree.stampa()

def equal_height(avl_lit, avl_big):
    """Caso in cui i due alberi hanno la stessa altezza"""

    maxSon = avl_lit.maxKeySon(avl_lit.tree.root)
    avl_lit.deleteNode(maxSon)  # abbiamo cancellato il nodo maggiore e bilanciato
    tmp_nodeTree = DictAVL()  # la foglia maggiore delle chiavi minori
    tmp_nodeTree.insert(maxSon.info[0], maxSon.info[1])

    # Uniamo i due alberi come due sottoalberi
    tmp_nodeTree.tree.root.leftSon = avl_lit.tree.root
    tmp_nodeTree.tree.root.rightSon = avl_big.tree.root
    avl_lit.tree.root.father, avl_big.tree.root.father  = tmp_nodeTree.tree.root , tmp_nodeTree.tree.root

    rad = tmp_nodeTree.tree.root.leftSon
    while rad != None:
        avl_big.updateHeight(rad)
        avl_big.rotate(rad)
        rad = rad.father

    # Stampiamo l'albero bilanciato
    #tmp_nodeTree.tree.stampa()

def more_less_height(avl_lit, avl_big):
    """Caso in cui l'albero a chiavi minori è il più grande"""

    minSon = avl_big.minKeySon(avl_big.tree.root)
    avl_big.deleteNode(minSon)  # abbiamo cancellato il nodo minore e bilanciato
    tmp_nodeTree = DictAVL()  # la foglia maggiore delle chiavi minori
    tmp_nodeTree.insert(minSon.info[0], minSon.info[1])

    rad = avl_lit.tree.root
    while True:
        if avl_lit.height(rad) > (avl_big.height(avl_big.tree.root) + 1):
            rad = rad.rightSon
        else:
            tmp_litTreeSonRight = avl_lit.tree.cutRight(rad)  # sotto albero delle chiavi minori
            avl_lit.tree.insertAsRightSubTree(rad, tmp_nodeTree.tree)  # inserisco solo nodo foglia
            avl_lit.tree.insertAsRightSubTree(rad.rightSon, avl_big.tree)  # aggiungo avl con chiavi maggiori a quello che prima era il minimo
            avl_lit.tree.insertAsLeftSubTree(rad.leftSon, tmp_litTreeSonRight)  # aggiungo l'avl prima tagliato in precedenza
            break

    # Una volta inseriti i nuovi rami, iniziamo a bilanciare verso l'alto
    rad = rad.rightSon
    while rad != None:
        avl_lit.updateHeight(rad)
        avl_lit.rotate(rad)
        rad = rad.father

    # Stampiamo l'albero bilanciato
    #avl_lit.tree.stampa()


if __name__ == "__main__":
    # Nei test si può andare ad inserire le dimensioni in 'progettoDemo/Edit Configuration/Parameters'
    if len(sys.argv) != 3:
        print("Inserisci la dimensione (int) dei due alberi AVL")
    else:
        # Passando delle stringhe, dobbiamo fare il casting per riconvertirli ad interi

        # con seqList generiamo una lista di elementi tutti diversi (o uguali)
        list_tree1 = seqList(int(sys.argv[1]), 0)
        list_tree2 = seqList(int(sys.argv[2]), int(sys.argv[1]))

        # con randList generiamo una lista di elementi di chiave random
        #list_tree1 = randList(int(sys.argv[1]), 1, 500)
        #list_tree2 = randList(int(sys.argv[2]), 501 , 1000)

        tree_lit = randAVL(list_tree1)
        tree_big = randAVL(list_tree2)

        print("AVL creati. Dimensioni:\nAVL chiavi minori: {} nodi.\nAVL chiavi maggiori: {} nodi.\n".format(sys.argv[1],sys.argv[2]))

        tree_lit.tree.stampa()
        print('')
        tree_big.tree.stampa()

        if tree_lit.tree.root.info[2] == 0 or tree_big.tree.root.info[2] == 0:
        # facciamo solo concatenation_dummy, avendo meno passaggi sarà più rapida

            start = time()
            concatenation_dummy(tree_lit, tree_big)
            elapsed = time() - start
            print("Tempo concatenation_dummy: {} secondi.".format(elapsed))

        else:
            # essendo gli AVL basati su puntatori, creiamone una coppia per ogni algoritmo
            tree_lit_copy = randAVL(list_tree1)
            tree_big_copy = randAVL(list_tree2)

            # Stampo il tempo impiegato da entrambi gli algoritmi

            start = time()
            concatenation_dummy(tree_lit,tree_big)
            elapsed = time() - start
            print("Tempo concatenation_dummy: {} secondi.".format(elapsed))

            #dummy = elapsed	# usato per la raccolta dati con Excel

            start = time()
            concatenation(tree_lit_copy, tree_big_copy)
            elapsed = time() - start
            print("Tempo concatenation: {} secondi.".format(elapsed))
            
            #print("\n\nFor Excel")
            #print("{} {}".format(dummy,elapsed))	#usati per la raccolta dati rapida con Excel