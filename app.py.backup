from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones_flashcards_2024'

# Cargar adjetivos desde JSON
def load_adjectives():
    try:
        with open('data/adjectives.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['adjectives']
    except FileNotFoundError:
        print("❌ Error: No se encuentra el archivo data/adjectives.json")
        return []
    except json.JSONDecodeError:
        print("❌ Error: El archivo JSON no es válido")
        return []

adjectives = load_adjectives()

# Base de datos de resultados (en memoria)
results = []

# Mapa de dificultades
difficulty_map = {
    "basic": "Básico",
    "intermediate": "Intermedio",
    "advanced": "Avanzado"
}

# Mapa de sufijos para referencia rápida
suffix_map = {
    "oso": "Indica posesión o abundancia",
    "ivo": "Indica capacidad o tendencia",
    "ar": "Relación o pertenencia",
    "ble": "Indica posibilidad o capacidad",
    "ario": "Perteneciente o relativo a",
    "dor": "Que realiza la acción",
    "ísimo": "Grado superlativo o extremo",
    "eño": "Origen o procedencia",
    "ico": "Relativo a ciencia o arte",
    "al": "Relación o pertenencia",
    "ado": "Semejanza o parecido",
    "ino": "Origen o procedencia",
    "udo": "Exceso o abundancia",
    "iento": "Presencia intensa",
    "izo": "Tendencia o propensión",
    "nte": "Que realiza la acción",
    "ón": "Aumentativo o tendencia",
    "oz": "Cualidad intensa",
    "il": "Relativo a grupo"
}

@app.route('/')
def index():
    """Página principal con resumen del curso"""
    return render_template('index.html', 
                         total_adjectives=len(adjectives),
                         difficulty_map=difficulty_map)

@app.route('/learn')
def learn():
    """Página de aprendizaje con todos los adjetivos"""
    difficulty = request.args.get('difficulty', 'all')
    classification = request.args.get('classification', 'all')
    
    filtered = adjectives
    if difficulty != 'all':
        filtered = [a for a in filtered if a['difficulty'] == difficulty]
    if classification != 'all':
        filtered = [a for a in filtered if a['classification'] == classification]
    
    return render_template('learn.html', 
                         adjectives=filtered,
                         difficulty_map=difficulty_map,
                         suffix_map=suffix_map,
                         current_difficulty=difficulty,
                         current_classification=classification)

@app.route('/flashcards')
def flashcards():
    """Página principal de flashcards"""
    return render_template('flashcards.html', 
                         difficulty_map=difficulty_map,
                         total_cards=len(adjectives))

@app.route('/api/flashcards/start', methods=['POST'])
def start_flashcards():
    """API para iniciar sesión de flashcards"""
    data = request.json
    difficulty = data.get('difficulty', 'all')
    mode = data.get('mode', 'learn')
    count = int(data.get('count', 20))
    
    # Filtrar según dificultad
    if difficulty == 'all':
        deck = adjectives.copy()
    elif difficulty == 'basic':
        deck = [a for a in adjectives if a['difficulty'] == 'basic']
    elif difficulty == 'intermediate':
        deck = [a for a in adjectives if a['difficulty'] == 'intermediate']
    else:
        deck = [a for a in adjectives if a['difficulty'] == 'advanced']
    
    # Limitar número de tarjetas
    if len(deck) > count:
        deck = random.sample(deck, count)
    
    # Mezclar el mazo
    random.shuffle(deck)
    
    # Guardar en sesión
    session['flashcards'] = {
        'deck': deck,
        'current_index': 0,
        'mode': mode,
        'remembered': [],
        'forgotten': []
    }
    
    return jsonify({
        'total': len(deck),
        'first_card': {
            'id': deck[0]['id'],
            'base': deck[0]['base'],
            'adjective': deck[0]['adjective'],
            'index': 0
        }
    })

@app.route('/flashcards/session')
def flashcards_session():
    """Página de sesión de flashcards"""
    if 'flashcards' not in session:
        return redirect(url_for('flashcards'))
    return render_template('flashcards_session.html')

@app.route('/api/flashcards/card/<int:index>')
def get_card(index):
    """API para obtener una tarjeta específica"""
    flashcards = session.get('flashcards')
    if not flashcards or index >= len(flashcards['deck']):
        return jsonify({'error': 'Tarjeta no encontrada'}), 404
    
    card = flashcards['deck'][index]
    return jsonify({
        'id': card['id'],
        'base': card['base'],
        'adjective': card['adjective'],
        'suffix': card['suffix'],
        'explanation': card['explanation'],
        'example': card['example'],
        'hint': card.get('hint', ''),
        'difficulty': card['difficulty'],
        'classification': card['classification'],
        'subcategory': card['subcategory'],
        'index': index,
        'total': len(flashcards['deck'])
    })

@app.route('/api/flashcards/response', methods=['POST'])
def record_flashcard_response():
    """API para registrar respuesta de flashcard"""
    data = request.json
    flashcards = session.get('flashcards')
    
    if not flashcards:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    index = data['index']
    remembered = data['remembered']
    card = flashcards['deck'][index]
    
    # Registrar resultado
    record = {
        'card_id': card['id'],
        'base': card['base'],
        'remembered': remembered,
        'time': datetime.now().isoformat()
    }
    
    if remembered:
        flashcards['remembered'].append(record)
    else:
        flashcards['forgotten'].append(record)
    
    session['flashcards'] = flashcards
    
    return jsonify({
        'success': True,
        'remembered_count': len(flashcards['remembered']),
        'forgotten_count': len(flashcards['forgotten']),
        'completed': len(flashcards['remembered']) + len(flashcards['forgotten']) == len(flashcards['deck'])
    })

@app.route('/api/flashcards/next')
def next_flashcard():
    """API para obtener siguiente tarjeta no respondida"""
    flashcards = session.get('flashcards')
    if not flashcards:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    total_answered = len(flashcards['remembered']) + len(flashcards['forgotten'])
    
    if total_answered >= len(flashcards['deck']):
        return jsonify({'completed': True})
    
    return jsonify({'next_index': total_answered})

@app.route('/api/flashcards/stats')
def get_flashcard_stats():
    """API para obtener estadísticas de la sesión actual"""
    flashcards = session.get('flashcards')
    if not flashcards:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    return jsonify({
        'remembered': len(flashcards['remembered']),
        'forgotten': len(flashcards['forgotten']),
        'total': len(flashcards['deck']),
        'percentage': round((len(flashcards['remembered']) / len(flashcards['deck'])) * 100) if flashcards['deck'] else 0
    })

@app.route('/api/flashcards/review')
def review_flashcards():
    """API para obtener tarjetas olvidadas para repasar"""
    flashcards = session.get('flashcards')
    if not flashcards:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    forgotten_ids = [r['card_id'] for r in flashcards['forgotten']]
    forgotten_cards = [c for c in adjectives if c['id'] in forgotten_ids]
    
    return jsonify({
        'cards': forgotten_cards,
        'count': len(forgotten_cards)
    })

@app.route('/adjetivo/<int:adjective_id>')
def adjective_detail(adjective_id):
    """Página detallada de un adjetivo específico"""
    adjective = next((a for a in adjectives if a['id'] == adjective_id), None)
    if adjective:
        # Encontrar adjetivos relacionados (mismo sufijo o clasificación)
        related = [a for a in adjectives if a['id'] != adjective_id and 
                  (a['suffix'] == adjective['suffix'] or 
                   a['classification'] == adjective['classification'])][:3]
        return render_template('adjective_detail.html', 
                             adjective=adjective, 
                             related=related,
                             difficulty_map=difficulty_map,
                             suffix_map=suffix_map)
    return redirect(url_for('learn'))

@app.route('/practice')
def practice():
    """Página de configuración de práctica"""
    return render_template('practice_setup.html', 
                         difficulty_map=difficulty_map)

@app.route('/api/practice/start', methods=['POST'])
def start_practice():
    """API para iniciar una sesión de práctica"""
    data = request.json
    difficulty = data.get('difficulty', 'basic')
    question_count = int(data.get('question_count', 10))
    
    # Filtrar preguntas según dificultad
    if difficulty == 'basic':
        pool = [a for a in adjectives if a['difficulty'] in ['basic', 'intermediate']]
    elif difficulty == 'intermediate':
        pool = [a for a in adjectives if a['difficulty'] == 'intermediate']
    else:
        pool = adjectives
    
    # Seleccionar preguntas aleatorias
    selected = random.sample(pool, min(question_count, len(pool)))
    
    # Guardar en sesión
    session['practice'] = {
        'questions': [{'id': a['id'], 'base': a['base'], 
                      'correct_suffix': a['suffix']} for a in selected],
        'current_index': 0,
        'answers': [],
        'score': 0,
        'difficulty': difficulty,
        'start_time': datetime.now().isoformat()
    }
    
    return jsonify({
        'total': len(selected),
        'first_question': {
            'base': selected[0]['base'],
            'index': 0
        }
    })

@app.route('/practice/session')
def practice_session():
    """Página de sesión de práctica activa"""
    if 'practice' not in session:
        return redirect(url_for('practice'))
    return render_template('practice_session.html')

@app.route('/api/practice/question/<int:index>')
def get_question(index):
    """API para obtener una pregunta específica"""
    practice = session.get('practice')
    if not practice or index >= len(practice['questions']):
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    
    question = practice['questions'][index]
    return jsonify({
        'base': question['base'],
        'index': index,
        'total': len(practice['questions'])
    })

@app.route('/api/practice/answer', methods=['POST'])
def submit_answer():
    """API para enviar una respuesta"""
    data = request.json
    practice = session.get('practice')
    
    if not practice:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    index = data['index']
    answer = data['answer']
    
    question = practice['questions'][index]
    is_correct = answer == question['correct_suffix']
    
    # Guardar respuesta
    answer_record = {
        'question_index': index,
        'base': question['base'],
        'user_answer': answer,
        'correct_answer': question['correct_suffix'],
        'is_correct': is_correct
    }
    practice['answers'].append(answer_record)
    
    if is_correct:
        practice['score'] += 1
    
    # Si es la última pregunta, guardar resultado
    if len(practice['answers']) == len(practice['questions']):
        result = {
            'date': datetime.now().isoformat(),
            'difficulty': practice['difficulty'],
            'score': practice['score'],
            'total': len(practice['questions']),
            'percentage': round((practice['score'] / len(practice['questions'])) * 100)
        }
        results.append(result)
    
    session['practice'] = practice
    
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question['correct_suffix'],
        'score': practice['score'],
        'completed': len(practice['answers']) == len(practice['questions'])
    })

@app.route('/api/practice/next')
def next_question():
    """API para obtener el índice de la siguiente pregunta no respondida"""
    practice = session.get('practice')
    if not practice:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    answered_indices = [a['question_index'] for a in practice['answers']]
    for i in range(len(practice['questions'])):
        if i not in answered_indices:
            return jsonify({'next_index': i})
    
    return jsonify({'completed': True})

@app.route('/results')
def results_page():
    """Página de resultados históricos"""
    return render_template('results.html', 
                         results=results,
                         difficulty_map=difficulty_map)

@app.route('/api/results/clear', methods=['POST'])
def clear_results():
    """API para limpiar resultados"""
    global results
    results = []
    return jsonify({'success': True})

@app.route('/api/adjectives/stats')
def adjective_stats():
    """API para obtener estadísticas de adjetivos"""
    stats = {
        'total': len(adjectives),
        'by_difficulty': {
            'basic': len([a for a in adjectives if a['difficulty'] == 'basic']),
            'intermediate': len([a for a in adjectives if a['difficulty'] == 'intermediate']),
            'advanced': len([a for a in adjectives if a['difficulty'] == 'advanced'])
        },
        'by_classification': {
            'calificativo': len([a for a in adjectives if a['classification'] == 'calificativo']),
            'relacional': len([a for a in adjectives if a['classification'] == 'relacional'])
        }
    }
    return jsonify(stats)

@app.route('/api/flashcards/suffix/<suffix>')
def get_suffix_cards(suffix):
    """API para obtener tarjetas por sufijo"""
    suffix_cards = [a for a in adjectives if a['suffix'] == suffix]
    return jsonify({
        'suffix': suffix,
        'explanation': suffix_map.get(suffix, ''),
        'cards': suffix_cards,
        'count': len(suffix_cards)
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 INICIANDO APLICACIÓN FLASK")
    print("=" * 50)
    print(f"📚 Adjetivos cargados: {len(adjectives)}")
    print(f"📊 Básicos: {len([a for a in adjectives if a['difficulty'] == 'basic'])}")
    print(f"📊 Intermedios: {len([a for a in adjectives if a['difficulty'] == 'intermediate'])}")
    print(f"📊 Avanzados: {len([a for a in adjectives if a['difficulty'] == 'advanced'])}")
    print(f"🔑 Sufijos diferentes: {len(set([a['suffix'] for a in adjectives]))}")
    print("=" * 50)
    print("🌐 Servidor disponible en:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Codespaces: Puerto 5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF
