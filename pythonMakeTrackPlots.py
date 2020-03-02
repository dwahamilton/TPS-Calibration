import ROOT,itertools,math,pdb,copy
from DataFormats.FWLite import Events,Handle
from math import pi
ROOT.FWLiteEnabler.enable()
ROOT.gROOT.SetBatch(True)

class Plot:
  def __init__(self,fileName,plotName,plotLabel,plotColor,plotMarker,type=''):
    rootFile=ROOT.TFile(fileName,"OPEN")
    #pdb.set_trace()
    if type=='res':
      tempPlot=rootFile.Get(plotName)
      tempPlot.FitSlicesY()
      tempPlotRes=ROOT.gDirectory.Get(tempPlot.GetName()+'_2')
      self.plot=copy.deepcopy(tempPlotRes)
    else:
      self.plot=copy.deepcopy(rootFile.Get(plotName))

    self.plotLabel=plotLabel
    self.plotColor=plotColor
    self.plotMarker=plotMarker

class Plotter:
  def __init__(self,plotsStr,axisBounds,axisLabels,legBounds,PU,setLog,type='',addStr=''):
    self.plots=[]
    self.plotsStr=plotsStr
    self.axisBounds=axisBounds
    self.axisLabels=axisLabels
    self.legBounds=legBounds
    self.PU=PU
    self.addStr=addStr
    self.setLog=setLog
    self.type=type

  # Get plots from files
  def GetPlots(self,plots):
    for plot in plots:
      self.plots.append(plot)

  # Make canvas from plots
  def Plot(self):
    canv=ROOT.TCanvas(self.plotsStr,self.plotsStr,600,400)
    canv.cd()
    if self.setLog==1:
      canv.SetLogy()
    canv.SetGrid()
    if self.type=='AP':
      self.plots[0].plot.Draw("AP")
    else:
      self.plots[0].plot.Draw()
      self.plots[0].plot.SetStats(0)
    self.plots[0].plot.SetLineWidth(0)
    self.plots[0].plot.SetLineWidth(0)
    self.plots[0].plot.SetMarkerColor(0)
    self.plots[0].plot.SetTitle("")
    self.plots[0].plot.GetXaxis().SetRangeUser(self.axisBounds[0][0],self.axisBounds[0][1])
    self.plots[0].plot.GetYaxis().SetRangeUser(self.axisBounds[1][0],self.axisBounds[1][1])
    self.plots[0].plot.GetXaxis().SetTitle(self.axisLabels[0])
    self.plots[0].plot.GetXaxis().SetTitleSize(0.05)
    self.plots[0].plot.GetXaxis().SetTitleOffset(0.76)
    self.plots[0].plot.GetYaxis().SetTitle(self.axisLabels[1])
    self.plots[0].plot.GetYaxis().SetTitleSize(0.05)
    self.plots[0].plot.GetYaxis().SetTitleOffset(0.90)
    leg=ROOT.TLegend(self.legBounds[0],self.legBounds[1],self.legBounds[2],self.legBounds[3])
    leg.SetTextSize(0.0425)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetLineWidth(4)
    for plot in self.plots:
      if self.type=='AP':
        plot.plot.Draw("Psame")
      else:
        plot.plot.Draw("SAME")
      plot.plot.SetLineColor(plot.plotColor)
      plot.plot.SetLineWidth(1)
      plot.plot.SetMarkerStyle(plot.plotMarker)
      plot.plot.SetMarkerColor(plot.plotColor)
      leg.AddEntry(plot.plot,plot.plotLabel,"lp")
    leg.Draw()
    CMSText=ROOT.TPaveText(0.1,0.9,0.6,1,"NDC")
    CMSText.AddText("CMS Simulation, "+str(self.PU)+" PU"+self.addStr)
    CMSText.SetBorderSize(0)
    CMSText.SetFillStyle(0)
    CMSText.Draw()
    canv.Write()
    #canv.SaveAs('/uscms_data/d3/davidh/CMSSW_10_6_1_patch2/src/Rootfiles/Plots/TPSPNGs/'+self.plotsStr+'.png')

# Make plotters and common parameters
plotters=[]
muPlotFileP1='Rootfiles/pythonOut/tdrPlots_singleMu200.root'
muPlotFileP2='Rootfiles/pythonOut/tdrPlots_singleMu200_DTAM.root'
muPlotFileIsol='Rootfiles/pythonOut/tdrPlots_singleMu200_isol.root'
nuPlotFileP1='Rootfiles/pythonOut/tdrPlots_singleNu200.root'
nuPlotFileP2='Rootfiles/pythonOut/tdrPlots_singleNu200_DTAM.root'
nuPlotFileIsol='Rootfiles/pythonOut/tdrPlots_singleNu200_isol.root'
plotFile='/uscms_data/d3/davidh/CMSSW_10_6_1_patch2/src/Rootfiles/pythonOut/TPSPlotsFermi.root'

PU=200

# Get mu eff plots
effMu={}
rateNu={}
phaseName={'P1':'P1','P2':'P2','isol':'P1 Isol'}
muFileName={'P1':muPlotFileP1,'P2':muPlotFileP2,'isol':muPlotFileIsol}
nuFileName={'P1':nuPlotFileP1,'P2':nuPlotFileP2,'isol':nuPlotFileIsol}
phaseColor={'P1':ROOT.kRed,'P2':ROOT.kBlue,'isol':ROOT.kBlack}
effVarList=['Pt','Eta']
rateVarList=['rate','rateVsPU_']
ptList=['0','3','5','10','15','20']

for phase in phaseName:
  for var in rateVarList:
    rateNu[phase,var]=Plot(nuFileName[phase],var+'TPS',phaseName[phase],phaseColor[phase],6)
  for var in effVarList:
    for pt in ptList:
      muPlotName='effVs'+var+'TPS'+pt
      effMu[phase,var,pt]=Plot(muFileName[phase],muPlotName,phaseName[phase],phaseColor[phase],6)

# Eff parameters
effAxisBounds={'Pt':[[0,100],[0,1]],'Eta':[[-0.85,0.85],[0,1]]}
effAxisLabels={'Pt':['gen. #mu p_{T}','Eff.'],'Eta':['gen. #mu #eta','Eff.']}
effLegBounds=[0.75,0.1,0.95,0.25]

# Rate parameters
rateAxisBounds={'rate':[[0,100],[1e-1,1e3]],'rateVsPU_':[[0,300],[0,20]]}
rateAxisLabels={'rate':['Threshold (GeV)','Rate (kHz)'],'rateVsPU_':['PU','Rate (kHz)']}
rateLegBounds=[0.75,0.4,0.95,0.55]

# Eff plotters
effPlotList={'PComp':['P1','P2'],'isolComp':['P1','isol']}
effPlotter={}
for var in effVarList:
  for pt in ptList:
    for list in effPlotList:
      effPlotStr='eff'+var+pt+'GeV_'+list
      effPlotter[var,pt,list]=Plotter(effPlotStr,effAxisBounds[var],effAxisLabels[var],effLegBounds,PU,0,'AP')
      effPlotter[var,pt,list].GetPlots([effMu[phase,var,pt] for phase in effPlotList[list]])
      plotters.append(effPlotter[var,pt,list])

# Rate plotters
ratePlotList={'PComp':['P1','P2'],'isolComp':['P1','isol']}
ratePlotter={}
APList={'rate':'AP','rateVsPU_':''}
logList={'rate':1,'rateVsPU_':0}
for var in rateVarList:
  for list in ratePlotList:
    ratePlotStr=var+'_'+list
    ratePlotter[var,list]=Plotter(ratePlotStr,rateAxisBounds[var],rateAxisLabels[var],rateLegBounds,PU,logList[var],APList[var])
    ratePlotter[var,list].GetPlots([rateNu[phase,var] for phase in ratePlotList[list]])
    plotters.append(ratePlotter[var,list])

# Get mu res plots
detectorRes={}
phaseName={'P1':'P1','P2':'P2'}
phaseColor={'P1':ROOT.kRed,'P2':ROOT.kBlue}
phiPlot={'phi':'deltaPhiK','phiB':'deltaPhiBK_unSc'}
for phase in ['P1','P2']:
  for detector in ['1','5','8','10']:
    for eta in ['0','1','3']:
      for phi in phiPlot:
        plotName='detector'+detector+'/eta'+eta+'/'+phase+'/detector'+detector+'_eta'+eta+'_'+phase+'_'+phiPlot[phi]
        detectorRes[detector,eta,phi,phase]=Plot(plotFile,plotName,phaseName[phase],phaseColor[phase],21,'res')

# Res parameters
resAxisBounds={('1','phi'):[[-870,870],[0,100]],('5','phi'):[[-870,870],[0,100]],('8','phi'):[[-870,870],[0,100]],('10','phi'):[[-870,870],[0,100]],('1','phiB'):[[-870,870],[0,400]],('5','phiB'):[[-870,870],[0,475]],('8','phiB'):[[-870,870],[0,550]],('10','phiB'):[[-870,870],[0,800]]}
resAxisLabels={'phi':['k','#sigma_{#phi}'],'phiB':['k','#sigma_{#phi_{b}}']}
resLegBounds=[0.45,0.75,0.65,0.9]
addStr={('1','0'):'St.1, Wh.0',('1','1'):'St.1, Wh.1',('1','3'):'St.1, Wh.2',('5','0'):'St.2, Wh.0',('5','1'):'St.2, Wh.1',('5','3'):'St.2, Wh.2',('8','0'):'St.3, Wh.0',('8','1'):'St.3, Wh.1',('8','3'):'St.3, Wh.2',('10','0'):'St.4, Wh.0',('10','1'):'St.4, Wh.1',('10','3'):'St.4, Wh.2'}

resPlotter={}
for detector in ['1','5','8','10']:
  for eta in ['0','1','3']:
    for phi in phiPlot:
      resPlotStr='resPlot_detector'+detector+'_eta'+eta+'_'+phi
      resPlotter[detector,eta,phi]=Plotter(resPlotStr,resAxisBounds[detector,phi],resAxisLabels[phi],resLegBounds,PU,0,'',', '+addStr[detector,eta])
      resPlotter[detector,eta,phi].GetPlots([detectorRes[detector,eta,phi,'P1'],detectorRes[detector,eta,phi,'P2']])
      plotters.append(resPlotter[detector,eta,phi])

# Make and write canvases to file
fileName='/uscms_data/d3/davidh/CMSSW_10_6_1_patch2/src/Rootfiles/Plots/TPSPlots.root'
f=ROOT.TFile(fileName,'RECREATE')
f.cd()
for plotter in plotters:
  plotter.Plot()
f.Close()
