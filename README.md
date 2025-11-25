# TP 2 – IA et Tests Logiciels Automatisés

## 🎯 Objectifs pédagogiques

À l'issue de ce TP, vous serez capable de :

1. **Comprendre** les bénéfices et limites de l'IA dans l'automatisation des tests
2. **Générer automatiquement** des tests unitaires et fonctionnels à partir de spécifications textuelles
3. **Mettre en œuvre** des tests visuels avec comparaison d'images
4. **Utiliser Allure Report** pour générer automatiquement des rapports de tests riches, analyser les tendances, et visualiser les résultats de manière intelligente.
5. **Intégrer** l'ensemble dans un pipeline CI/CD avec GitHub Actions

## 🔧 Pré-requis logiciels

### Logiciels requis
- **Python 3.11+** ([python.org](https://python.org))
- **Git** ([git-scm.com](https://git-scm.com))
- **VS Code** ou **IntelliJ IDEA** avec plugin Python
- **Google Chrome** ou **Firefox** (pour Selenium)

## Étape 1 – Configuration du projet et introduction à l'IA dans les tests

### 🎯 Objectif
Initialiser l'environnement de travail et comprendre les cas d'usage de l'IA dans les tests logiciels.

"Ce que vous allez faire":
- poser la structure du projet (src/, tests/, specs/, ai_tools/, reports/, screenshots/),
- créer un environnement virtuel et installer les dépendances,
- configurer pytest (découverte des tests, rapports HTML/Allure),
- ajouter `conftest.py` à la racine pour que le module `src` soit importable.

"Pourquoi": garantir un environnement reproductible et une base de tests standardisée dès le départ.

### 🧩 Instructions

#### 1.1 Configuration de votre branche GitHub
- Créez une nouvelle branche ('git checkout -b <votre_nom>')

#### 1.2 Structure des dossiers
Créez l'arborescence suivante :

```
tp1-ia-tests/
├── src/
│   └── calculator.py          # Application à tester
├── tests/
│   ├── __init__.py
│   ├── generated/             # Tests générés par IA
│   │   └── __init__.py
│   └── visual/                # Tests visuels
│       └── __init__.py
├── specs/
│   └── calculator_spec.txt    # Spécifications textuelles
├── ai_tools/
│   ├── __init__.py
│   ├── test_generator.py      # Générateur de tests IA
│   └── visual_comparator.py     # Comparator Visuel
├── screenshots/
│   ├── baseline/              # Images de référence
│   └── current/               # Images courantes
├── reports/
├── requirements.txt
└── pytest.ini
```

#### 1.3 Installation des dépendances

Créez le fichier `requirements.txt` :

```txt
pytest==7.4.3
pytest-html==4.1.1
selenium==4.15.2
pillow==10.1.0
pandas==2.1.3
scikit-learn==1.3.2
matplotlib==3.8.2
allure-pytest==2.13.2
webdriver-manager==4.0.1
```

Installez les dépendances :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 1.4 Configuration pytest

Créez le fichier `pytest.ini` :

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --html=reports/report.html
    --self-contained-html
    --alluredir=reports/allure-results
```

#### 1.5 Configuration PYTHONPATH

Créez le fichier `conftest.py` à la racine du projet :

```python
"""Configuration pytest globale"""
import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
```

Ce fichier permet à pytest de trouver le module `src` lors de l'exécution des tests.

### 🧪 Résultat attendu

✅ Structure de projet créée  
✅ Environnement virtuel activé  
✅ Toutes les dépendances installées sans erreur  
✅ Commande `pytest --version` retourne la version 7.4.3+

---

## Étape 2 – Application cible et spécifications textuelles

### 🎯 Objectif
Créer une application simple à tester et rédiger des spécifications en langage naturel qui serviront de base à la génération automatique de tests.

"Ce que vous allez faire":
- implémenter une petite calculatrice (`Calculator`, `AdvancedCalculator`) avec des règles claires (ex. division par zéro),
- écrire des spécifications Given‑When‑Then dans `specs/calculator_spec.txt`.

"Pourquoi": ces specs seront la source d’entrée pour le générateur automatique de tests de l’Étape 3.

### 🧩 Instructions

#### 2.1 Création de l'application Calculator

Créez le fichier `src/calculator.py` :

```python
"""
Module Calculator - Application simple pour démonstration des tests IA
"""

class Calculator:
    """Calculatrice avec opérations de base"""
    
    def add(self, a: float, b: float) -> float:
        """Additionne deux nombres"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Soustrait b de a"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplie deux nombres"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divise a par b
        
        Raises:
            ValueError: Si b est égal à 0
        """
        if b == 0:
            raise ValueError("Division par zéro impossible")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Calcule base^exponent"""
        return base ** exponent
    
    def modulo(self, a: float, b: float) -> float:
        """Retourne le reste de a divisé par b"""
        if b == 0:
            raise ValueError("Modulo par zéro impossible")
        return a % b


class AdvancedCalculator(Calculator):
    """Calculatrice avancée avec fonctions mathématiques"""
    
    def factorial(self, n: int) -> int:
        """Calcule la factorielle de n
        
        Args:
            n: Entier positif
            
        Returns:
            Factorielle de n
            
        Raises:
            ValueError: Si n est négatif
        """
        if n < 0:
            raise ValueError("Factorielle définie uniquement pour les entiers positifs")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def is_prime(self, n: int) -> bool:
        """Vérifie si n est un nombre premier"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
```

#### 2.2 Rédaction des spécifications

Créez le fichier `specs/calculator_spec.txt` :

```text
# Spécifications de la Calculatrice

## Fonctionnalités de base

### Addition
- GIVEN deux nombres positifs WHEN j'additionne THEN le résultat est la somme
- GIVEN un nombre positif et un nombre négatif WHEN j'additionne THEN le résultat est correct
- GIVEN deux nombres décimaux WHEN j'additionne THEN le résultat est précis

### Soustraction
- GIVEN deux nombres positifs WHEN je soustrais THEN le résultat est correct
- GIVEN le résultat est négatif WHEN je soustrais THEN le signe est correct

### Multiplication
- GIVEN deux nombres positifs WHEN je multiplie THEN le résultat est le produit
- GIVEN un nombre par zéro WHEN je multiplie THEN le résultat est zéro
- GIVEN deux nombres négatifs WHEN je multiplie THEN le résultat est positif

### Division
- GIVEN deux nombres où le diviseur n'est pas zéro WHEN je divise THEN le résultat est correct
- GIVEN le diviseur est zéro WHEN je divise THEN une exception ValueError est levée
- GIVEN une division décimale WHEN je divise THEN le résultat est précis

### Puissance
- GIVEN une base et un exposant positif WHEN je calcule la puissance THEN le résultat est correct
- GIVEN un exposant négatif WHEN je calcule la puissance THEN le résultat est un décimal
- GIVEN un exposant de zéro WHEN je calcule la puissance THEN le résultat est 1

### Modulo
- GIVEN deux nombres positifs WHEN je calcule le modulo THEN le reste est correct
- GIVEN le diviseur est zéro WHEN je calcule le modulo THEN une exception est levée

## Fonctionnalités avancées

### Factorielle
- GIVEN un entier positif WHEN je calcule la factorielle THEN le résultat est correct
- GIVEN zéro WHEN je calcule la factorielle THEN le résultat est 1
- GIVEN un nombre négatif WHEN je calcule la factorielle THEN une exception est levée

### Nombre premier
- GIVEN un nombre premier WHEN je vérifie THEN retourne True
- GIVEN un nombre non premier WHEN je vérifie THEN retourne False
- GIVEN un nombre inférieur à 2 WHEN je vérifie THEN retourne False
```

Vérifier que le module fonctionne :

```bash
# Vérifier que le module fonctionne
python -c "from src.calculator import Calculator; c = Calculator(); print(c.add(5, 3))"
```

### 🧪 Résultat attendu

✅ Fichier `calculator.py` créé avec toutes les méthodes  
✅ Spécifications rédigées en format Given-When-Then  
✅ Test manuel de l'application réussit (affiche 8)

---

## Étape 3 – Générateur automatique de tests avec IA (simulé)

### 🎯 Objectif
Créer un outil qui parse les spécifications textuelles et génère automatiquement des tests pytest correspondants.

"Ce que vous allez faire":
- parser le fichier de specs, identifier les sections/scénarios,
- transformer chaque scénario en test pytest (nommage, corps du test),
- écrire le fichier `tests/generated/test_calculator_generated.py` puis l’exécuter.

"Ce que fait la commande":
- `python ai_tools/test_generator.py` génère le fichier de tests,
- `pytest tests/generated/ -v` exécute uniquement ces tests générés.

### 🧩 Instructions

#### 3.1 Créer le générateur de tests

Créez le fichier `ai_tools/test_generator.py` :

```python
"""
Générateur automatique de tests à partir de spécifications textuelles
Simule l'utilisation d'un LLM pour transformer du langage naturel en code de test
"""

import re
from typing import List, Dict
from pathlib import Path


class TestGenerator:
    """Génère des tests pytest à partir de spécifications Given-When-Then"""

    def __init__(self, specs_file: str):
        self.specs_file = Path(specs_file)
        self.specs = self._parse_specifications()

    def _parse_specifications(self) -> Dict[str, List[str]]:
        """Parse le fichier de spécifications et extrait les scénarios"""
        with open(self.specs_file, 'r', encoding='utf-8') as f:
            content = f.read()

        specs = {}
        current_section = None

        # Extraction des sections et scénarios
        for line in content.split('\n'):
            # Détection des sections (### Titre)
            if line.startswith('###'):
                current_section = line.replace('#', '').strip().lower()
                specs[current_section] = []
            # Détection des scénarios (- GIVEN...)
            elif line.startswith('- GIVEN') and current_section:
                specs[current_section].append(line[2:])  # Retire "- "

        return specs

    def _generate_test_name(self, scenario: str) -> str:
        """Génère un nom de test à partir d'un scénario"""
        # Extraire les parties clés du scénario
        match = re.search(r'WHEN (.+?) THEN', scenario)
        if match:
            action = match.group(1).strip()
            # Nettoyer et convertir en snake_case
            test_name = re.sub(r'[^\w\s]', '', action)
            test_name = test_name.lower().replace(' ', '_')
            return f"test_{test_name}"
        return "test_scenario"

    def _generate_test_body(self, section: str, scenario: str) -> str:
        """Génère le corps du test en fonction du scénario"""
        # Parser le scénario
        given_match = re.search(r'GIVEN (.+?) WHEN', scenario)
        when_match = re.search(r'WHEN (.+?) THEN', scenario)
        then_match = re.search(r'THEN (.+?)$', scenario)

        given = given_match.group(1) if given_match else ""
        when = when_match.group(1) if when_match else ""
        then = then_match.group(1) if then_match else ""

        # Génération du code selon la section
        code = self._map_scenario_to_code(section, given, when, then)

        return f'''        """
        GIVEN {given}
        WHEN {when}
        THEN {then}
        """
        calculator = Calculator()
{code}'''

    def _map_scenario_to_code(self, section: str, given: str, when: str, then: str) -> str:
        """Mappe un scénario vers du code Python concret (logique simplifiée)"""

        # Mapping basé sur les mots-clés
        if section == "addition":
            if "positifs" in given:
                return "        result = calculator.add(5, 3)\n        assert result == 8"
            elif "négatif" in given:
                return "        result = calculator.add(5, -3)\n        assert result == 2"
            elif "décimaux" in given:
                return "        result = calculator.add(5.5, 3.2)\n        assert abs(result - 8.7) < 0.01"

        elif section == "soustraction":
            if "positifs" in given:
                return "        result = calculator.subtract(10, 3)\n        assert result == 7"
            elif "négatif" in given:
                return "        result = calculator.subtract(3, 10)\n        assert result == -7"

        elif section == "multiplication":
            if "positifs" in given:
                return "        result = calculator.multiply(5, 3)\n        assert result == 15"
            elif "zéro" in given:
                return "        result = calculator.multiply(5, 0)\n        assert result == 0"
            elif "négatifs" in given:
                return "        result = calculator.multiply(-5, -3)\n        assert result == 15"

        elif section == "division":
            if "n'est pas zéro" in given:
                return "        result = calculator.divide(10, 2)\n        assert result == 5.0"
            elif "zéro" in given:
                return "        with pytest.raises(ValueError, match=\"Division par zéro\"):\n            calculator.divide(10, 0)"
            elif "décimale" in given:
                return "        result = calculator.divide(7, 3)\n        assert abs(result - 2.333) < 0.01"

        elif section == "puissance":
            if "positif" in given:
                return "        result = calculator.power(2, 3)\n        assert result == 8"
            elif "négatif" in given:
                return "        result = calculator.power(2, -2)\n        assert result == 0.25"
            elif "zéro" in given:
                return "        result = calculator.power(5, 0)\n        assert result == 1"

        elif section == "modulo":
            if "positifs" in given:
                return "        result = calculator.modulo(10, 3)\n        assert result == 1"
            elif "zéro" in given:
                return "        with pytest.raises(ValueError):\n            calculator.modulo(10, 0)"

        elif section == "factorielle":
            if "positif" in given and "zéro" not in given:
                return "        from src.calculator import AdvancedCalculator\n        calculator = AdvancedCalculator()\n        result = calculator.factorial(5)\n        assert result == 120"
            elif "zéro" in given:
                return "        from src.calculator import AdvancedCalculator\n        calculator = AdvancedCalculator()\n        result = calculator.factorial(0)\n        assert result == 1"
            elif "négatif" in given:
                return "        from src.calculator import AdvancedCalculator\n        calculator = AdvancedCalculator()\n        with pytest.raises(ValueError):\n            calculator.factorial(-5)"

        elif section == "nombre premier":
            if "premier" in given and "non" not in given:
                return "        from src.calculator import AdvancedCalculator\n        calculator = AdvancedCalculator()\n        assert calculator.is_prime(7) == True"
            elif "non premier" in given:
                return "        from src.calculator import AdvancedCalculator\n        calculator = AdvancedCalculator()\n        assert calculator.is_prime(8) == False"
            elif "inférieur" in given:
                return "        from src.calculator import AdvancedCalculator\n        calculator = AdvancedCalculator()\n        assert calculator.is_prime(1) == False"

        # Par défaut
        return "        # TODO: Implémenter ce test\n        pass"

    def generate_tests(self, output_file: str):
        """Génère le fichier de tests complet"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # En-tête du fichier
        content = '''"""
Tests générés automatiquement par IA à partir des spécifications
Fichier source: {}
"""

import pytest
from src.calculator import Calculator


class TestCalculatorGenerated:
    """Tests générés automatiquement"""
    
'''.format(self.specs_file.name)

        # Génération des tests
        for section, scenarios in self.specs.items():
            content += f"    # Tests pour: {section}\n"
            for scenario in scenarios:
                test_name = self._generate_test_name(scenario)
                test_body = self._generate_test_body(section, scenario)
                content += f"\n    def {test_name}(self):\n{test_body}\n\n"

        # Écriture du fichier
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Tests générés avec succès: {output_path}")
        print(f"📊 Nombre de sections: {len(self.specs)}")
        print(f"📊 Nombre total de tests: {sum(len(scenarios) for scenarios in self.specs.values())}")


def main():
    """Point d'entrée principal"""
    generator = TestGenerator('specs/calculator_spec.adoc')
    generator.generate_tests('tests/generated/test_calculator_generated.py')


if __name__ == '__main__':
    main()
```

#### 3.2 Exécuter le générateur

```bash
python ai_tools/test_generator.py
```

#### 3.3 Analyser les tests générés

Ouvrez le fichier `tests/generated/test_calculator_generated.py` généré et observez comment les spécifications ont été transformées en code de test.

Exécuter les tests générés :

```bash
# Exécuter les tests générés
pytest tests/generated/test_calculator_generated.py -v
```

### 🧪 Résultat attendu

✅ Fichier `test_calculator_generated.py` créé automatiquement  
✅ Tous les scénarios des specs transformés en tests  
✅ Tests exécutés avec succès (tous PASSED)  
✅ Message: "X tests passed in Y seconds"

**Exemple de sortie:**
```
✅ Tests générés avec succès: tests/generated/test_calculator_generated.py
📊 Nombre de sections: 8
📊 Nombre total de tests: 17
```

---

## Étape 4 – Tests visuels automatisés avec comparaison d'images

### 🎯 Objectif
Implémenter des tests visuels qui capturent des screenshots d'interface et les comparent automatiquement avec des images de référence.

"Ce que vous allez faire":
- créer une page HTML contrôlable et déterministe (`calculator_ui.html`),
- capturer des screenshots avec Selenium (Chrome headless, taille fixe),
- comparer chaque screenshot à une baseline via `VisualComparator` (tolérance configurable),
- produire un diff visuel pour diagnostiquer les écarts.

"Résultat attendu":
- premier run: création des baselines et `pytest.skip`,
- runs suivants: comparaison baseline vs current, tests `PASSED` si l’écart ≤ tolérance.

### 🧩 Instructions

#### 4.1 Créer une page HTML simple à tester

Créez le fichier `src/calculator_ui.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculatrice</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .calculator {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 320px;
        }
        h1 {
            text-align: center;
            color: #667eea;
            margin-top: 0;
        }
        .display {
            background: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            text-align: right;
            font-size: 28px;
            margin-bottom: 20px;
            min-height: 40px;
            word-wrap: break-word;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        button {
            padding: 20px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        button:hover {
            transform: scale(1.05);
        }
        .number {
            background: #e0e0e0;
            color: #333;
        }
        .operator {
            background: #667eea;
            color: white;
        }
        .equals {
            background: #48bb78;
            color: white;
            grid-column: span 2;
        }
        .clear {
            background: #f56565;
            color: white;
            grid-column: span 2;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>🧮 Calculatrice</h1>
        <div id="display" class="display">0</div>
        <div class="buttons">
            <button class="number" onclick="appendNumber('7')">7</button>
            <button class="number" onclick="appendNumber('8')">8</button>
            <button class="number" onclick="appendNumber('9')">9</button>
            <button class="operator" onclick="setOperator('/')">/</button>
            
            <button class="number" onclick="appendNumber('4')">4</button>
            <button class="number" onclick="appendNumber('5')">5</button>
            <button class="number" onclick="appendNumber('6')">6</button>
            <button class="operator" onclick="setOperator('*')">×</button>
            
            <button class="number" onclick="appendNumber('1')">1</button>
            <button class="number" onclick="appendNumber('2')">2</button>
            <button class="number" onclick="appendNumber('3')">3</button>
            <button class="operator" onclick="setOperator('-')">-</button>
            
            <button class="number" onclick="appendNumber('0')">0</button>
            <button class="number" onclick="appendNumber('.')">.</button>
            <button class="equals" onclick="calculate()">=</button>
            <button class="operator" onclick="setOperator('+')">+</button>
            
            <button class="clear" onclick="clearDisplay()">Clear</button>
        </div>
    </div>

    <script>
        let currentValue = '0';
        let previousValue = null;
        let operator = null;

        function updateDisplay() {
            document.getElementById('display').textContent = currentValue;
        }

        function appendNumber(num) {
            if (currentValue === '0') {
                currentValue = num;
            } else {
                currentValue += num;
            }
            updateDisplay();
        }

        function setOperator(op) {
            if (previousValue === null) {
                previousValue = parseFloat(currentValue);
                currentValue = '0';
            }
            operator = op;
        }

        function calculate() {
            if (previousValue !== null && operator !== null) {
                const current = parseFloat(currentValue);
                let result;
                switch(operator) {
                    case '+': result = previousValue + current; break;
                    case '-': result = previousValue - current; break;
                    case '*': result = previousValue * current; break;
                    case '/': result = previousValue / current; break;
                }
                currentValue = result.toString();
                previousValue = null;
                operator = null;
                updateDisplay();
            }
        }

        function clearDisplay() {
            currentValue = '0';
            previousValue = null;
            operator = null;
            updateDisplay();
        }
    </script>
</body>
</html>
```

#### 4.2 Créer l'outil de comparaison visuelle

Créez le fichier `ai_tools/visual_comparator.py` :

```python
"""
Comparateur visuel d'images pour les tests
Utilise Pillow pour la comparaison pixel par pixel et génère un diff visuel
"""

from PIL import Image, ImageDraw, ImageChops
from pathlib import Path
import numpy as np
from typing import Tuple, Optional


class VisualComparator:
    """Compare deux images et génère un rapport de différences"""
    
    def __init__(self, tolerance: float = 0.1):
        """
        Args:
            tolerance: Pourcentage de différence acceptable (0.0 à 1.0)
        """
        self.tolerance = tolerance
    
    def compare_images(
        self, 
        baseline_path: str, 
        current_path: str,
        diff_output: Optional[str] = None
    ) -> Tuple[bool, float, str]:
        """
        Compare deux images
        
        Args:
            baseline_path: Chemin de l'image de référence
            current_path: Chemin de l'image courante
            diff_output: Chemin pour sauvegarder l'image de différence
            
        Returns:
            Tuple (is_match, difference_percentage, message)
        """
        baseline = Image.open(baseline_path)
        current = Image.open(current_path)
        
        # Vérifier que les images ont la même taille
        if baseline.size != current.size:
            return False, 100.0, f"Tailles différentes: {baseline.size} vs {current.size}"
        
        # Calculer la différence
        diff = ImageChops.difference(baseline, current)
        
        # Convertir en array numpy pour calcul
        diff_array = np.array(diff)
        
        # Calculer le pourcentage de différence
        if diff_array.size == 0:
            return True, 0.0, "Images identiques"
        
        # Moyenne des différences (0-255 par canal)
        mean_diff = np.mean(diff_array) / 255.0
        max_diff = np.max(diff_array) / 255.0
        
        # Pourcentage de pixels différents
        threshold = 10  # Seuil de différence par pixel
        diff_mask = np.any(diff_array > threshold, axis=-1) if len(diff_array.shape) == 3 else diff_array > threshold
        pixels_diff = np.sum(diff_mask)
        total_pixels = diff_mask.size
        percentage_diff = (pixels_diff / total_pixels) * 100
        
        # Générer l'image de différence si demandé
        if diff_output:
            self._generate_diff_image(baseline, current, diff, diff_output)
        
        # Déterminer si c'est un match
        is_match = percentage_diff <= (self.tolerance * 100)
        
        message = f"Différence: {percentage_diff:.2f}% des pixels (moyenne: {mean_diff*100:.2f}%, max: {max_diff*100:.2f}%)"
        
        return is_match, percentage_diff, message
    
    def _generate_diff_image(self, baseline: Image, current: Image, diff: Image, output_path: str):
        """Génère une image composite montrant baseline, current et diff"""
        width, height = baseline.size
        
        # Créer une image 3x plus large
        composite = Image.new('RGB', (width * 3, height), color='white')
        
        # Coller les images
        composite.paste(baseline.convert('RGB'), (0, 0))
        composite.paste(current.convert('RGB'), (width, 0))
        
        # Amplifier la différence pour la rendre visible
        diff_enhanced = diff.point(lambda x: x * 10)
        composite.paste(diff_enhanced.convert('RGB'), (width * 2, 0))
        
        # Ajouter des labels
        draw = ImageDraw.Draw(composite)
        
        # Sauvegarder
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        composite.save(output_path)
    
    def create_baseline(self, screenshot_path: str, baseline_path: str):
        """Copie un screenshot comme nouvelle baseline"""
        img = Image.open(screenshot_path)
        Path(baseline_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(baseline_path)
        print(f"✅ Baseline créée: {baseline_path}")


def main():
    """Démonstration"""
    comparator = VisualComparator(tolerance=0.05)
    
    # Exemple d'utilisation
    print("Comparateur visuel initialisé avec tolérance de 5%")


if __name__ == '__main__':
    main()
```

#### 4.3 Créer les tests visuels Selenium

Créez le fichier `tests/visual/test_calculator_ui.py` :

```python
"""
Tests visuels de l'interface calculatrice avec Selenium
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from ai_tools.visual_comparator import VisualComparator


@pytest.fixture
def driver():
    """Fixture pour le driver Selenium"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def comparator():
    """Fixture pour le comparateur visuel"""
    return VisualComparator(tolerance=0.02)  # 2% de tolérance


class TestCalculatorVisual:
    """Tests visuels de la calculatrice"""
    
    def test_initial_state(self, driver, comparator):
        """Test de l'état initial de la calculatrice"""
        # Charger la page
        html_path = Path(__file__).parent.parent.parent / 'src' / 'calculator_ui.html'
        driver.get(f'file://{html_path.absolute()}')
        
        # Attendre que la page soit chargée
        time.sleep(1)
        
        # Prendre un screenshot
        screenshots_dir = Path(__file__).parent.parent.parent / 'screenshots'
        current_path = screenshots_dir / 'current' / 'initial_state.png'
        baseline_path = screenshots_dir / 'baseline' / 'initial_state.png'
        diff_path = screenshots_dir / 'diff' / 'initial_state_diff.png'
        
        current_path.parent.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(current_path))
        
        # Si baseline n'existe pas, la créer
        if not baseline_path.exists():
            comparator.create_baseline(str(current_path), str(baseline_path))
            pytest.skip("Baseline créée, relancer les tests")
        
        # Comparer avec la baseline
        is_match, diff_percentage, message = comparator.compare_images(
            str(baseline_path),
            str(current_path),
            str(diff_path)
        )
        
        assert is_match, f"Différence visuelle détectée: {message}"
    
    def test_after_calculation(self, driver, comparator):
        """Test après une opération de calcul"""
        html_path = Path(__file__).parent.parent.parent / 'src' / 'calculator_ui.html'
        driver.get(f'file://{html_path.absolute()}')
        time.sleep(1)
        
        # Effectuer un calcul: 5 + 3 =
        driver.find_element(By.XPATH, "//button[text()='5']").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[text()='+']").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[text()='3']").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[text()='=']").click()
        time.sleep(0.5)
        
        # Screenshot
        screenshots_dir = Path(__file__).parent.parent.parent / 'screenshots'
        current_path = screenshots_dir / 'current' / 'after_calculation.png'
        baseline_path = screenshots_dir / 'baseline' / 'after_calculation.png'
        diff_path = screenshots_dir / 'diff' / 'after_calculation_diff.png'
        
        driver.save_screenshot(str(current_path))
        
        if not baseline_path.exists():
            comparator.create_baseline(str(current_path), str(baseline_path))
            pytest.skip("Baseline créée, relancer les tests")
        
        is_match, diff_percentage, message = comparator.compare_images(
            str(baseline_path),
            str(current_path),
            str(diff_path)
        )
        
        assert is_match, f"Différence visuelle après calcul: {message}"
    
    def test_display_content(self, driver):
        """Test du contenu affiché (test fonctionnel en bonus)"""
        html_path = Path(__file__).parent.parent.parent / 'src' / 'calculator_ui.html'
        driver.get(f'file://{html_path.absolute()}')
        time.sleep(1)
        
        # Vérifier l'affichage initial
        display = driver.find_element(By.ID, 'display')
        assert display.text == '0', "Affichage initial incorrect"
        
        # Test de calcul
        driver.find_element(By.XPATH, "//button[text()='7']").click()
        time.sleep(0.2)
        assert display.text == '7'
        
        driver.find_element(By.XPATH, "//button[text()='8']").click()
        time.sleep(0.2)
        assert display.text == '78'
```


### 💻 Commandes

```bash
# Installer ChromeDriver
pip install webdriver-manager
```
Créer dossier screenshots/diff:

```bash
# Créer dossier diff
mkdir -p screenshots/diff
```

Exécuter les tests visuels (première fois = création baseline) :

```bash
# Exécuter les tests visuels (première fois = création baseline)
pytest tests/visual/ -v
```

Relancer pour une vraie comparaison :

```bash
# Relancer pour vraie comparaison
pytest tests/visual/ -v
```

### 🧪 Résultat attendu

✅ Interface HTML créée et fonctionnelle  
✅ Comparateur visuel opérationnel  
✅ Baselines créées lors du premier run  
✅ Tests visuels passent au second run  
✅ Images de diff générées dans `screenshots/diff/`

**Note:** Au premier run, vous verrez "Baseline créée". Au second run, les tests doivent PASSER.

---

## Étape 5 – Analyse intelligente des résultats avec Allure Report

### 🎯 Objectif
Utiliser **Allure Report** (outil open-source professionnel) pour générer automatiquement des rapports de tests riches, analyser les tendances, et visualiser les résultats de manière intelligente.

"Ce que vous allez faire" : configurer et utiliser Allure Report pour :
- générer des rapports HTML interactifs automatiquement,
- visualiser les statistiques de tests (succès, échecs, durée),
- identifier les tests qui échouent le plus souvent,
- analyser les tendances et l'évolution dans le temps,
- exporter et partager les rapports facilement.

### 🧩 Instructions

#### 5.1 Installation d'Allure Commandline

"Ce que vous allez faire" : installer le CLI Allure qui permet de générer les rapports HTML à partir des données collectées par pytest.


**Sur macOS/Linux :**
```bash
# Installer via npm (nécessite Node.js)
npm install -g allure-commandline

# Vérifier l'installation
allure --version
```

**Sur Windows (PowerShell) :**
```powershell
# Via Scoop (si installé)
scoop install allure

# Ou via Chocolatey
choco install allure-commandline

# Ou télécharger manuellement depuis:
# https://github.com/allure-framework/allure2/releases
```

**Alternative : utiliser Docker (si npm n'est pas disponible) :**
```bash
# Pas besoin d'installer, on utilise l'image Docker
docker run -it --rm -v "$PWD:/app" -w /app frankescobar/allure-docker-service allure --version
```


#### 5.2 Configuration d'Allure dans pytest

"Ce que vous allez faire" : le fichier `conftest.py` existe déjà (créé à l'Étape 1). Il n'y a rien de spécial à faire, 
pytest collecte automatiquement les données Allure quand on utilise `--alluredir`.

#### 5.3 Exécuter les tests et générer le rapport Allure

"Ce que vous allez faire" : exécuter pytest avec Allure, puis générer le rapport HTML interactif.

**Étape 1 : Exécuter les tests avec collecte Allure**

```bash
# Exécuter tous les tests - les données Allure sont collectées automatiquement
pytest tests/ -v --alluredir=reports/allure-results
```

**Étape 2 : Générer le rapport HTML**

```bash
# Générer le rapport HTML
allure generate reports/allure-results --clean -o reports/allure-report

# Ouvrir le rapport dans le navigateur (macOS)
allure open reports/allure-report

# 4bis. Ou ouvrir manuellement (tous OS)
# Ouvrez reports/allure-report/index.html dans votre navigateur
```

**Étape 3 : Visualiser les résultats**

Le rapport Allure s'ouvre dans votre navigateur et affiche :
- 📊 **Overview** : Statistiques globales (total, passés, échoués, durée)
- 📈 **Graphs** : Graphiques de tendances, durée des tests
- 📋 **Suites** : Liste des suites de tests par catégorie
- ⏱️ **Timeline** : Timeline d'exécution des tests
- 📸 **Packages** : Groupement par packages/modules


### 🧪 Résultat attendu

✅ Allure CLI installé et fonctionnel  
✅ Données Allure collectées dans `reports/allure-results/`  
✅ Rapport HTML généré dans `reports/allure-report/`  
✅ Rapport affiché dans le navigateur avec :
- Graphiques de statistiques
- Liste des tests passés/échoués
- Durées d'exécution
- Détails des erreurs pour les tests échoués

**Capture d'écran attendue du rapport Allure :**
- Page d'accueil avec graphiques (pie chart des résultats, timeline)
- Vue détaillée de chaque test avec statut, durée, logs

### 🎓 Ce que vous avez appris

1. **Allure Report** est un outil standard pour l'analyse de tests
2. La **collecte automatique** via `--alluredir` capture toutes les informations
3. Le **rapport HTML interactif** permet une analyse visuelle efficace


---

## Étape 6 – Intégration CI/CD complète avec GitHub Actions

### 🎯 Objectif
Créer un pipeline CI/CD complet qui exécute automatiquement tous les tests, génère les analyses IA, et publie les rapports.

### 🧩 Instructions

"Ce que vous allez faire" : vous allez construire un pipeline CI/CD complet étape par étape. Créez le fichier `.github/workflows/ci-tests-ia.yml` en suivant les instructions ci-dessous.

#### 6.1 Structure de base du workflow

Créez le dossier et le fichier :
```bash
mkdir -p .github/workflows
touch .github/workflows/ci-tests-ia.yml
```

**Étape 1 : Définir le nom et les déclencheurs**

Ajoutez l'en-tête du workflow. Un workflow GitHub Actions doit commencer par :
- `name:` : le nom du workflow (ex: "CI - Tests Automatisés avec IA")
- `on:` : quand le workflow doit s'exécuter (push, pull_request, schedule)

**Indices :**
- Le workflow doit s'exécuter sur votre branches `nom_votre_branche` lors d'un `push`

**Vérification** : Votre structure doit ressembler à :
```yaml
name: CI - Tests Automatisés avec IA

on:
  push:
    branches: [ ??? ]  # Quelles branches ?
```

---

#### 6.2 Définir le job et l'environnement

**Étape 2 : Créer le job principal**

Ajoutez la section `jobs:` avec un job nommé `test-and-analyze`.

**Indices :**
- `runs-on: ubuntu-latest` : exécution sur Ubuntu
- `strategy.matrix` : permet de tester plusieurs versions de Python (utilisez `python-version: ['3.11']`)

**Vérification** : Vous devez avoir quelque chose comme :
```yaml
jobs:
  test-and-analyze:
    name: Tests + Analyse IA
    runs-on: ???  # Quel OS ?
    
    strategy:
      matrix:
        python-version: [???]  # Quelle version ?
    
    steps:
      # Les étapes suivent ici...
```

---

#### 6.3 Étapes de configuration de base

**Étape 3 : Checkout et configuration Python**

Ajoutez les premières étapes du workflow :

1. **Checkout du code** : utilisez `actions/checkout@v4` pour récupérer le code du dépôt
2. **Setup Python** : utilisez `actions/setup-python@v4` avec :
    - `python-version: ${{ matrix.python-version }}`
    - `cache: 'pip'` (pour accélérer les builds)
3. **Installation des dépendances** :
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

**Ressources** : Consultez la [documentation GitHub Actions](https://docs.github.com/en/actions) si besoin.

---

#### 6.4 Setup des outils de test

**Étape 4 : Configuration Chrome pour Selenium**

Ajoutez une étape pour installer Chrome (nécessaire pour Selenium).

**Indice :** Utilisez l'action `browser-actions/setup-chrome@latest`

---

#### 6.5 Exécution des tests

**Étape 5 : Tests générés et tests visuels**

Créez deux étapes séparées pour exécuter :
1. **Tests générés** :
    - D'abord générer les tests : `python ai_tools/test_generator.py`
    - Puis les exécuter : `pytest tests/generated/ -v --html=reports/generated-report.html --self-contained-html`
    - Ajoutez `continue-on-error: true` pour que le pipeline continue même si ces tests échouent

2. **Tests visuels** :
    - Exécuter : `pytest tests/visual/ -v --html=reports/visual-report.html --self-contained-html`
    - Même `continue-on-error: true`

**Astuce** : Utilisez `echo` pour afficher des messages informatifs dans les logs.

---

#### 6.6 Génération des rapports Allure

**Étape 6 : Collecte et génération Allure**

Créez deux étapes avec `if: always()` (s'exécutent même en cas d'échec) :

1. **Exécution complète avec Allure** :
    - Exécuter tous les tests avec collecte Allure : `pytest tests/ -v --html=reports/full-report.html --self-contained-html --alluredir=reports/allure-results`
    - `continue-on-error: true`

2. **Génération du rapport HTML Allure** :
    - Installer Allure CLI : `npm install -g allure-commandline`
    - Générer le rapport : `allure generate reports/allure-results --clean -o reports/allure-report`

**Question à réfléchir** : Pourquoi utilise-t-on `if: always()` ici ?

---

#### 6.7 Upload des artifacts

**Étape 7 : Sauvegarder les rapports et screenshots**

Créez deux étapes pour uploader les artifacts (avec `if: always()`) :

1. **Upload des rapports** :
    - Action : `actions/upload-artifact@v3`
    - `name: test-reports`
    - `path: reports/`
    - `retention-days: 30`

2. **Upload des screenshots** :
    - Même action
    - `name: screenshots`
    - `path: screenshots/`
    - `retention-days: 30`

**Indice** : Consultez la [documentation upload-artifact](https://github.com/actions/upload-artifact) pour la syntaxe exacte.


---

### 💻 Commandes de validation

Après avoir créé votre workflow :

```bash
# Pousser sur GitHub pour tester
git add .github/workflows/ci-tests-ia.yml
git commit -m "feat: add CI/CD pipeline"
git push
```

**Vérification sur GitHub :**
1. Allez dans l'onglet "Actions" de votre dépôt
2. Vous devriez voir votre workflow s'exécuter
3. Consultez les logs pour détecter d'éventuelles erreurs

### 🧪 Résultat attendu

✅ Workflow créé avec succès  
✅ Syntaxe YAML valide  
✅ Pipeline s'exécute sur push/PR  
✅ Tests exécutés automatiquement  
✅ Rapports uploadés comme artifacts  
✅ Commentaire automatique sur les PRs

### 🆘 En cas d'erreur

**Erreur de syntaxe YAML** :
- Vérifiez l'indentation (espaces, pas de tabs)
- Vérifiez que chaque clé est correctement fermée

**Action non trouvée** :
- Vérifiez les versions des actions (v4, v3, etc.)
- Consultez la documentation officielle de chaque action

**Tests qui échouent** :
- C'est normal au début ! Consultez les logs pour identifier le problème

---

**🎉 Félicitations! Vous avez complété le TP2!**

Vous maîtrisez maintenant:

✅ La génération automatique de tests avec IA  
✅ Les tests visuels et comparaison d'images  
✅ L'analyse des résultats avec Allure Report  
✅ L'intégration CI/CD complète

---

## 📚 Ressources complémentaires

### Documentation
- [Pytest](https://docs.pytest.org/)
- [Selenium Python](https://selenium-python.readthedocs.io/)
- [Pillow](https://pillow.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)

### Articles
- "AI in Software Testing: Hype or Reality?"
- "Visual Regression Testing Best Practices"
- "Test Prioritization Techniques"

### Outils alternatifs
- [Percy](https://percy.io/) - Tests visuels (freemium)
- [Playwright](https://playwright.dev/) - Alternative à Selenium
- [Allure](https://docs.qameta.io/allure/) - Reporting avancé



