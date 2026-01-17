import unicodedata


class U_String(str):
    """Classe personnalisée pour les chaînes de caractères avec des fonctionnalités supplémentaires"""

    # Seuil de correspondance par préfixe (75%)
    _prefixMatchThreshold = 0.75
    # Nombre maximum de sous-chaînes à vérifier pour éviter les problèmes de performance
    _maxSubstringChecks = 10

    def remove_diacritics(self) -> str:
        """Supprime les diacritiques (accents)"""
        # Décompose les caractères accentués (é -> e + ´)
        nfd = unicodedata.normalize('NFD', self)
        # Garde seulement les caractères non-diacritiques
        return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    
    def levenshtein_distance(self, other: str) -> int:
        """Calcule la distance de Levenshtein entre deux chaînes (optimisé)"""
        if self == other:
            return 0
        if not self:
            return len(other)
        if not other:
            return len(self)
        # Assurer que self est la chaîne la plus courte pour minimiser l'usage mémoire
        s1, s2 = (self, other) if len(self) <= len(other) else (other, self)
        len_s1, len_s2 = len(s1), len(s2)

        previous_row = list(range(len_s2 + 1))
        current_row = [0] * (len_s2 + 1)

        for i in range(1, len_s1 + 1):
            current_row[0] = i
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                current_row[j] = min(
                    previous_row[j] + 1,      # suppression
                    current_row[j - 1] + 1,   # insertion
                    previous_row[j - 1] + cost # substitution
                )
            previous_row, current_row = current_row, previous_row
        return previous_row[len_s2]

    def fuzzy_match(self, other: str) -> bool:
        """Vérifie si une chaîne correspond à une autre avec tolérance aux erreurs
        
        Stratégie:
        1. Correspondance exacte (sous-chaîne)
        2. Correspondance par préfixe pour mots >= 3 caractères
        3. Recherche floue avec Levenshtein sur les mots
        """
        # Normalisation une seule fois
        normalized_self = self.remove_diacritics().lower()
        normalized_other = U_String(other).remove_diacritics().lower()

        # 1. Correspondance exacte (sous-chaîne)
        if normalized_other in normalized_self:
            return True

        # 2. Correspondance par préfixe (au moins 60% du mot)
        if len(normalized_other) >= 3:
            prefix_length = int(len(normalized_other) * self._prefixMatchThreshold)
            prefix = normalized_other[:prefix_length]
            if prefix in normalized_self:
                return True

        # 3. Recherche floue par mot avec distance de Levenshtein
        words = normalized_self.split()
        threshold = 1 if len(normalized_other) <= 4 else 2
        
        for word in words:
            if not word:
                continue

            # Correspondance exacte déjà testée ligne 57, skip
            # Vérifier la distance de Levenshtein pour les mots de longueur similaire
            if abs(len(word) - len(normalized_other)) <= 2:
                distance = self.levenshtein_distance(normalized_other) if word == self else U_String(word).levenshtein_distance(normalized_other)
                if distance <= threshold:
                    return True

            # Vérifier si le mot de la requête est une sous-chaîne avec tolérance
            if len(word) >= len(normalized_other):
                substrings_checked = 0
                for i in range(len(word) - len(normalized_other) + 1):
                    if substrings_checked >= self._maxSubstringChecks:
                        break
                    substring = word[i:i + len(normalized_other)]
                    distance = U_String(substring).levenshtein_distance(normalized_other)
                    if distance <= 1:
                        return True
                    substrings_checked += 1

        return False
