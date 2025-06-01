class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'

import re 

def leeAlumnos(ficAlumnos):
    """
    Lee el fichero de texto que se le pasa como único 
    argumento y devuelve un diccionario con los datos de los alumnos.
    
    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumn = {}
    expr_id = r'\s*(?P<id>\d+)\s+'
    expr_nom = r'(?P<nom>[\w\s]+?)\s+'
    expr_notes = r'(?P<notes>[\d.\s]+)\s*'
    expresion = re.compile(expr_id + expr_nom + expr_notes) # más manejable
    # expresion = re.compile(r'\s*\d+\s+[\w\s]+[\d.]+\s*') # r:regular. s:space. d: *:cero o mas veces. +una o mas veces
    # expresion = re.compile(r'\s*(?P<id>\d+)\s+(?P<nom>[\w\s]+?)\s+(?P<nota>[\d.\s]+)\s*') # r:regular. s:space. d: *:cero o mas veces. +una o mas veces
    # abrir un archivo con gestor de contenido
    with open(ficAlumnos, 'rt', encoding='utf-8') as fpAlumnos: 
        for linea in fpAlumnos:
            match = expresion.match(linea.strip())
            # match = expresion.search(linea)
            if match is not None: 
                # id = int(match.group(1))
                # nom = match.group(2).strip()
                # notes = list(map(float, re.split(r'\s+', match.group(3).strip())))
                id = int(match['id'])
                nom = match['nom']
                notes = [float(nota) for nota in match['notes'].split()]
                alumn[nom] = Alumno(nom, id, notes)
    return alumn

resultado = leeAlumnos('alumnos.txt')
print(resultado)

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
    
