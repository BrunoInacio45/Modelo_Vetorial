def uniao(lst):
    lstaux = []
    for i in lst:                                                                       #Faz a uniao entre duas listas
        for j in i:
            if j not in lstaux:
                lstaux.append(j)

    return lstaux


lista = [[1,2],[2,3]]
print(uniao(lista))