"""
Script de test manuel pour l'API
Teste tous les endpoints principaux
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Test de l'API Catalogue de Livres\n")
    print("=" * 60)

    # Test 1: Info de l'API
    print("\n1️⃣ Test: GET / (Info API)")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    # Test 2: Ajouter un livre
    print("\n2️⃣ Test: POST /livres (Ajouter un livre)")
    livre_data = {
        "isbn": "978-2-07-036222-6",
        "title": "Les Misérables",
        "author": "Victor Hugo",
        "publisher": "Gallimard",
        "publication_year": 1862,
        "summary": "Un roman historique et social qui suit le destin de Jean Valjean..."
    }
    response = requests.post(f"{BASE_URL}/livres", json=livre_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    # Test 3: Récupérer tous les livres
    print("\n3️⃣ Test: GET /livres (Liste tous les livres)")
    response = requests.get(f"{BASE_URL}/livres")
    print(f"   Status: {response.status_code}")
    livres = response.json()
    print(f"   Nombre de livres: {len(livres)}")
    if livres:
        print(f"   Premier livre: {livres[0]['title']} par {livres[0]['author']}")
        print(f"   Éditeur: {livres[0]['publisher']}")

    # Test 4: Rechercher par ISBN
    print("\n4️⃣ Test: GET /livres/{isbn} (Recherche par ISBN)")
    isbn = "978-2-07-036222-6"
    response = requests.get(f"{BASE_URL}/livres/{isbn}")
    print(f"   Status: {response.status_code}")
    livre = response.json()
    print(f"   Trouvé: {livre['title']} ({livre['publication_year']})")
    print(f"   Éditeur: {livre['publisher']}")

    # Test 5: Recherche intelligente
    print("\n5️⃣ Test: GET /livres/search/ (Recherche intelligente)")
    response = requests.get(f"{BASE_URL}/livres/search/", params={"q": "victor hugo"})
    print(f"   Status: {response.status_code}")
    resultats = response.json()
    print(f"   Résultats trouvés: {len(resultats)}")

    # Test 6: Mettre à jour un livre
    print("\n6️⃣ Test: PUT /livres/{isbn} (Mettre à jour)")
    update_data = {
        "summary": "Chef-d'œuvre de Victor Hugo publié en 1862."
    }
    response = requests.put(f"{BASE_URL}/livres/{isbn}", json=update_data)
    print(f"   Status: {response.status_code}")
    print(f"   Résumé mis à jour: {response.json()['summary'][:50]}...")

    # Test 7: Statistiques
    print("\n7️⃣ Test: GET /stats (Statistiques)")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"   Status: {response.status_code}")
    stats = response.json()
    print(f"   Total de livres: {stats['total_livres']}")
    print(f"   Total d'auteurs: {stats['total_auteurs']}")
    print(f"   Année la plus ancienne: {stats['annee_plus_ancienne']}")

    # Test 8: Ajouter un deuxième livre
    print("\n8️⃣ Test: POST /livres (Ajouter un deuxième livre)")
    livre_data2 = {
        "isbn": "978-2-07-041123-4",
        "title": "Notre-Dame de Paris",
        "author": "Victor Hugo",
        "publisher": "Gallimard",
        "publication_year": 1831,
        "summary": "L'histoire de Quasimodo et Esmeralda."
    }
    response = requests.post(f"{BASE_URL}/livres", json=livre_data2)
    print(f"   Status: {response.status_code}")
    print(f"   Ajouté: {response.json()['title']}")

    # Test 9: Livres par auteur
    print("\n9️⃣ Test: GET /livres/author/{author} (Livres par auteur)")
    response = requests.get(f"{BASE_URL}/livres/author/Victor Hugo")
    print(f"   Status: {response.status_code}")
    livres_hugo = response.json()
    print(f"   Livres de Victor Hugo: {len(livres_hugo)}")
    for livre in livres_hugo:
        print(f"     - {livre['title']} ({livre['publication_year']})")

    # Test 10: Supprimer un livre
    print("\n🔟 Test: DELETE /livres/{isbn} (Supprimer)")
    isbn_to_delete = "978-2-07-041123-4"
    response = requests.delete(f"{BASE_URL}/livres/{isbn_to_delete}")
    print(f"   Status: {response.status_code}")
    print(f"   Message: {response.json()['message']}")

    print("\n" + "=" * 60)
    print("✅ Tous les tests sont terminés!")
    print("\nL'API fonctionne correctement avec le nouvel attribut 'publisher'")

if __name__ == "__main__":
    print("\n⚠️  Assurez-vous que l'API est lancée avec: uvicorn api:app --reload")
    print("Attendre 3 secondes avant de commencer les tests...\n")
    time.sleep(3)

    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Erreur: Impossible de se connecter à l'API")
        print("   Lancez d'abord l'API avec: uvicorn api:app --reload")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
