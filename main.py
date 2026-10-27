import pandas as pd

# 1. Завантажуємо вихідний файл
df = pd.read_csv('10_27_2026_9_42_31 PM_queryResults.csv')

# Функція для очищення URI (залишає лише корисну назву після '#')
def clean_uri(text):
    if isinstance(text, str) and '#' in text:
        return text.split('#')[-1]
    return str(text)

# Очищаємо всі колонки
df['subject'] = df['subject'].apply(clean_uri)
df['predicate'] = df['predicate'].apply(clean_uri)
df['object'] = df['object'].apply(clean_uri)

# 2. Формуємо вузли (nodes.csv)
# Знаходимо всі триплети, де предикат — це 'type' (встановлює клас)
nodes = df[df['predicate'] == 'type'][['subject', 'object']].copy()
nodes.columns = ['id', 'label']

# Відкидаємо системні типи OWL/RDF, залишаємо лише наші медичні класи
system_types = ['NamedIndividual', 'Class', 'ObjectProperty', 'DatatypeProperty', 'Ontology', 'TransitiveProperty', 'Property']
nodes = nodes[~nodes['label'].isin(system_types)].drop_duplicates()

# 3. Формуємо зв'язки (edges.csv)
# Зв'язки — це всі триплети, де предикат не 'type', а об'єкт є серед списку id наших вузлів
valid_node_ids = set(nodes['id'])
edges = df[(df['predicate'] != 'type') & (df['object'].isin(valid_node_ids))].copy()
edges = edges[['subject', 'object', 'predicate']]
edges.columns = ['source', 'target', 'type']

# Зберігаємо результати
nodes.to_csv('nodes.csv', index=False)
edges.to_csv('edges.csv', index=False)

print(f"Готово! Створено вузлів: {len(nodes)}, створено зв'язків: {len(edges)}")