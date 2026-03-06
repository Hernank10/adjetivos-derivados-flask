import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"

def test_flashcards_api():
    """Probar la API de flashcards"""
    
    print("🔍 Probando API de flashcards...")
    
    # 1. Obtener estadísticas de adjetivos
    print("\n1. Obteniendo estadísticas generales...")
    response = requests.get(f"{BASE_URL}/api/adjectives/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Total adjetivos: {data['total']}")
        print(f"   📊 Por dificultad: {data['by_difficulty']}")
    else:
        print(f"   ❌ Error: {response.status_code}")
    
    # 2. Iniciar sesión de flashcards
    print("\n2. Iniciando sesión de flashcards...")
    payload = {
        "difficulty": "all",
        "mode": "learn",
        "count": 5
    }
    response = requests.post(f"{BASE_URL}/api/flashcards/start", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Sesión iniciada: {data['total']} tarjetas")
        print(f"   🃏 Primera tarjeta: {data['first_card']['base']}")
    else:
        print(f"   ❌ Error: {response.status_code}")
    
    # 3. Obtener una tarjeta específica
    print("\n3. Obteniendo tarjeta 0...")
    response = requests.get(f"{BASE_URL}/api/flashcards/card/0")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Tarjeta cargada: {data['base']} → {data['adjective']}")
        print(f"   📝 Explicación: {data['explanation'][:50]}...")
    else:
        print(f"   ❌ Error: {response.status_code}")
    
    print("\n✨ Prueba completada!")

if __name__ == "__main__":
    test_flashcards_api()
