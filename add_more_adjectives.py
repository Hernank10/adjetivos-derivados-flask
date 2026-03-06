import json

# Cargar el JSON actual
with open('data/adjectives.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

adjectives = data['adjectives']
current_ids = [a['id'] for a in adjectives]
next_id = max(current_ids) + 1

# Adjetivos adicionales (26-50)
more_adjectives = [
    {
        "id": next_id + i,
        "adjective": adj[0],
        "base": adj[1],
        "suffix": adj[2],
        "difficulty": adj[3],
        "classification": adj[4],
        "subcategory": adj[5],
        "example": adj[6],
        "explanation": adj[7],
        "hint": adj[8]
    }
    for i, adj in enumerate([
        # id 26-30
        ("ruidoso", "ruido", "oso", "basic", "calificativo", "posesión",
         "El motor de ese coche es muy ruidoso.",
         "Que hace ruido o produce mucho ruido.",
         "Que se escucha fuerte"),
        ("esperanzador", "esperanzar", "dor", "advanced", "calificativo", "cualidad",
         "Las noticias sobre la cura son esperanzadoras.",
         "Que da esperanza o infunde esperanza.",
         "Te hace sentir optimismo"),
        ("arenoso", "arena", "oso", "basic", "calificativo", "posesión",
         "El fondo del río es arenoso.",
         "Que tiene arena o está cubierto de arena.",
         "Como la playa"),
        ("informativo", "informar", "ivo", "intermediate", "calificativo", "capacidad",
         "El folleto contiene material informativo.",
         "Que sirve para informar o dar información.",
         "Da datos y noticias"),
        ("argentino", "Argentina", "ino", "intermediate", "relacional", "origen",
         "El tango argentino es famoso en todo el mundo.",
         "Natural de Argentina o perteneciente a este país.",
         "Del país del tango"),
        # id 31-35
        ("doloroso", "dolor", "oso", "basic", "calificativo", "posesión",
         "La inyección fue muy dolorosa.",
         "Que causa dolor.",
         "Duele mucho"),
        ("tropical", "trópico", "al", "intermediate", "relacional", "lugar",
         "Las frutas tropicales son deliciosas.",
         "Perteneciente o relativo a los trópicos.",
         "De zonas cálidas"),
        ("alcohólico", "alcohol", "ico", "intermediate", "relacional", "sustancia",
         "Las bebidas alcohólicas no son para menores.",
         "Que contiene alcohol.",
         "Tiene una sustancia que embriaga"),
        ("huesudo", "hueso", "udo", "advanced", "calificativo", "posesión",
         "El perro callejero estaba muy huesudo.",
         "Que tiene muchos huesos o estos se notan mucho.",
         "Se le marcan los huesos"),
        ("cultural", "cultura", "al", "intermediate", "relacional", "campo",
         "El museo organiza actividades culturales.",
         "Perteneciente o relativo a la cultura.",
         "Relacionado con el arte y las tradiciones"),
        # id 36-40
        ("hambriento", "hambre", "iento", "advanced", "calificativo", "posesión",
         "Los niños hambrientos comieron rápidamente.",
         "Que tiene mucha hambre.",
         "Quiere comer"),
        ("eléctrico", "electricidad", "ico", "intermediate", "relacional", "energía",
         "El coche eléctrico contamina menos.",
         "Que funciona con electricidad.",
         "Funciona con corriente"),
        ("cobrizo", "cobre", "izo", "advanced", "calificativo", "semejanza",
         "El atardecer tenía tonos cobrizos.",
         "Que tiene color de cobre.",
         "Color rojizo metálico"),
        ("sediento", "sed", "iento", "advanced", "calificativo", "posesión",
         "Después de correr, estaba muy sediento.",
         "Que tiene mucha sed.",
         "Necesita agua"),
        ("democrático", "democracia", "ico", "advanced", "relacional", "política",
         "Las elecciones son un proceso democrático.",
         "Perteneciente o relativo a la democracia.",
         "Del gobierno del pueblo"),
        # id 41-45
        ("olvidadizo", "olvidar", "izo", "advanced", "calificativo", "tendencia",
         "Mi abuelo es un poco olvidadizo.",
         "Que se olvida de las cosas con facilidad.",
         "No recuerda bien"),
        ("metálico", "metal", "ico", "intermediate", "relacional", "material",
         "El sonido metálico provenía del taller.",
         "Perteneciente o relativo al metal.",
         "Del material de las latas"),
        ("rojizo", "rojo", "izo", "intermediate", "calificativo", "semejanza",
         "El cielo al atardecer se volvió rojizo.",
         "Que tira a rojo o tiene aspecto rojo.",
         "Color como la sangre pero más suave"),
        ("familiar", "familia", "ar", "basic", "relacional", "grupo",
         "La reunión familiar será el domingo.",
         "Perteneciente o relativo a la familia.",
         "De padres, hijos y abuelos"),
        ("gigantesco", "gigante", "esco", "advanced", "calificativo", "semejanza",
         "El edificio era de proporciones gigantescas.",
         "De tamaño muy grande, como un gigante.",
         "Muy, muy grande"),
        # id 46-50
        ("sonriente", "sonreír", "nte", "intermediate", "calificativo", "acción",
         "La niña sonriente saludó a todos.",
         "Que sonríe.",
         "Que muestra felicidad con la boca"),
        ("cristalino", "cristal", "ino", "advanced", "calificativo", "semejanza",
         "El agua de la montaña es cristalina.",
         "Que es claro y transparente como el cristal.",
         "Se ve a través"),
        ("asustadizo", "asustar", "izo", "advanced", "calificativo", "tendencia",
         "El gato es muy asustadizo.",
         "Que se asusta con facilidad.",
         "Se asusta rápido"),
        ("espumoso", "espuma", "oso", "intermediate", "calificativo", "posesión",
         "La cerveza tiene una capa espumosa.",
         "Que tiene o produce espuma.",
         "Hace burbujas"),
        ("polvoriento", "polvo", "iento", "advanced", "calificativo", "posesión",
         "El libro viejo estaba polvoriento.",
         "Cubierto de polvo.",
         "Tiene tierra fina encima")
    ])
]

# Agregar nuevos adjetivos
adjectives.extend(more_adjectives)

# Guardar el archivo actualizado
with open('data/adjectives.json', 'w', encoding='utf-8') as f:
    json.dump({"adjectives": adjectives}, f, ensure_ascii=False, indent=2)

print(f"✅ Se agregaron {len(more_adjectives)} adjetivos nuevos")
print(f"✅ Total ahora: {len(adjectives)} adjetivos")
