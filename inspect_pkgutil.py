import pkgutil, sys, json, os
print('pkgutil module:', pkgutil)
print('__file__:', getattr(pkgutil, '__file__', None))
print('has get_loader:', hasattr(pkgutil, 'get_loader'))
print('get_loader repr:', repr(getattr(pkgutil, 'get_loader', None)))
print('\n--- sys.path (first 20) ---')
for p in sys.path[:20]:
    print(p)

# Check for local files that could shadow pkgutil
print('\n--- local files named pkgutil.* in project root ---')
root = os.path.dirname(__file__)
for name in os.listdir(root):
    if name.startswith('pkgutil'):
        print(name)

# Print installed pkgutil package location if available via importlib
try:
    import importlib.util
    spec = importlib.util.find_spec('pkgutil')
    print('\nfind_spec for pkgutil ->', spec)
except Exception as e:
    print('find_spec error:', e)
