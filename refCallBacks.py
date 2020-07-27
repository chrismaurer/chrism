
            print '\n------- callbacks -------\n'
            print callbacks.keys()
            print '\n.....'
            print dir(callbacks[0])
            print '\n.....'
            print dir(callbacks[1])
            print '\n.....'
            print type(callbacks['OnOrderFilled'][0]['order'])
            print '\n.....'
            print dir(callbacks['OnOrderFilled'][0]['order'])
            print '\n.....'
            print callbacks['OnOrderFilled'][0]['order']
            print '\n.....'
            print type(callbacks['OnFillRecord'][0]['fill'])
            print '\n.....'
            print dir(callbacks['OnFillRecord'][0]['fill'])
            print '\n.....'
            print callbacks['OnFillRecord'][0]['fill']
            print '\n.....'