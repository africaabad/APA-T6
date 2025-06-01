import re

def normalizaHoras(fitxerEntrada, fitxerSortida):
    # Llista de patrons regex i funcions per transformar expressions horàries
    formats_hora = [
        # Format HH:MM
        (r'\b(\d{1,2}):(\d{2})\b', lambda h, m: f'{int(h):02}:{int(m):02}' if 0 <= int(h) < 24 and 0 <= int(m) < 60 else f'{h}:{m}'),

        # Format amb lletres: 9h45m
        (r'\b(\d{1,2})h(\d{1,2})m\b', lambda h, m: f'{int(h):02}:{int(m):02}' if 0 <= int(h) < 24 and 0 <= int(m) < 60 else f'{h}h{m}m'),

        # Format simple amb h: 6h
        (r'\b(\d{1,2})h\b', lambda h: f'{int(h):02}:00' if 0 <= int(h) < 24 else f'{h}h'),

        # Expressions verbals típiques de la tarda
        (r'\b(\d{1,2}) y media de la tarde\b', lambda h: f'{(int(h) + 12) % 24:02}:30'),
        (r'\b(\d{1,2}) y cuarto de la tarde\b', lambda h: f'{(int(h) + 12) % 24:02}:15'),
        (r'\b(\d{1,2}) menos cuarto de la tarde\b', lambda h: f'{(int(h) + 11) % 24:02}:45'),

        # Hora del matí amb h
        (r'\b(\d{1,2})h de la mañana\b', lambda h: f'{int(h) % 12:02}:00'),

        # Mitjanit
        (r'\b12 de la noche\b', lambda: '00:00'),

        # Expressions genèriques
        (r'\b(\d{1,2}) en punto\b', lambda h: f'{int(h) % 12 or 12:02}:00'),
        (r'\b(\d{1,2}) y media\b', lambda h: f'{int(h) % 12 or 12:02}:30'),
        (r'\b(\d{1,2}) y cuarto\b', lambda h: f'{int(h) % 12 or 12:02}:15'),
        (r'\b(\d{1,2}) menos cuarto\b', lambda h: f'{(int(h) - 1) % 12 or 12:02}:45'),
    ]

    # Obrim els fitxers
    with open(fitxerEntrada, 'r', encoding='utf-8') as origen, open(fitxerSortida, 'w', encoding='utf-8') as desti:
        for linia in origen:
            linia_original = linia
            for patron, transformador in formats_hora:
                def substitut(match):
                    try:
                        return transformador(*match.groups())
                    except:
                        return match.group(0)  # Retorna el text original si hi ha error
                linia = re.sub(patron, substitut, linia)
            desti.write(linia)

if __name__ == "__main__":
    normalizaHoras("horas.txt", "hores_normalitzades.txt")
