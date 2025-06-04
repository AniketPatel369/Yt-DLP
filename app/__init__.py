"""
Flask Application Factory
Creates and configures the Flask application instance
"""
from flask import Flask, render_template
from flask_cors import CORS
import logging
import os

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='../static')
    
    # Load configuration
    app.config.from_object('config.settings')
    
    # Enable CORS for API endpoints
    CORS(app, origins=['*'])  # Allow all origins for API
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    
    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='')  # ✅ No prefix for root access
    
    # Web interface route (separate from API)
    @app.route('/web')
    def web_interface():
        """Serve the web interface"""
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app
