import ROOT as r
from matplotlib import colors as clr
import numpy as np

class pyStack():
    def __init__(self, drawOrder):
        self.stack = list()
        self.colors = list()
        self.edgecolors = list()
        self.names = list()
        self.fancyNames = None
        self.bins = None
        self.hists = list()
        self.rHistTotal = None
        self.align = 'left'
        self.title = None
        
        for name, hist in drawOrder:
            self.names.append(name)
            if not self.title: self.title =hist.GetName()
            if not self.bins:  self._setupBins(hist)
            self.hists.append(hist)
            tmp = list()
            for i in range(1, hist.GetNbinsX()+1):
                tmp.append(hist.GetBinContent(i))
            self.stack.append(tmp)
            if not self.rHistTotal:
                self.rHistTotal = hist.Clone(self.title)
            else:
                self.rHistTotal.Add(hist)
        
    def setColors(self, colorMap):
        for name in self.names:
            self.colors.append(colorMap[name])
            self.edgecolors.append(self._darkenColor(colorMap[name]))

    def setLegendNames(self, info):
        self.fancyNames = list()
        for name in self.names:
            fName = info.getLegendName(name)
            if '\\' in fName:
                fName = r'$%s$' % fName
            self.fancyNames.append(fName)

    def _darkenColor(self, color):
        cvec = clr.to_rgba(color)
        dark = 0.3
        return tuple([i - dark if i > dark else 0.0 for i in cvec])
    
    def _setupBins(self, hist):
        self.bins = list()
        for i in range(1, hist.GetNbinsX()+2):
            self.bins.append(hist.GetBinLowEdge(i))

    def getRHist(self):
        return self.rHistTotal

                
    def getXVal(self):
        return [self.bins[:-1]]*len(self.stack)

        
    def getInputs(self):
        return {"weights":self.stack, "x":self.getXVal(), "bins":self.bins, "histtype":'stepfilled', "color":self.colors, "stacked":True, "label":self.fancyNames, 'align':self.align}

    def applyPatches(self, plot, patches):
        for p, ec in zip(patches, self.edgecolors):
            plot.setp(p, edgecolor=ec)