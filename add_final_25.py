import json

# Cargar el JSON actual
with open('data/adjectives.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

adjectives = data['adjectives']
current_ids = [a['id'] for a in adjectives]
next_id = max(current_ids) + 1

# Últimos 25 adjetivos (76-100)
final_adjectives = [
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
        # id 76-80
        ("jugoso", "jugo", "oso", "basic", "calificativo", "posesión",
         "La naranja estaba muy jugosa.",
         "Que tiene mucho jugo.",
         "Tiene líquido"),
        ("milenario", "milenio", "ario", "advanced", "relacional", "tiempo",
         "Es una tradición milenaria.",
         "Que tiene miles de años.",
         "Muy, muy antiguo"),
        ("tembloroso", "temblor", "oso", "intermediate", "calificativo", "posesión",
         "El perro estaba tembloroso por el frío.",
         "Que tiembla o tiene temblores.",
         "Se mueve sin control"),
        ("bondadoso", "bondad", "oso", "intermediate", "calificativo", "posesión",
         "El anciano bondadoso ayudaba a todos.",
         "Que tiene bondad.",
         "Es bueno con los demás"),
        ("valioso", "valor", "oso", "intermediate", "calificativo", "posesión",
         "El cuadro era muy valioso.",
         "Que tiene mucho valor.",
         "Vale mucho dinero"),
        # id 81-85
        ("juguetón", "jugar", "ón", "intermediate", "calificativo", "tendencia",
         "El cachorro era muy juguetón.",
         "Que juega mucho o le gusta jugar.",
         "Le gusta divertirse"),
        ("cambiante", "cambiar", "nte", "intermediate", "calificativo", "acción",
         "El clima en esta región es cambiante.",
         "Que cambia con frecuencia.",
         "No es estable"),
        ("dependiente", "depender", "nte", "intermediate", "calificativo", "acción",
         "Es muy dependiente de sus padres.",
         "Que depende de algo o alguien.",
         "Necesita ayuda"),
        ("sonoro", "sonido", "oro", "intermediate", "calificativo", "cualidad",
         "El grito fue muy sonoro.",
         "Que produce sonido o se escucha bien.",
         "Se escucha fuerte"),
        ("gigantesco", "gigante", "esco", "advanced", "calificativo", "semejanza",
         "El edificio era gigantesco.",
         "De tamaño enorme.",
         "Muy, muy grande"),
        # id 86-90
        ("ceroso", "cera", "oso", "intermediate", "calificativo", "semejanza",
         "La superficie tenía aspecto ceroso.",
         "Parecido a la cera.",
         "Como una vela"),
        ("pastoso", "pasta", "oso", "intermediate", "calificativo", "semejanza",
         "La mezcla quedó muy pastosa.",
         "Con consistencia de pasta.",
         "Como masa"),
        ("arenisco", "arena", "isco", "advanced", "calificativo", "semejanza",
         "El terreno era arenisco.",
         "Que tiene arena o parece arena.",
         "Como la playa"),
        ("pedregoso", "piedra", "oso", "intermediate", "calificativo", "posesión",
         "El camino era pedregoso.",
         "Lleno de piedras.",
         "Con muchas rocas"),
        ("cenagoso", "ciénaga", "oso", "advanced", "calificativo", "posesión",
         "El terreno cenagoso era peligroso.",
         "Que tiene ciénaga o pantano.",
         "Lleno de barro"),
        # id 91-95
        ("calizo", "cal", "izo", "advanced", "calificativo", "semejanza",
         "El suelo calizo es blanquecino.",
         "Que contiene cal o parece cal.",
         "De roca blanca"),
        ("ferroso", "hierro", "oso", "advanced", "calificativo", "posesión",
         "El agua tenía sabor ferroso.",
         "Que contiene hierro.",
         "Con metal"),
        ("cuadrangular", "cuadrángulo", "ar", "advanced", "relacional", "forma",
         "El edificio tenía forma cuadrangular.",
         "Con forma de cuadrángulo.",
         "Cuatro lados"),
        ("triangular", "triángulo", "ar", "intermediate", "relacional", "forma",
         "El instrumento musical es triangular.",
         "Con forma de triángulo.",
         "Tres lados"),
        ("circular", "círculo", "ar", "basic", "relacional", "forma",
         "La mesa era circular.",
         "Con forma de círculo.",
         "Redondo"),
        # id 96-100
        ("piloso", "pelo", "oso", "advanced", "calificativo", "posesión",
         "El brazo piloso del hombre.",
         "Que tiene pelo o vello.",
         "Con vello"),
        ("escamoso", "escama", "oso", "advanced", "calificativo", "posesión",
         "El pez tenía la piel escamosa.",
         "Que tiene escamas.",
         "Como los peces"),
        ("granulado", "gránulo", "ado", "intermediate", "calificativo", "semejanza",
         "El azúcar granulada es más fina.",
         "En forma de gránulos.",
         "Como granos pequeños"),
        ("lobulado", "lóbulo", "ado", "advanced", "calificativo", "forma",
         "La hoja tenía forma lobulada.",
         "Que tiene lóbulos.",
         "Con partes redondeadas"),
        ("festivo", "fiesta", "ivo", "intermediate", "calificativo", "cualidad",
         "Mañana es un día festivo.",
         "De celebración o fiesta.",
         "Día de celebración")
    ])
]

# Agregar nuevos adjetivos
adjectives.extend(final_adjectives)

# Guardar el archivo actualizado
with open('data/adjectives.json', 'w', encoding='utf-8') as f:
    json.dump({"adjectives": adjectives}, f, ensure_ascii=False, indent=2)

print(f"✅ Se agregaron {len(final_adjectives)} adjetivos nuevos")
print(f"✅ Total ahora: {len(adjectives)} adjetivos (100 completos)")

# Mostrar estadísticas finales
basic = len([a for a in adjectives if a['difficulty'] == 'basic'])
intermediate = len([a for a in adjectives if a['difficulty'] == 'intermediate'])
advanced = len([a for a in adjectives if a['difficulty'] == 'advanced'])
calificativo = len([a for a in adjectives if a['classification'] == 'calificativo'])
relacional = len([a for a in adjectives if a['classification'] == 'relacional'])
suffixes = len(set([a['suffix'] for a in adjectives]))

print(f"\n📊 Estadísticas finales:")
print(f"   - Básicos: {basic}")
print(f"   - Intermedios: {intermediate}")
print(f"   - Avanzados: {advanced}")
print(f"   - Calificativos: {calificativo}")
print(f"   - Relacionales: {relacional}")
print(f"   - Sufijos diferentes: {suffixes}")
