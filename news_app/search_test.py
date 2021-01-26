items = [
    "Weinstein, Harvey",
    "Harvey Weinstein", 
    "Weinstein",
    "Hillary Clinton", 
    "Clinton, Hillary", 
    "Clinton", 
    "Cosby"
]

search_string = "Hillary Clinton"

def search_column(items, search_string):
    search_terms = search_string.split()
    found = False
    found_examples = []
    for item in items:
        terms_found = 0
        for term in search_terms:
            if term.lower() in item.lower():
                terms_found += 1
            if terms_found == len(search_terms):
                found = True
                found_examples.append(item)
    
    return found, found_examples
print(search_column(items, search_string))
