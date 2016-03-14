#coding=utf-8
from IPython.display import SVG, display, Image
import graphviz as gv

class relacion:
    """
    Esta es la clase relación
    Attributes:
        rels el conjunto de tuplas que componen la relación
        universo el conjunto sobre el que está definida la relación
        cero definido para relaciones de orden con un mínimo
        uno definido para relaciones de orden con un máximo
    """
    def __init__(self, l, uni=set({})):
        """
        Crea una relación binaria (finita) a partir de una lista de parejas (tuplas) y de un universo (opcional).
        Si el universo no se especifica, entonces se tomará como tal la unión de todas las entradas de las parejas de la relación.

        Args:
            l un conjunto de pares (tuplas)
            uni (opcional) un conjunto donde pertenecen las entradas de las tuplas
        Example:
            >>> r = relacion({(1,2),(2,3)}, {1,2,3,4})
            >>> print(r)
            {(1, 2), (2, 3)} en el conjunto {1, 2, 3, 4}
            >>> r
            Relación binaria
            >>> r(2,3)
            True
            >>> r(1,3)
            False
        """
        if not(isinstance(l,set)):
            raise TypeError("La entrada debe ser un conjunto de parejas")
        if not(all(isinstance(t,tuple) and len(t)==2 for t in l)):
            raise TypeError("La entrada debe ser un conjunto de parejas")
        u = set([])
        for t in l:
            u = u.union(set(t))
        if len(uni)>0:
            if not(u <= uni):
                raise ValueError("Hay pares cuyas entradas no están en el universo dado")
            self.universo = uni
        else:
            self.universo = u
        self.rels = l

    def __repr__(self):
        return "Relación binaria"

    def __str__(self):
        return str(self.rels)+" en el conjunto "+str(self.universo)

    def __call__(self, a, b):
        return self.rel(a,b)

    def es_reflexiva(self):
        """
        Determina si la relación binaria es reflexiva
        """
        return all((a,a) in self.rels for a in self.universo)

    def es_simetrica(self):
        """
        Determina si la relación binaria es simétrica
        """
        return all((t[1],t[0]) in self.rels for t in self.rels)

    def es_transitiva(self):
        """
        Determina si la relación binaria es transitiva
        """
        return all((t[0],s[1]) in self.rels for t in self.rels for s in self.rels if t[1]==s[0])

    def es_antisimetrica(self):
        """
        Determina si la relación binaria es antisimétrica
        """
        return all(t[0]==t[1] for t in self.rels if (t[1],t[0]) in self.rels)

    def es_total(self):
        """
        Determina si la relación binaria es total (o lineal; dados dos elementos o el primero está relacionado con el segundo o viceversa)
        """
        return all((((a,b) in self.rels) or ((b,a) in self.rels)) for a in self.universo for b in self.universo if a!=b)

    def es_equivalencia(self):
        """
        Determina si la relación binaria es reflexiva, transitiva y simétrica
        """
        return self.es_reflexiva() and self.es_simetrica() and self.es_transitiva()

    def es_orden(self):
        """
        Determina si la relación binaria es reflexiva, transitiva y antisimétrica
        """
        return self.es_reflexiva() and self.es_antisimetrica() and self.es_transitiva()

    def es_orden_total(self):
        """
        Determina si la relación binaria es de orden total (o lineal)
        """
        return self.es_orden() and self.es_total()

    def rel(self,a,b):
        """
        Determina si dos elementos están relacionados por la relación
        """
        return (a,b) in self.rels

    def clases_equivalencia(self):
        """
        Calcula las clases de equivalencia (si es relación de equivalencia)
        """
        uu = self.universo.copy()
        cl = set({})
        while len(uu)>0:
            a = uu.pop()
            ca = set(b for b in self.universo if (a,b) in self.rels)
            uu.difference_update(ca)
            cl.add(frozenset(ca))
        return cl

    def pinta(self, l=None):
        """
        Dibuja los elementos del universo y las relaciones entre éstos
        """
        g=gv.Digraph(format='svg')
        g.attr('graph', rankdir='BT')
        if l!=None:
            if not(l<=self.universo):
                raise ValueError("Los nodos seleccionados no están en el universo de la relación")
            g.attr('node', shape='doublecircle')
            for x in l:
                g.node(str(x))
            g.attr('node', shape='circle')
            for x in self.universo.difference(l):
                g.node(str(x))
        else:
            for x in self.universo:
                g.node(str(x))
        for t in self.rels:
            g.edge(str(t[0]),str(t[1]))
        salida= g.render()
        display(SVG(salida))
        return salida

    def hasse(self):
        """
        Dibuja el diagrama de Hasse asociado a la relación
        """
        rs = set(t for t in self.rels if t[0]!=t[1])
        rsm = set(t for t in self.rels if any(((t[0],x) in rs) and ((x,t[1]) in rs) for x in self.universo))
        g = gv.Graph(format='svg')
        for x in self.universo:
            g.node(str(x))
        for t in rs.difference(rsm):
            g.edge(str(t[1]),str(t[0]))
        salida= g.render()
        display(SVG(salida))
        return relacion(rs.difference(rsm))

    def maximales(self, l):
        """
        Calcula los elementos maximales del conjunto dado (si la relación es de orden)
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in l if set(b for b in l if self.rel(a,b))==set({a}))

    def minimales(self, l):
        """
        Calcula los elementos minimales del conjunto dado (si la relación es de orden)
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in l if set(b for b in l if self.rel(b,a))==set({a}))

    def mayorantes(self, l):
        """
        Calcula los elementos mayorantes del conjunto dado (si la relación es de orden), a saber, aquellos que están por encima de todos los elementos del conjunto dado
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in self.universo if all(self.rel(b,a) for b in l))

    def minorantes(self, l):
        """
        Calcula los elementos minorantes del conjunto dado (si la relación es de orden), a saber, aquellos que están por debajo de todos los elementos del conjunto dado
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in self.universo if all(self.rel(a,b) for b in l))

    def maximo(self,l):
        """
        Calcula el máximo del conjunto dado (si es una relación de orden); en caso de no existir devuelve None
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.maximales(l)
        if len(m)!=1:
            return None
        return list(m)[0]

    def minimo(self,l):
        """
        Calcula el mínimo del conjunto dado (si es una relación de orden); en caso de no existir devuelve None
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.minimales(l)
        if len(m)!=1:
            return None
        return list(m)[0]

    def infimo(self,l):
        """
        Calcula el ínfimo del conjunto dado (si es una relación de orden); en caso de no existir devuelve None
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.minorantes(l)
        return self.maximo(m)

    def supremo(self,l):
        """
        Calcula el supremo del conjunto dado (si es una relación de orden); en caso de no existir devuelve None
        """
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.mayorantes(l)
        return self.minimo(m)

    def es_reticulo_superior(self):
        """
        Determina si cualesquiera dos elemetos tienen supremo
        """
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        u = self.universo
        return all(self.supremo(set({a,b}))!=None for a in u for b in u  )

    def es_reticulo_inferior(self):
        """
        Determina si cualesquiera dos elemetos tienen ínfimo
        """
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        u = self.universo
        return all(self.infimo(set({a,b}))!=None for a in u for b in u  )

    def es_reticulo(self):
        """
        Decide si el conjunto con la relación dada es un retículo
        """
        return self.es_reticulo_inferior() and self.es_reticulo_superior()

    def complemento(self,a):
        """
        Calcula el complemento de un elemento (si es que es una relación de orden con máximo y mínimo); devuelve None si no existe
        """
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        try:
            cero = self.cero
        except AttributeError:
            cero = self.minimo(self.universo)
            if cero==None:
                raise TypeError("El universo no tiene mínimo")
            self.cero = cero

        try:
            uno = self.uno
        except AttributeError:
            uno = self.maximo(self.universo)
            if uno==None:
                raise TypeError("El universo no tiene máximo")
            self.uno = uno

        for x in self.universo:
            par=set({x,a})
            if self.infimo(par)==cero and self.supremo(par)==uno:
                return x
        return None
    def es_complementado(self):
        """
        Determina si todo elemento tiene complemento
        """
        return all(self.complemento(a)!=None for a in self.universo)

    def es_distributivo(self):
        """
        Determina si el conjunto con las operaciones supremo e ínfimo es distributivo
        """
        if not(self.es_reticulo()):
            return False
        un = self.universo
        if any(self.supremo({a,self.infimo({b,c})})!=self.infimo({self.supremo({a,b}),self.supremo({a,c})}) for a in un for b in un for c in un):
            return False
        #if any(self.infimo(a,self.supremo(b,c))!=self.supremo(self.infimo(a,b),self.infimo(a,c)) for a in un for b in un for c in un):
        #    return False # no es necesaria, basta una de las distributivas
        return True

    def es_algebra_Boole(self):
        """
        Decide si el conjunto con las operaciones supremo e ínfimo es un Álgebra de Boole
        """
        return self.es_distributivo() and self.es_complementado()

    def atomos(self):
        """
        Calcula los átomos del álgebra de Boole; aunque en realidad calcula los elementos minimales del conjunto resultante al quitar el cero (mínimo)
        """
        try:
            cero = self.cero
        except AttributeError:
            cero = self.minimo(self.universo)
            if cero==None:
                raise TypeError("El universo no tiene mínimo")
            self.cero = cero

        un = self.universo.copy()
        un.remove(cero)
        return self.minimales(un)

    def coatomos(self):
        """
        Calcula los coátomos del álgebra de Boole; aunque en realidad calcula los elementos maximales del conjunto resultante al quitar el uno (máximo)
        """
        try:
            uno = self.uno
        except AttributeError:
            uno = self.maximo(self.universo)
            if uno==None:
                raise TypeError("El universo no tiene máximo")
            self.uno = uno

        un = self.universo.copy()
        un.remove(uno)
        return self.maximales(un)

    def es_subreticulo(self,l):
        """
        Determina si los elementos del conjunto l son un subretículo
        """
        if not(self.es_reticulo()):
            raise ValueError("El conjunto con la relación dada no es un retículo")
        return all(self.supremo({a,b}) in l for a in l for b in l) and all(self.infimo({a,b}) in l for a in l for b in l)

    def es_subalgebra(self,l):
        """
        Determina si los elementos del conjunto l son un subálgebra de Boole
        """
        if not(self.es_algebra_Boole()):
            raise ValueError("El conjunto con la relación dada no es un álgebra de Boole")

        if not(self.es_subreticulo(l)):
            return False
        if not(self.cero in l and self.uno in l):
            return False
        return all(self.complemento(a) in l for a in l)

def identidad(l):
    """
    Define la relación identidad sobre un conjunto dado
    """
    if not(isinstance(l,s)):
        raise TypeError("El argumento debe ser un conjunto")

    ll = set((a,a) for a in l)
    return relacion(ll)

def divisores(n):
    """
    Define el conjunto de divisores de n con la relación de divisibilidad, si n es un entero
    En caso de que n sea un conjunto enteros, hace lo mismo pero con los elementos de n
    """
    if isinstance(n,int) and n>0:
        u = set(a for a in range(1,n+1) if n%a==0)
        return relacion(set((a,b) for a in u for b in u if b%a==0),u)
    if isinstance(n,set) and all(isinstance(x,int) for x in n):
        u = n.copy()
        return relacion(set((a,b) for a in u for b in u if b==0 or (a!=0 and b%a==0)))

    raise TypeError("El argumento debe ser un entero positivo o bien un conjunto de enteros")
