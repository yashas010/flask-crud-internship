#!/usr/bin/env python
import os
from app import app, db

# Initialize database tables on startup
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
