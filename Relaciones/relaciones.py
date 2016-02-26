#coding=utf-8
from IPython.display import SVG, display, Image
import graphviz as gv

class relacion:
    def __init__(self, l, uni=set({})):
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
        return str(self.rels)

    def __call__(self, a, b):
        return self.rel(a,b)

    def es_reflexiva(self):
        return all((a,a) in self.rels for a in self.universo)

    def es_simetrica(self):
        return all((t[1],t[0]) in self.rels for t in self.rels)

    def es_transitiva(self):
        return all((t[0],s[1]) in self.rels for t in self.rels for s in self.rels if t[1]==s[0])

    def es_antisimetrica(self):
        return all(t[0]==t[1] for t in self.rels if (t[1],t[0]) in self.rels)

    def es_total(self):
        return all((((a,b) in self.rels) or ((b,a) in self.rels)) for a in self.universo for b in self.universo if a!=b)

    def es_equivalencia(self):
        return self.es_reflexiva() and self.es_simetrica() and self.es_transitiva()

    def es_orden(self):
        return self.es_reflexiva() and self.es_antisimetrica() and self.es_transitiva()

    def es_orden_total(self):
        return self.es_orden() and self.es_total()

    def rel(self,a,b):
        return (a,b) in self.rels

    def clases_equivalencia(self):
        uu = self.universo.copy()
        cl = set({})
        while len(uu)>0:
            a = uu.pop()
            ca = set(b for b in self.universo if (a,b) in self.rels)
            uu.difference_update(ca)
            cl.add(frozenset(ca))
        return cl

    def pinta(self, l=None):
        g=gv.Digraph(format='svg')
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
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in l if set(b for b in l if self.rel(a,b))==set({a}))

    def minimales(self, l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in l if set(b for b in l if self.rel(b,a))==set({a}))

    def mayorantes(self, l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in self.universo if all(self.rel(b,a) for b in l))

    def minorantes(self, l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        return set(a for a in self.universo if all(self.rel(a,b) for b in l))

    def maximo(self,l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.maximales(l)
        if len(m)!=1:
            return None
        return list(m)[0]

    def minimo(self,l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.minimales(l)
        if len(m)!=1:
            return None
        return list(m)[0]

    def infimo(self,l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.minorantes(l)
        return self.maximo(m)

    def supremo(self,l):
        if not(l<=self.universo):
            raise TypeError("El argumento debe ser un subconjunto del universo de la relación")
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        m=self.mayorantes(l)
        return self.minimo(m)

    def es_reticulo_superior(self):
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        u = self.universo
        return all(self.supremo(set({a,b}))!=None for a in u for b in u  )

    def es_reticulo_inferior(self):
        if not(self.es_orden()):
            raise TypeError("La relación no es de orden")
        u = self.universo
        return all(self.infimo(set({a,b}))!=None for a in u for b in u  )

    def es_reticulo(self):
        return self.es_reticulo_inferior() and self.es_reticulo_superior()

    def complemento(self,a):
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

        return all(self.complemento(a)!=None for a in self.universo)

    def es_distributivo(self):
        if not(self.es_reticulo()):
            return False
        un = self.universo
        if any(self.supremo({a,self.infimo({b,c})})!=self.infimo({self.supremo({a,b}),self.supremo({a,c})}) for a in un for b in un for c in un):
            return False
        #if any(self.infimo(a,self.supremo(b,c))!=self.supremo(self.infimo(a,b),self.infimo(a,c)) for a in un for b in un for c in un):
        #    return False # no es necesaria, basta una de las distributivas
        return True

    def es_Algebra_Boole(self):
        return self.es_distributivo() and self.es_complementado()

    def atomos(self):
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

def identidad(l):
    if not(isinstance(l,s)):
        raise TypeError("El argumento debe ser un conjunto")

    ll = set((a,a) for a in l)
    return relacion(ll)
