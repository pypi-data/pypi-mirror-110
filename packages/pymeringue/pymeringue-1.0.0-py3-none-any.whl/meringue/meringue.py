import builtins

class Meringue(list):
    def last(self):
        return self.at(-1)
        
    def unique(self):
        print(self)
        return Meringue([i for n, i in enumerate(self) if i not in self[:n]])
        
    def removeAllInstances(self, *items):
        temp = self
        for item in items:
            temp = filter(lambda i : i != item, temp)
        return Meringue(temp)
        
    def removeCommonElements(self, *lists):
        _list = self.flat(lists)
        return Meringue(filter(lambda i : i not in _list, self))
            
    def flat(self, _list):
        if not _list:
            _list = self
        temp = []
        for item in _list:
            if isinstance(item, (list, tuple)):
                for subitem in item: 
                    temp.append(subitem)
            else:
                temp.append(item)
        return Meringue(temp)
        
    def at(self, n=0):
        return self[n]

builtins.Meringue = Meringue