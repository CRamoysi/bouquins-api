"""
Tests pour la classe U_String (Unicorn String utilities)
"""
import pytest
from unicorn.u_string import U_String


class TestRemoveDiacritics:
    """Tests pour la méthode remove_diacritics"""
    
    def test_remove_accents_french(self):
        """Teste la suppression des accents français"""
        text = U_String("éàçñ")
        assert text.remove_diacritics() == "eacn"
    
    def test_remove_accents_mixed(self):
        """Teste avec plusieurs types d'accents"""
        text = U_String("Hôtel à São Paulo")
        result = text.remove_diacritics()
        assert result == "Hotel a Sao Paulo"
    
    def test_empty_string(self):
        """Teste avec chaîne vide"""
        text = U_String("")
        assert text.remove_diacritics() == ""
    
    def test_no_diacritics(self):
        """Teste avec une chaîne sans accents"""
        text = U_String("Hello World")
        assert text.remove_diacritics() == "Hello World"
    
    def test_only_diacritics(self):
        """Teste avec uniquement des caractères accentués"""
        text = U_String("éèêëàâäùûüôö")
        result = text.remove_diacritics()
        assert "é" not in result
        assert "è" not in result


class TestLevenshteinDistance:
    """Tests pour la méthode levenshtein_distance"""
    
    def test_identical_strings(self):
        """Teste avec chaînes identiques"""
        text = U_String("hello")
        assert text.levenshtein_distance("hello") == 0
    
    def test_empty_strings(self):
        """Teste avec chaînes vides"""
        text = U_String("")
        assert text.levenshtein_distance("") == 0
        
        text = U_String("hello")
        assert text.levenshtein_distance("") == 5
        
        text = U_String("")
        assert text.levenshtein_distance("world") == 5
    
    def test_one_character_difference(self):
        """Teste avec une différence d'un caractère"""
        text = U_String("chat")
        assert text.levenshtein_distance("chat") == 0
        assert text.levenshtein_distance("char") == 1  # substitution
        assert text.levenshtein_distance("hat") == 1   # suppression
        assert text.levenshtein_distance("chats") == 1 # insertion
    
    def test_multiple_differences(self):
        """Teste avec plusieurs différences"""
        text = U_String("kitten")
        assert text.levenshtein_distance("sitting") == 3
    
    def test_completely_different(self):
        """Teste avec chaînes complètement différentes"""
        text = U_String("abc")
        assert text.levenshtein_distance("xyz") == 3
    
    def test_length_optimization(self):
        """Teste que l'optimisation par longueur fonctionne"""
        # Peu importe l'ordre, le résultat doit être le même
        text1 = U_String("short")
        text2 = U_String("very long string")
        
        dist1 = text1.levenshtein_distance(text2)
        dist2 = U_String(text2).levenshtein_distance(text1)
        
        assert dist1 == dist2


class TestFuzzyMatch:
    """Tests pour la méthode fuzzy_match"""
    
    def test_exact_match(self):
        """Teste la correspondance exacte"""
        text = U_String("Hello World")
        assert text.fuzzy_match("Hello") == True
        assert text.fuzzy_match("World") == True
        assert text.fuzzy_match("Hello World") == True
    
    def test_case_insensitive(self):
        """Teste l'insensibilité à la casse"""
        text = U_String("Hello World")
        assert text.fuzzy_match("hello") == True
        assert text.fuzzy_match("WORLD") == True
        assert text.fuzzy_match("HeLLo") == True
    
    def test_diacritics_tolerance(self):
        """Teste la tolérance aux accents"""
        text = U_String("Café français")
        assert text.fuzzy_match("Cafe") == True
        assert text.fuzzy_match("francais") == True
        assert text.fuzzy_match("café") == True
    
    def test_prefix_match(self):
        """Teste la correspondance par préfixe (60% du mot)"""
        text = U_String("programmation python")
        # "prog" est 60% de "programmation" (10 * 0.6 = 6, donc on prend les 6 premiers)
        assert text.fuzzy_match("program") == True
        assert text.fuzzy_match("pyth") == True
    
    def test_short_words_no_prefix(self):
        """Teste que les mots trop courts (<3 caractères) ne font pas de match par préfixe seul"""
        text = U_String("Hi all")
        # "al" est trouvé comme sous-chaîne de "all" (distance 0)
        assert text.fuzzy_match("al") == True
        # Mais un mot court sans correspondance ne match pas
        assert text.fuzzy_match("xy") == False
        assert text.fuzzy_match("zz") == False
    
    def test_levenshtein_tolerance_short_words(self):
        """Teste la tolérance Levenshtein pour mots courts (≤4 caractères)"""
        text = U_String("chat chien")
        # Distance 1 acceptable pour mots courts
        assert text.fuzzy_match("char") == True  # distance 1 de "chat"
        assert text.fuzzy_match("chit") == True  # distance 1 de "chat"
        assert text.fuzzy_match("xhat") == True  # distance 1 de "chat"
        assert text.fuzzy_match("xxat") == False # distance 2 de "chat", trop loin
    
    def test_levenshtein_tolerance_long_words(self):
        """Teste la tolérance Levenshtein pour mots longs (>4 caractères)"""
        text = U_String("python programming")
        # Distance 2 acceptable pour mots longs
        assert text.fuzzy_match("pithon") == True  # distance 1 de "python"
        assert text.fuzzy_match("pythen") == True  # distance 1 de "python"
        assert text.fuzzy_match("programing") == True  # distance 1 de "programming"
        assert text.fuzzy_match("progaming") == True   # distance 2 de "programming"
    
    def test_substring_match(self):
        """Teste la correspondance par sous-chaîne avec distance 1"""
        text = U_String("anticonstitutionnellement")
        # Recherche "constitu" dans le texte
        assert text.fuzzy_match("constitu") == True
        assert text.fuzzy_match("constitx") == True  # distance 1 acceptable
    
    def test_no_match(self):
        """Teste les cas sans correspondance"""
        text = U_String("Hello World")
        assert text.fuzzy_match("xyz") == False
        assert text.fuzzy_match("bonjour") == False
        assert text.fuzzy_match("test") == False
    
    def test_empty_strings(self):
        """Teste avec chaînes vides"""
        text = U_String("Hello")
        assert text.fuzzy_match("") == True  # chaîne vide trouvée dans toute chaîne
        
        empty_text = U_String("")
        assert empty_text.fuzzy_match("Hello") == False
        assert empty_text.fuzzy_match("") == True
    
    def test_multiple_words_in_text(self):
        """Teste avec plusieurs mots dans le texte"""
        text = U_String("le chat mange du poisson")
        assert text.fuzzy_match("chat") == True
        assert text.fuzzy_match("poisson") == True
        assert text.fuzzy_match("poissan") == True  # distance 1
        assert text.fuzzy_match("chien") == False
    
    def test_word_boundaries(self):
        """Teste que la recherche fonctionne par mot"""
        text = U_String("catastrophe")
        assert text.fuzzy_match("cat") == True  # sous-chaîne
        assert text.fuzzy_match("astrophe") == True  # sous-chaîne
    
    def test_max_substring_checks_limit(self):
        """Teste que la limite de vérifications de sous-chaînes est respectée"""
        # Créer un texte avec un très long mot
        text = U_String("a" * 100)
        # Cela ne devrait pas planter même avec un mot très long
        result = text.fuzzy_match("aa")
        assert isinstance(result, bool)


class TestInheritance:
    """Teste que U_String hérite bien de str"""
    
    def test_is_string(self):
        """Vérifie que U_String est une sous-classe de str"""
        text = U_String("hello")
        assert isinstance(text, str)
        assert isinstance(text, U_String)
    
    def test_string_methods(self):
        """Vérifie que les méthodes de str fonctionnent"""
        text = U_String("Hello World")
        assert text.upper() == "HELLO WORLD"
        assert text.lower() == "hello world"
        assert text.split() == ["Hello", "World"]
        assert len(text) == 11
    
    def test_concatenation(self):
        """Teste la concaténation"""
        text = U_String("Hello")
        result = text + " World"
        assert result == "Hello World"
    
    def test_slicing(self):
        """Teste le slicing"""
        text = U_String("Hello World")
        assert text[0:5] == "Hello"
        assert text[-5:] == "World"


# Tests d'intégration
class TestIntegration:
    """Tests combinant plusieurs méthodes"""
    
    def test_remove_diacritics_then_compare(self):
        """Teste normalisation puis comparaison"""
        text1 = U_String("café")
        text2 = U_String("cafe")
        
        norm1 = text1.remove_diacritics()
        norm2 = text2.remove_diacritics()
        
        assert norm1 == norm2
    
    def test_fuzzy_search(self):
        """Teste une recherche floue simulée"""
        search = U_String("café")
        options = ["cafe", "caffe", "coffee", "tea"]
        
        # Trouve le plus proche
        distances = [(opt, search.levenshtein_distance(opt)) for opt in options]
        closest = min(distances, key=lambda x: x[1])
        
        assert closest[0] == "cafe"  # Distance = 1
        assert closest[1] == 1


# Fixtures pytest (données réutilisables)
@pytest.fixture
def sample_texts():
    """Fixture fournissant des textes de test"""
    return {
        'simple': U_String("hello"),
        'accents': U_String("éèêë"),
        'mixed': U_String("Café français"),
        'empty': U_String(""),
    }


def test_with_fixture(sample_texts):
    """Exemple utilisant une fixture"""
    assert len(sample_texts['simple']) == 5
    assert sample_texts['empty'] == ""
