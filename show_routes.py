from app import create_app  
app = create_app()  

with app.app_context():
    for r in sorted(app.url_map.iter_rules(), key=lambda x: str(x)):
        print(r)
