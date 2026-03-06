// Clase principal para manejar las flashcards
class FlashcardManager {
    constructor() {
        this.currentCard = null;
        this.sessionData = null;
        this.currentIndex = 0;
        this.stats = {
            remembered: 0,
            forgotten: 0,
            total: 0
        };
    }

    // Iniciar nueva sesión
    async startSession(difficulty, mode, count) {
        try {
            const response = await fetch('/api/flashcards/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    difficulty: difficulty,
                    mode: mode,
                    count: count
                })
            });
            
            this.sessionData = await response.json();
            this.stats.total = this.sessionData.total;
            return this.sessionData;
        } catch (error) {
            console.error('Error starting session:', error);
            throw error;
        }
    }

    // Cargar una tarjeta específica
    async loadCard(index) {
        try {
            const response = await fetch(`/api/flashcards/card/${index}`);
            this.currentCard = await response.json();
            this.currentIndex = index;
            return this.currentCard;
        } catch (error) {
            console.error('Error loading card:', error);
            throw error;
        }
    }

    // Registrar respuesta
    async recordResponse(remembered) {
        try {
            const response = await fetch('/api/flashcards/response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    index: this.currentIndex,
                    remembered: remembered
                })
            });
            
            const data = await response.json();
            
            if (remembered) {
                this.stats.remembered++;
            } else {
                this.stats.forgotten++;
            }
            
            return data;
        } catch (error) {
            console.error('Error recording response:', error);
            throw error;
        }
    }

    // Obtener siguiente tarjeta
    async getNextCard() {
        try {
            const response = await fetch('/api/flashcards/next');
            return await response.json();
        } catch (error) {
            console.error('Error getting next card:', error);
            throw error;
        }
    }

    // Obtener estadísticas actuales
    async getStats() {
        try {
            const response = await fetch('/api/flashcards/stats');
            return await response.json();
        } catch (error) {
            console.error('Error getting stats:', error);
            throw error;
        }
    }

    // Obtener tarjetas para repasar
    async getReviewCards() {
        try {
            const response = await fetch('/api/flashcards/review');
            return await response.json();
        } catch (error) {
            console.error('Error getting review cards:', error);
            throw error;
        }
    }

    // Calcular progreso
    getProgress() {
        const answered = this.stats.remembered + this.stats.forgotten;
        return {
            answered: answered,
            total: this.stats.total,
            percentage: Math.round((answered / this.stats.total) * 100) || 0
        };
    }

    // Calcular puntuación
    getScore() {
        return {
            remembered: this.stats.remembered,
            forgotten: this.stats.forgotten,
            percentage: Math.round((this.stats.remembered / this.stats.total) * 100) || 0
        };
    }

    // Reiniciar sesión
    reset() {
        this.currentCard = null;
        this.sessionData = null;
        this.currentIndex = 0;
        this.stats = {
            remembered: 0,
            forgotten: 0,
            total: 0
        };
    }
}

// Utilidades para la UI
const FlashcardUI = {
    // Actualizar estadísticas en la UI
    updateStats(stats) {
        $('#rememberedCount').text(stats.remembered);
        $('#forgottenCount').text(stats.forgotten);
        
        const progress = ((stats.remembered + stats.forgotten) / stats.total) * 100;
        $('#progressBar').css('width', progress + '%');
        
        const currentCardNum = stats.remembered + stats.forgotten + 1;
        if (currentCardNum <= stats.total) {
            $('#currentCardCount').text(`${currentCardNum}/${stats.total}`);
            $('#progressText').text(`Tarjeta ${currentCardNum} de ${stats.total}`);
        }
    },

    // Mostrar tarjeta en la UI
    displayCard(card) {
        // Front de la tarjeta
        $('#baseWord').text(card.base);
        
        // Dificultad
        let difficultyClass = 'bg-secondary';
        let difficultyText = card.difficulty;
        switch(card.difficulty) {
            case 'basic':
                difficultyClass = 'badge-basic';
                difficultyText = 'Básico';
                break;
            case 'intermediate':
                difficultyClass = 'badge-intermediate';
                difficultyText = 'Intermedio';
                break;
            case 'advanced':
                difficultyClass = 'badge-advanced';
                difficultyText = 'Avanzado';
                break;
        }
        $('#cardDifficulty')
            .text(difficultyText)
            .removeClass()
            .addClass(`badge ${difficultyClass}`);
        
        // Clasificación
        $('#cardClassification').text(
            card.classification.charAt(0).toUpperCase() + 
            card.classification.slice(1)
        );
        
        $('#cardSubcategory').text(`Subcategoría: ${card.subcategory}`);
        
        // Back de la tarjeta
        $('#cardSuffix').text(`+${card.suffix}`);
        $('#adjectiveWord').text(card.adjective);
        $('#explanation').text(card.explanation);
        $('#example').text(`"${card.example}"`);
        
        if (card.hint) {
            $('#hint')
                .html(`<i class="fas fa-lightbulb"></i> ${card.hint}`)
                .show();
        } else {
            $('#hint').hide();
        }
        
        // Actualizar progreso
        $('#currentCardCount').text(`${card.index + 1}/${card.total}`);
        $('#progressText').text(`Tarjeta ${card.index + 1} de ${card.total}`);
    },

    // Mostrar resultados
    displayResults(score) {
        $('#finalRemembered').text(score.remembered);
        $('#finalForgotten').text(score.forgotten);
        $('#finalTotal').text(score.remembered + score.forgotten);
        $('#finalPercentage').text(score.percentage + '%');
        $('#finalProgressBar').css('width', score.percentage + '%');
        
        let message = '';
        let icon = '';
        
        if (score.percentage >= 90) {
            message = '¡Excelente! Dominas los adjetivos derivados.';
            icon = 'fa-crown';
        } else if (score.percentage >= 70) {
            message = '¡Muy bien! Sigue practicando para mejorar.';
            icon = 'fa-star';
        } else if (score.percentage >= 50) {
            message = 'Bien, pero necesitas más práctica.';
            icon = 'fa-smile';
        } else {
            message = 'Sigue estudiando, ¡tú puedes lograrlo!';
            icon = 'fa-book';
        }
        
        $('#finalMessage').html(`<i class="fas ${icon} me-2"></i>${message}`);
    },

    // Animar respuesta
    animateResponse(remembered) {
        const $card = $('#flashcard');
        $card.addClass(remembered ? 'pulse-success' : 'pulse-error');
        setTimeout(() => {
            $card.removeClass('pulse-success pulse-error');
        }, 500);
    },

    // Voltear tarjeta
    flipCard() {
        $('#flashcard').toggleClass('flipped');
    },

    // Resetear UI
    reset() {
        $('#setupSection').show();
        $('#sessionSection').hide();
        $('#resultsSection').hide();
        $('#flashcard').removeClass('flipped');
    },

    // Mostrar sección de sesión
    showSession() {
        $('#setupSection').hide();
        $('#sessionSection').show();
        $('#resultsSection').hide();
    },

    // Mostrar resultados
    showResults() {
        $('#setupSection').hide();
        $('#sessionSection').hide();
        $('#resultsSection').show();
    }
};

// Inicialización cuando el documento está listo
$(document).ready(function() {
    const manager = new FlashcardManager();
    let currentMode = 'learn';

    // Manejadores de eventos para los modos
    $('.mode-btn').click(function() {
        $('.mode-btn').removeClass('active');
        $(this).addClass('active');
        currentMode = $(this).data('mode');
    });

    // Iniciar sesión
    $('#startFlashcards').click(async function() {
        const difficulty = $('#difficultySelect').val();
        const count = parseInt($('#countSelect').val());
        
        $(this).prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i>Cargando...');
        
        try {
            await manager.startSession(difficulty, currentMode, count);
            const firstCard = await manager.loadCard(0);
            
            FlashcardUI.showSession();
            FlashcardUI.displayCard(firstCard);
            
            const stats = await manager.getStats();
            FlashcardUI.updateStats(stats);
        } catch (error) {
            alert('Error al iniciar la sesión. Por favor, intenta de nuevo.');
        } finally {
            $(this).prop('disabled', false).html('<i class="fas fa-play me-2"></i>Comenzar sesión');
        }
    });

    // Voltear tarjeta al hacer clic
    $('#flashcard').click(function() {
        FlashcardUI.flipCard();
    });

    $('#flipBtn').click(function() {
        FlashcardUI.flipCard();
    });

    // Recordar tarjeta
    $('#rememberBtn').click(async function() {
        $(this).prop('disabled', true);
        $('#forgetBtn').prop('disabled', true);
        
        try {
            await manager.recordResponse(true);
            FlashcardUI.animateResponse(true);
            
            const completed = manager.getProgress().answered === manager.stats.total;
            
            if (completed) {
                const score = manager.getScore();
                FlashcardUI.displayResults(score);
                FlashcardUI.showResults();
            } else {
                const next = await manager.getNextCard();
                if (next.next_index !== undefined) {
                    const nextCard = await manager.loadCard(next.next_index);
                    FlashcardUI.displayCard(nextCard);
                }
            }
            
            const stats = await manager.getStats();
            FlashcardUI.updateStats(stats);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            $(this).prop('disabled', false);
            $('#forgetBtn').prop('disabled', false);
        }
    });

    // No recordar tarjeta
    $('#forgetBtn').click(async function() {
        $(this).prop('disabled', true);
        $('#rememberBtn').prop('disabled', true);
        
        try {
            await manager.recordResponse(false);
            FlashcardUI.animateResponse(false);
            
            const completed = manager.getProgress().answered === manager.stats.total;
            
            if (completed) {
                const score = manager.getScore();
                FlashcardUI.displayResults(score);
                FlashcardUI.showResults();
            } else {
                const next = await manager.getNextCard();
                if (next.next_index !== undefined) {
                    const nextCard = await manager.loadCard(next.next_index);
                    FlashcardUI.displayCard(nextCard);
                }
            }
            
            const stats = await manager.getStats();
            FlashcardUI.updateStats(stats);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            $(this).prop('disabled', false);
            $('#rememberBtn').prop('disabled', false);
        }
    });

    // Siguiente tarjeta
    $('#nextBtn').click(async function() {
        $('#flashcard').removeClass('flipped');
        $(this).prop('disabled', true);
        
        try {
            const next = await manager.getNextCard();
            if (next.next_index !== undefined) {
                const nextCard = await manager.loadCard(next.next_index);
                FlashcardUI.displayCard(nextCard);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Nueva sesión
    $('#newSessionBtn, #newSessionBtn2').click(function() {
        manager.reset();
        FlashcardUI.reset();
    });

    // Repasar olvidadas
    $('#reviewForgottenBtn').click(async function() {
        try {
            const data = await manager.getReviewCards();
            if (data.count > 0) {
                alert(`Tienes ${data.count} tarjetas para repasar. Esta función estará disponible próximamente.`);
            } else {
                alert('¡No hay tarjetas para repasar!');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Atajo de teclado: espacio para voltear
    $(document).keydown(function(e) {
        if (e.key === ' ' && $('#sessionSection').is(':visible')) {
            e.preventDefault();
            FlashcardUI.flipCard();
        }
    });
});
