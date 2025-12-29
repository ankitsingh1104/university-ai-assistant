"""Main application entry point."""
import os
from dotenv import load_dotenv
from backend import create_app

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.run(host=host, port=port, debug=debug)
