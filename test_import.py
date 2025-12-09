import sys
import traceback
sys.path.insert(0, 'src')

try:
    import ui.views.activity_view as av
    print('✅ Module imported successfully')
    print('Exported classes:', [x for x in dir(av) if not x.startswith('_')])
    if hasattr(av, 'Dashboard_activity'):
        print('✅ Dashboard_activity found!')
    else:
        print('❌ Dashboard_activity NOT found!')
except Exception as e:
    print('❌ Import failed:')
    traceback.print_exc()
