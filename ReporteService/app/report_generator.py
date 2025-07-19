from collections import Counter

def resumen_por_estado(quejas):
    return dict(Counter(q.estado for q in quejas))

def resumen_por_origen(quejas):
    return dict(Counter(q.origen for q in quejas))
