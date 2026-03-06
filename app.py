from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_super_segura_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    practices = db.relationship('Practice', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Práctica
class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    mode = db.Column(db.String(50), nullable=False)  # 'standard', 'timed', 'marathon'
    difficulty = db.Column(db.String(50), nullable=False)  # 'mixed', 'basic', 'intermediate', 'advanced'
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_spent = db.Column(db.Integer)  # segundos totales
    details = db.Column(db.Text)  # JSON con detalles de cada respuesta
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%d/%m/%Y %H:%M'),
            'mode': self.mode,
            'difficulty': self.difficulty,
            'score': self.score,
            'total': self.total_questions,
            'percentage': self.percentage,
            'time_spent': self.time_spent
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear tablas
with app.app_context():
    db.create_all()

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

# Mapa de dificultades
difficulty_map = {
    "basic": "Básico",
    "intermediate": "Intermedio",
    "advanced": "Avanzado"
}

# Mapa de sufijos
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

# Rutas de autenticación
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('register'))
        
        # Crear usuario
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso. ¡Bienvenido!', 'success')
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # Estadísticas del usuario
    practices = Practice.query.filter_by(user_id=current_user.id).order_by(Practice.date.desc()).all()
    
    total_practices = len(practices)
    total_questions = sum(p.total_questions for p in practices)
    total_correct = sum(p.score for p in practices)
    avg_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    # Práctica más reciente
    last_practice = practices[0] if practices else None
    
    # Distribución por dificultad
    by_difficulty = {
        'basic': sum(1 for p in practices if p.difficulty == 'basic'),
        'intermediate': sum(1 for p in practices if p.difficulty == 'intermediate'),
        'advanced': sum(1 for p in practices if p.difficulty == 'advanced'),
        'mixed': sum(1 for p in practices if p.difficulty == 'mixed')
    }
    
    return render_template('profile.html',
                         user=current_user,
                         practices=practices,
                         total_practices=total_practices,
                         total_questions=total_questions,
                         total_correct=total_correct,
                         avg_percentage=round(avg_percentage, 1),
                         last_practice=last_practice,
                         by_difficulty=by_difficulty)

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html', 
                         total_adjectives=len(adjectives),
                         difficulty_map=difficulty_map,
                         user=current_user if current_user.is_authenticated else None)

@app.route('/learn')
def learn():
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
                         current_classification=classification,
                         user=current_user if current_user.is_authenticated else None)

@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html', 
                         difficulty_map=difficulty_map,
                         total_cards=len(adjectives),
                         user=current_user if current_user.is_authenticated else None)

@app.route('/practice')
def practice():
    return render_template('practice_setup.html', 
                         difficulty_map=difficulty_map,
                         user=current_user if current_user.is_authenticated else None)

@app.route('/practice/session')
@login_required
def practice_session():
    return render_template('practice_session.html')

@app.route('/api/practice/save', methods=['POST'])
@login_required
def save_practice():
    data = request.json
    
    practice = Practice(
        user_id=current_user.id,
        mode=data['mode'],
        difficulty=data['difficulty'],
        score=data['score'],
        total_questions=data['total'],
        percentage=data['percentage'],
        time_spent=data.get('time_spent', 0),
        details=json.dumps(data.get('details', []))
    )
    
    db.session.add(practice)
    db.session.commit()
    
    return jsonify({'success': True, 'practice_id': practice.id})

@app.route('/results')
@login_required
def results_page():
    practices = Practice.query.filter_by(user_id=current_user.id).order_by(Practice.date.desc()).all()
    return render_template('results.html', 
                         practices=[p.to_dict() for p in practices],
                         user=current_user)

@app.route('/api/practice/start', methods=['POST'])
@login_required
def start_practice():
    data = request.json
    difficulty = data.get('difficulty', 'mixed')
    question_count = int(data.get('count', 10))
    
    # Filtrar según dificultad
    if difficulty == 'mixed':
        pool = adjectives
    elif difficulty == 'basic':
        pool = [a for a in adjectives if a['difficulty'] == 'basic']
    elif difficulty == 'intermediate':
        pool = [a for a in adjectives if a['difficulty'] == 'intermediate']
    else:
        pool = [a for a in adjectives if a['difficulty'] == 'advanced']
    
    # Seleccionar preguntas aleatorias
    selected = random.sample(pool, min(question_count, len(pool)))
    
    # Guardar en sesión
    session['practice'] = {
        'questions': [{'id': a['id'], 'base': a['base'], 
                      'correct_suffix': a['suffix'],
                      'hint': a.get('hint', ''),
                      'difficulty': a['difficulty']} for a in selected],
        'mode': data.get('mode', 'standard'),
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

@app.route('/api/practice/question/<int:index>')
@login_required
def get_question(index):
    practice = session.get('practice')
    if not practice or index >= len(practice['questions']):
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    
    question = practice['questions'][index]
    return jsonify({
        'base': question['base'],
        'hint': question.get('hint', ''),
        'difficulty': question['difficulty'],
        'index': index,
        'total': len(practice['questions'])
    })

@app.route('/api/practice/answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    practice = session.get('practice')
    
    if not practice:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    index = data['index']
    answer = data['answer']
    response_time = data.get('response_time', 0)
    
    question = practice['questions'][index]
    is_correct = answer == question['correct_suffix']
    
    # Guardar respuesta en sesión
    if 'answers' not in practice:
        practice['answers'] = []
    
    practice['answers'].append({
        'question_index': index,
        'base': question['base'],
        'user_answer': answer,
        'correct_answer': question['correct_suffix'],
        'is_correct': is_correct,
        'response_time': response_time
    })
    
    session['practice'] = practice
    
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question['correct_suffix'],
        'completed': len(practice['answers']) == len(practice['questions'])
    })

@app.route('/api/practice/next')
@login_required
def next_question():
    practice = session.get('practice')
    if not practice:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    answered_indices = [a['question_index'] for a in practice.get('answers', [])]
    for i in range(len(practice['questions'])):
        if i not in answered_indices:
            return jsonify({'next_index': i})
    
    return jsonify({'completed': True})

@app.route('/api/adjectives/stats')
def adjective_stats():
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

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 INICIANDO APLICACIÓN FLASK CON AUTENTICACIÓN")
    print("=" * 50)
    print(f"📚 Adjetivos cargados: {len(adjectives)}")
    print(f"👥 Base de datos: usuarios.db")
    print("=" * 50)
    print("🌐 Servidor disponible en:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Codespaces: Puerto 5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
