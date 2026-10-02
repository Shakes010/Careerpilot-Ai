from app.main import app

def test_routes():
    print("Testing FastAPI app router loading...")
    route_paths = []
    for r in app.routes:
        if hasattr(r, "path"):
            route_paths.append(r.path)
    print(f"Loaded {len(route_paths)} routes:")
    for path in sorted(set(route_paths)):
        print(f"  - {path}")
    print("\nAPI Startup Test Completed Successfully!")

if __name__ == "__main__":
    test_routes()
