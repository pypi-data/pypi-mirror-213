import requests
import pendulum

url_double_recent = 'https://blaze.com/api/roulette_games/recent'
url_double_current = 'https://blaze.com/api/roulette_games/current'
url_double_history = 'https://blaze.com/api/roulette_games/history'
url_crash_recent = 'https://blaze.com/api/crash_games/recent'
url_crash_current = 'https://blaze.com/api/crash_games/current'
url_crash_history = 'https://blaze.com/api/crash_games/history'

def Last_Results_Double(
        *args,
        cor=False,
        numero=False,
        horario=False,
        id=False,
):
    br_tz = pendulum.now().timezone_name

    results = {
        'cores': [],
        'numeros': [],
        'ids': [],
        'horarios': [],

    }

    requisicao20 = requests.get(url_double_history).json()['records']

    for i,it in reversed(list(enumerate(requisicao20))):
      
        if 'id' in requisicao20[i]:
            results['ids'].append(requisicao20[i]['id'])
      
        if 'color' in requisicao20[i]:
            results['cores'].append(requisicao20[i]['color'])
      
        if 'roll' in requisicao20[i]:
            results['numeros'].append(requisicao20[i]['roll'])
      
        if 'created_at' in requisicao20[i]:
            convert = pendulum.parse(requisicao20[i]['created_at']).in_timezone(br_tz)
            results['horarios'].append(convert)

    if cor:
        if args:
            if len(args) == 2:
                return results['cores'][args[0]:args[1]]
            elif len(args) < 2:
                return results['cores'][args[0]]
        else:
            return results['cores']
    
    elif numero:
        if args:
            if len(args) == 2:
                return results['numeros'][args[0]:args[1]]
            elif len(args) < 2:
                return results['numeros'][args[0]]
        else:
            return results['numeros']
        
    elif horario:
        if args:
            if len(args) == 2:
                return results['horarios'][args[0]:args[1]]
            elif len(args) < 2:
                return results['horarios'][args[0]]
        else:
            return results['horarios']
        
    elif id:
        if args:
            if len(args) == 2:
                return results['ids'][args[0]:args[1]]
            elif len(args) < 2:
                return results['ids'][args[0]]
        else:
            return results['ids']
    
    else:
        return results
    

def Status_double():
    
    return requests.get(url_double_current).json()["status"]


def Last_Results_crash(
        *args,
        crash_point=False,
        horario=False,
        id=False,
):
    br_tz = pendulum.now().timezone_name

    results = {
        'crash_point': [],
        'ids': [],
        'horarios': [],

    }

    requisicao20 = requests.get(url_crash_history).json()['records']

    for i,it in reversed(list(enumerate(requisicao20))):
      
        if 'id' in requisicao20[i]:
            results['ids'].append(requisicao20[i]['id'])
      
        if 'crash_point' in requisicao20[i]:
            results['crash_point'].append(float(requisicao20[i]['crash_point']))
      
        if 'created_at' in requisicao20[i]:
            convert = pendulum.parse(requisicao20[i]['created_at']).in_timezone(br_tz)
            results['horarios'].append(convert)
    
    if crash_point:
        if len(args) > 0:
            if len(args) == 2:
                return results['crash_point'][args[0]:args[1]]
            elif len(args) < 2:
                return results['crash_point'][args[0]]
        else:
            return results['crash_point']
        
    elif horario:
        if len(args) > 0:
            if len(args) == 2:
                return results['horarios'][args[0]:args[1]]
            elif len(args) < 2:
                return results['horarios'][args[0]]
        else:
            return results['horarios']
        
    elif id:
        if len(args) > 0:
            if len(args) == 2:
                return results['ids'][args[0]:args[1]]
            elif len(args) < 2:
                return results['ids'][args[0]]
        else:
            return results['ids']
    
    else:
        return results
    
    
def Status_crash():
    
    return requests.get(url_crash_current).json()["status"]
