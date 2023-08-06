# -*- coding:utf-8 -*-


def between1(a,b):
    '''Print numbers between a and b'''
    if type(a) != type(int()) and type(b) != type(int()):
        raise TypeError('Must be integer.')
    result = []
    if a>b:
        for i in range(a-1,b):
            result.append(i)
    elif a<b:
        for i in range(a-1,b,-1):
            result.append(i)
    else:
        print('a and b must be different!')
    return result


def between2(l1,l2,a,b):
    '''Print numbers between l1[a] and l2[b]'''
    if type(l1) != type(list()) and type(l1) != type(tuple()) and type(l1) != type(dict()) and type(l2) != type(list()) and type(l2) != type(tuple()) and type(l1) != type(dict()):
        raise TypeError('l1, l2 must be list, dict or tuple.')
    if type(a) != type(int()) and type(b) != type(int()):
        raise TypeError('a, b must be integer.')
    result = []
    if l1[a]>l2[b]: 
        for i in range(l1[a-1],l2[b]):
            result.append(i)
    elif l1[a]<l2[b]:
        for i in range(l1[a-1],l2[b],-1):
            result.append(i)
    else:
        print('l1[a] and l2[b] must be different!')
    return result


def between3(s1,s2):
    l1 = ['nm','um','mm','cm','dm','m','km']
    l2 = ['nm2','um2','mm2','cm2','dm2','m2','hm2','km2']
    l3 = ['nm3','um3','mm3','cm3','dm3','m3','km3']
    l4 = ['mg','g','kg','t']
    if type(s1) != type(str()) and type(s2) != type(str()):
        raise TypeError('Must be string.')
    result = []
    if s1 in l1 and s2 in l2:
        try:
            if l1.index(s1)>l1.index(s2):
                for i in l1[l1.index(s1)-1:l1.index(s2)]:
                    result.append(i)
            elif l1.index(s1)<l1.index(s2):
                for i in l1[l1.index(s1)-1:l1.index(s2):-1]:
                    result.append(i)
            else:
                print('s1 and s2 must be different!')
        except ValueError:
            raise ValueError('s1 and s2 must be one of the units of length, area, volume and mass.')
    elif s1 in l2 and s2 in l2:
        try:
            if l2.index(s1)>l2.index(s2):
                for i in l2[l2.index(s1)-1:l2.index(s2)]:
                    result.append(i)
            elif l2.index(s1)<l2.index(s2):
                for i in l2[l2.index(s1)-1:l2.index(s2):-1]:
                    result.append(i)
            else:
                print('s1 and s2 must be different!')
        except ValueError:
            raise ValueError('s1 and s2 must be one of the units of length, area, volume and mass.')
    elif s1 in l3 and s2 in l3:
        try:
            if l3.index(s1)>l3.index(s2):
                for i in l3[l3.index(s1)-1:l3.index(s2)]:
                    result.append(i)
            elif l3.index(s1)<l3.index(s2):
                for i in l3[l3.index(s1)-1:l3.index(s2):-1]:
                    result.append(i)
            else:
                print('s1 and s2 must be different!')
        except ValueError:
            raise ValueError('s1 and s2 must be one of the units of length, area, volume and mass.')
    elif s1 in l4 and s2 in l4:
        try:
            if l4.index(s1)>l4.index(s2):
                for i in l4[l4.index(s1)-1:l4.index(s2)]:
                    result.append(i)
            elif l4.index(s1)<l4.index(s2):
                for i in l4[l4.index(s1)-1:l4.index(s2):-1]:
                    result.append(i)
            else:
                print('s1 and s2 must be different!')
        except ValueError:
            raise ValueError('s1 and s2 must be one of the units of length, area, volume and mass.')
    else:
        for i in range(4):
            if s1 in eval('l' + str(i+1)):
                raise ValueError('s1 and s2 must be same type.')
        raise ValueError('s1 and s2 must be one of the units of length, area, volume and mass.')
    return result
