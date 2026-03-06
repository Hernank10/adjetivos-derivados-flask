import json

# Cargar el JSON actual
with open('data/adjectives.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

adjectives = data['adjectives']
current_ids = [a['id'] for a in adjectives]
next_id = max(current_ids) + 1

# Adjetivos adicionales (51-75)
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
        # id 51-55
        ("brillante", "brillar", "nte", "intermediate", "calificativo", "acción",
         "Las estrellas brillantes iluminaban la noche.",
         "Que brilla o tiene brillo.",
         "Da luz"),
        ("cerámico", "cerámica", "ico", "advanced", "relacional", "material",
         "Los azulejos cerámicos son resistentes.",
         "Perteneciente o relativo a la cerámica.",
         "De barro cocido"),
        ("dormilón", "dormir", "ón", "intermediate", "calificativo", "tendencia",
         "Mi gato es muy dormilón.",
         "Que duerme mucho.",
         "Le gusta estar en la cama"),
        ("misterioso", "misterio", "oso", "intermediate", "calificativo", "posesión",
         "La casa abandonada tenía un aire misterioso.",
         "Que tiene misterio o lo sugiere.",
         "Difícil de entender o explicar"),
        ("barbudo", "barba", "udo", "advanced", "calificativo", "posesión",
         "El personaje del cuento era un anciano barbudo.",
         "Que tiene mucha barba.",
         "Tiene pelo en la cara"),
        # id 56-60
        ("veloz", "velocidad", "oz", "advanced", "calificativo", "cualidad",
         "El guepardo es un animal muy veloz.",
         "Que se mueve con mucha velocidad.",
         "Muy rápido"),
        ("lluvioso", "lluvia", "oso", "basic", "calificativo", "posesión",
         "Abril es un mes lluvioso en mi ciudad.",
         "Donde llueve mucho o abunda la lluvia.",
         "Cae mucha agua del cielo"),
        ("poderoso", "poder", "oso", "intermediate", "calificativo", "posesión",
         "El mago era muy poderoso.",
         "Que tiene mucho poder o influencia.",
         "Tiene mucha fuerza o autoridad"),
        ("infantil", "infante", "il", "intermediate", "relacional", "grupo",
         "La literatura infantil es muy variada.",
         "Perteneciente o relativo a los niños.",
         "Para niños"),
        ("amigable", "amigo", "ble", "intermediate", "calificativo", "capacidad",
         "El recepcionista fue muy amigable.",
         "Que muestra amistad o es fácil de tratar.",
         "Hace amigos fácilmente"),
        # id 61-65
        ("cerdoso", "cerda", "oso", "advanced", "calificativo", "posesión",
         "El jabalí tiene un pelaje cerdoso.",
         "Que tiene cerdas o es áspero como ellas.",
         "Pelo duro como el del cerdo"),
        ("montañoso", "montaña", "oso", "intermediate", "calificativo", "posesión",
         "El paisaje montañoso era impresionante.",
         "Que tiene montañas o está lleno de ellas.",
         "Con muchas elevaciones"),
        ("resbaladizo", "resbalar", "izo", "advanced", "calificativo", "tendencia",
         "El suelo mojado estaba resbaladizo.",
         "Que hace resbalar o es fácil de resbalar.",
         "Difícil mantenerse de pie"),
        ("quebradizo", "quebrar", "izo", "advanced", "calificativo", "tendencia",
         "El vidrio es un material quebradizo.",
         "Que se quiebra o rompe con facilidad.",
         "Se rompe fácilmente"),
        ("asustador", "asustar", "dor", "intermediate", "calificativo", "cualidad",
         "La película de terror era muy asustadora.",
         "Que asusta o causa miedo.",
         "Da miedo"),
        # id 66-70
        ("confianzudo", "confianza", "udo", "advanced", "calificativo", "tendencia",
         "No seas tan confianzudo con los desconocidos.",
         "Que se toma demasiada confianza.",
         "Se pasa de confiado"),
        ("oloroso", "olor", "oso", "intermediate", "calificativo", "posesión",
         "Las flores olorosas alegraban el jardín.",
         "Que tiene olor, especialmente agradable.",
         "Tiene aroma"),
        ("plateado", "plata", "ado", "intermediate", "calificativo", "semejanza",
         "El coche nuevo era de color plateado.",
         "De color plata o parecido a la plata.",
         "Color brillante como la plata"),
        ("grasiento", "grasa", "iento", "advanced", "calificativo", "posesión",
         "El mecánico tenía las manos grasientas.",
         "Cubierto de grasa.",
         "Tiene aceite o grasa"),
        ("famoso", "fama", "oso", "basic", "calificativo", "posesión",
         "El actor famoso saludaba a sus fans.",
         "Que tiene fama o es conocido por muchos.",
         "Lo conoce mucha gente"),
        # id 71-75
        ("orgulloso", "orgullo", "oso", "intermediate", "calificativo", "posesión",
         "Estaba orgulloso de sus logros.",
         "Que siente orgullo.",
         "Se siente bien por algo"),
        ("asqueroso", "asco", "oso", "intermediate", "calificativo", "posesión",
         "La comida en mal estado era asquerosa.",
         "Que causa asco.",
         "Da náuseas"),
        ("venenoso", "veneno", "oso", "intermediate", "calificativo", "posesión",
         "Algunas setas son venenosas.",
         "Que contiene veneno.",
         "Puede matar si se ingiere"),
        ("bondadoso", "bondad", "oso", "intermediate", "calificativo", "posesión",
         "El anciano bondadoso ayudaba a todos.",
         "Que tiene bondad.",
         "Es bueno con los demás"),
        ("valioso", "valor", "oso", "intermediate", "calificativo", "posesión",
         "El cuadro era muy valioso.",
         "Que tiene mucho valor.",
         "Vale mucho dinero")
    ])
]

# Agregar nuevos adjetivos
adjectives.extend(more_adjectives)

# Guardar el archivo actualizado
with open('data/adjectives.json', 'w', encoding='utf-8') as f:
    json.dump({"adjectives": adjectives}, f, ensure_ascii=False, indent=2)

print(f"✅ Se agregaron {len(more_adjectives)} adjetivos nuevos")
print(f"✅ Total ahora: {len(adjectives)} adjetivos")
