import ast

x = raw_input('Enter the dict')
x = ast.literal_eval(x)
print x['c'], x['iter']
print x

x = {'hidden_layer_sizes': [(100,40),(200,50)], 'alpha':[3,5,7]}