import numpy as np, matplotlib.pyplot as plt
import torch, torch.nn as nn
import locale
locale.setlocale(locale.LC_ALL, '') 

class ModelInfo:
    def __init__(self, model, beta=0.8):
        self.model = model
        self.beta  = min(0.999, max(0.001, beta)) 
        self.params = {}
        self.agg    = 0
    #---------------------------------------------------------------------------

    def num_params(self, grad=True):
        """
        Return number of model parameters

        Args:
        ------------
            grad (bool=True):
                parameters with gradient only (True), without gradient (False), all (None)
        """
        if grad == True:
            return sum([param.numel() for param in self.model.parameters() if param.requires_grad])
        if grad == False:
            return sum([param.numel() for param in self.model.parameters() if not param.requires_grad])
        return sum([param.numel() for param in self.model.parameters() ])


    #---------------------------------------------------------------------------

    def reset(self):
        """
        Set initial statistics values for each model parameter
        """
        self.params = dict()        
        for n, p in self.model.named_parameters():                        
            self.params[n] = {
                'numel': p.numel(),
                'shape': tuple(p.shape),
                'data' : torch.square(p.data).sum().cpu(),
                'min'  : p.data.abs().min().cpu(),
                'max'  : p.data.abs().max().cpu(),                              
                'grad' : 0,
            }
            if p.grad is not None:                    
                self.params[n]['grad'] = torch.square(p.grad).sum().cpu()

    #---------------------------------------------------------------------------

    def update(self):
        """
        Accumulate averages of statistics using exponential average
        """
        model = self.model
        if len(self.params) == 0:
            self.reset()
            return
        
        w1, w2 = 1-self.beta, self.beta
        for n, p in model.named_parameters():
            param = self.params[n]
            param['data'] = w1 * param['data'] + w2 * torch.square(p.data).sum().cpu()
            param['min']  = w1 * param['min']  + w2 * p.data.abs().min().cpu()
            param['max']  = w1 * param['max']  + w2 * p.data.abs().max().cpu()
            if p.grad is not None:                    
                if 'grad' not in param:
                    param['grad'] = torch.square(p.grad).sum().cpu()
                else:
                    param['grad'] = w1 * param['grad'] + w2 * torch.square(p.grad).sum().cpu()

    #---------------------------------------------------------------------------

    def get_groups(self, agg=0):
        """
        Create parameter group dictionaries (to aggregate statistics)

        Args:
        ------------
            agg (int=None):
                cut off the agg of the last levels of the parameter name to aggregate them (level0.weight -> level0)
        """        
        if agg is None:
            agg = self.agg
        else:
            self.agg = agg

        groups, names = dict(), dict()
        for n, _ in self.model.named_parameters():
            parts = n.split(".")
            parts = parts if agg==0 else parts[:- min(len(parts)-1, agg)]
            base  = ".".join(parts)                            
            if base in groups:
                groups[base]['names'].append(n)
            else:
                groups[base] = { 'names': [n], 'numel':[], 'data':[], 'min':[], 'max':[], 'shape':[], 'grad': [] }
            names[n] = base
        return groups, names

    #---------------------------------------------------------------------------

    def groups_init(self, groups):
        for group in groups.values():
            group['numel'] = []; group['shape']  = []; group['data']=[]; 
            group['min']   = []; group['max']  = []; 
            group['grad']  = []            

    #---------------------------------------------------------------------------

    def aggregate(self, agg=None):
        """
        """            
        groups, names = self.get_groups(agg=agg)
        self.groups_init(groups)
        if len(self.params) == 0:
            self.reset()
        
        for name, param in self.params.items():            
            group = names[name]
            groups[group]['numel'].append(param['numel']) 
            groups[group]['data'] .append( param['data'] )    
            groups[group]['grad'] .append( param['grad'] )                       
            groups[group]['min']  .append( param['min'])  
            groups[group]['max']  .append( param['max'])  
            groups[group]['shape'].append( param['shape'])    

        for group in groups.values():
            numel = group['numel'] = sum(group['numel'])
            group['data']  = (sum(group['data']) / numel)**0.5  if numel > 0 else 0
            group['min'] = min(group['min'])
            group['max'] = min(group['max'])
            group['shape'] = group['shape'][-1]         # ?
            if len(group['grad']):
                group['grad'] = (sum(group['grad']) / numel)**0.5  if numel > 0 else 0
            else:
                group['grad'] = 0

        return groups            

    #---------------------------------------------------------------------------

    def info(self, agg=None):
        """
        Вывести текстовую информацию о параметрах модели

        Args:
        ------------
            agg (int=None):
                агргировать число параметров по agg уровнях имени слоя, слева (shape показываться не будет)
        """
        groups = self.aggregate(agg=agg)
        w = max([len(n) for n in groups.keys() ])        
        print(f"{' '*w}    params     |mean|  [ min,         max ]  |grad|   shape")
        print("-"*(w+50))
        for name, group in groups.items():
            nm = name + " "*(w-len(name))
            print(f"{nm}  {group['numel']:9n} | {group['data']:8.3f}  [{group['min']:8.3f}, {group['max']:8.3f}]  {group['grad']:8.1e}  {group['shape']}  ")

        print("-"*(w+50))
        n1, n2, n3 = self.num_params(True),  self.num_params(False),  self.num_params(None)
        print(f"{'trainable'+' '*(w-9)}: {n1:9n}")
        if n2 or n3 != n1:
            print(f"{'other'+' '*(w-5)}: {n1:9n}")
            print(f"{'total'+' '*(w-5)}: {n3:9n}")

        return groups


    #---------------------------------------------------------------------------

    def plot(self, agg=None, data=True, grad=True, alpha=0.5, w=12, h=3):
        """
        Args:
        ------------
            agg (int=None):
                cut off the agg of the last levels of the parameter name to aggregate them (level0.weight -> level0)
            data (bool=True):
                show average absolute value of parameters
            grad (bool=True):
                show average absolute value of gradients
            alpha (float=0.5):
                transparency for bars of the number of elements in the parameter tensor
            w,h (int):
                chart width and height

        """
        groups = self.aggregate(agg=agg)
        numel, data, mi, ma, grad = [], [], [], [], []
        for name, group in groups.items():
            numel.append(group['numel'])
            data.append(group['data'])
            mi.append(group['min'])
            ma.append(group['max'])
            grad.append(group['grad'])
        x = np.arange(len(data))

        fig, ax = plt.subplots(1,1, figsize=(w, h))
        n1, n2 = self.num_params(), self.num_params(True)
        plt.title(f"params: {n2:n} ({100*n2/n1:.2f}%)")

        ax.set_yscale('log') 
        ax.bar(x, numel, label="num", alpha=alpha, color='lightgray')                
        ax.grid(ls=":")

        if data:
            ax1 = ax.twinx()     
            ax1.plot(x, data,   "-b.",  label="data")
            #ax1.errorbar(x, data,   yerr=[mi, ma],  fmt='-b.', elinewidth=2, capsize=4, lw=1)

            ax1.spines["left"].set_position(("outward", 30))
            ax1.spines["left"].set_visible(True)
            ax1.yaxis.set_label_position('left')
            ax1.yaxis.set_ticks_position('left')                
            ax1.set_ylabel("data", color='b')    
            ax1.tick_params(axis='y', colors='b')
        
        if grad:
            ax2 = ax.twinx()        
            ax2.plot(x, grad, "-r.", label="grad")                    
            ax2.set_ylabel("grad",  color='r')
            ax2.tick_params(axis='y', colors='r')

        plt.show()


"""
Метод parameters() - это генератор только по обучаемым параметрам (его мы передаём оптимизатору). 
Метод named_parameters() - аналогичный генератор, но дополнительно содержащий имена параметров. 
Эти два метода позволяют, в т.ч., достучаться до градиентов параметров. 
Кроме этого, есть словарь state_dict(), который обычно используется, 
когда модель сохраняется в файле для последующей загрузки. 
В нём присутствуют только данные и нет информации о градиентах, однако параметры есть все, включая не обучаемые. 
"""
