from __future__ import print_function
import ROOT,itertools,math
from array import array
from DataFormats.FWLite import Events, Handle
import copy
import pdb
ROOT.FWLiteEnabler.enable()

tag='root://cmseos.fnal.gov//store/user/bachtis/PhaseII_19_10_04/singleMu0'
#tag='root://cmseos.fnal.gov//store/user/bachtis/Mu_FlatPt2to100-pythia8-gun/PHASEII_SingleMu0/190930_194739/0000/test_3'

PHILSB=0.00019174760
ETALSB=0.00585938
CURVLSB=0.000122070

binsPhiMean={0:101,1:67,2:67,3:67}
binsPhiMeanK={0:101,1:67,2:67,3:67}
binsPhiBMean=75
binsPhiBMeanK=75

etaIndexMaxes={1:[51,99,142,176,216],2:[43,85,123,159,192],3:[38,75,106,137,169],4:[31,61,90,121,142]}
typeList=[0,1]
depthList=xrange(1,5)
etaList=xrange(0,5)
phases={'P1':'l1TPSStubs','P2':'l1TPSStubsAM'}
#phases={'P2':'l1TPSStubsAM'}

etaIndices={}
for depth in depthList:
  for eta in etaList:
    if eta==0:
      etaIndices[depth,eta]=[0,etaIndexMaxes[depth][eta]]
    else:
      etaIndices[depth,eta]=[etaIndexMaxes[depth][eta-1]+1,etaIndexMaxes[depth][eta]]

#phiOffset={(1,0):17.380,(1,1):18.680,(1,2):20.102,(1,3):20.532,(1,4):16.532,(2,0):-9.048,(2,1):-7.916,(2,2):-16.380,(2,3):-16.560,(2,4):-8.857,(3,0):7.264,(3,1):7.022,(3,2):3.550,(3,3):8.639,(3,4):12.27,(4,0):3.395,(4,1):0.012,(4,2):1.417,(4,3):0.562,(4,4):3.441,(1,-1):0,(2,-1):0,(3,-1):0,(4,-1):0}
phiOffset={(1,'P1'):17,(2,'P1'):-12,(3,'P1'):8,(4,'P1'):2,(1,'P2'):0,(2,'P2'):0,(3,'P2'):0,(4,'P2'):0}

#phiBConv={(1,0,'unSc','P1'):1,(1,1,'unSc','P1'):1,(1,2,'unSc','P1'):1,(1,3,'unSc','P1'):1,(1,4,'unSc','P1'):1,(2,0,'unSc','P1'):1,(2,1,'unSc','P1'):1,(2,2,'unSc','P1'):1,(2,3,'unSc','P1'):1,(2,4,'unSc','P1'):1,(3,0,'unSc','P1'):1,(3,1,'unSc','P1'):1,(3,2,'unSc','P1'):1,(3,3,'unSc','P1'):1,(3,4,'unSc','P1'):1,(4,0,'unSc','P1'):1,(4,1,'unSc','P1'):1,(4,2,'unSc','P1'):1,(4,3,'unSc','P1'):1,(4,4,'unSc','P1'):1,(1,-1,'unSc','P1'):1,(2,-1,'unSc','P1'):1,(3,-1,'unSc','P1'):1,(4,-1,'unSc','P1'):1,(1,0,'unSc','P2'):1,(1,1,'unSc','P2'):1,(1,2,'unSc','P2'):1,(1,3,'unSc','P2'):1,(1,4,'unSc','P2'):1,(2,0,'unSc','P2'):1,(2,1,'unSc','P2'):1,(2,2,'unSc','P2'):1,(2,3,'unSc','P2'):1,(2,4,'unSc','P2'):1,(3,0,'unSc','P2'):1,(3,1,'unSc','P2'):1,(3,2,'unSc','P2'):1,(3,3,'unSc','P2'):1,(3,4,'unSc','P2'):1,(4,0,'unSc','P2'):1,(4,1,'unSc','P2'):1,(4,2,'unSc','P2'):1,(4,3,'unSc','P2'):1,(4,4,'unSc','P2'):1,(1,-1,'unSc','P2'):1,(2,-1,'unSc','P2'):1,(3,-1,'unSc','P2'):1,(4,-1,'unSc','P2'):1,(1,0,'sc','P1'):1,(1,1,'sc','P1'):1,(1,2,'sc','P1'):1,(1,3,'sc','P1'):1,(1,4,'sc','P1'):1,(2,0,'sc','P1'):1,(2,1,'sc','P1'):1,(2,2,'sc','P1'):1,(2,3,'sc','P1'):1,(2,4,'sc','P1'):1,(3,0,'sc','P1'):1,(3,1,'sc','P1'):1,(3,2,'sc','P1'):1,(3,3,'sc','P1'):1,(3,4,'sc','P1'):1,(4,0,'sc','P1'):1,(4,1,'sc','P1'):1,(4,2,'sc','P1'):1,(4,3,'sc','P1'):1,(4,4,'sc','P1'):1,(1,-1,'sc','P1'):1,(2,-1,'sc','P1'):1,(3,-1,'sc','P1'):1,(4,-1,'sc','P1'):1,(1,0,'sc','P2'):1.531/0.8890,(1,1,'sc','P2'):1.520/0.9615,(1,2,'sc','P2'):1.493/0.8669,(1,3,'sc','P2'):1.520/0.7848,(1,4,'sc','P2'):1.429/0.6938,(2,0,'sc','P2'):1.671/0.6629,(2,1,'sc','P2'):1.664/0.6487,(2,2,'sc','P2'):1.649/0.6310,(2,3,'sc','P2'):1.616/0.5484,(2,4,'sc','P2'):1.573/0.4704,(3,0,'sc','P2'):1.745/0.3585,(3,1,'sc','P2'):1.754/0.3492,(3,2,'sc','P2'):1.737/0.3359,(3,3,'sc','P2'):1.714/0.3058,(3,4,'sc','P2'):1.687/0.2712,(4,0,'sc','P2'):1.818/0.1182,(4,1,'sc','P2'):1.793/0.1241,(4,2,'sc','P2'):1.782/0.1168,(4,3,'sc','P2'):1.766/0.1178,(4,4,'sc','P2'):1.738/0.1123,(1,-1,'sc','P2'):1,(2,-1,'sc','P2'):1,(3,-1,'sc','P2'):1,(4,-1,'sc','P2'):1}
phiBConv={(1,0,'unSc','P1'):1,(1,1,'unSc','P1'):1,(1,2,'unSc','P1'):1,(1,3,'unSc','P1'):1,(1,4,'unSc','P1'):1,(2,0,'unSc','P1'):1,(2,1,'unSc','P1'):1,(2,2,'unSc','P1'):1,(2,3,'unSc','P1'):1,(2,4,'unSc','P1'):1,(3,0,'unSc','P1'):1,(3,1,'unSc','P1'):1,(3,2,'unSc','P1'):1,(3,3,'unSc','P1'):1,(3,4,'unSc','P1'):1,(4,0,'unSc','P1'):1,(4,1,'unSc','P1'):1,(4,2,'unSc','P1'):1,(4,3,'unSc','P1'):1,(4,4,'unSc','P1'):1,(1,-1,'unSc','P1'):1,(2,-1,'unSc','P1'):1,(3,-1,'unSc','P1'):1,(4,-1,'unSc','P1'):1,(1,0,'unSc','P2'):1,(1,1,'unSc','P2'):1,(1,2,'unSc','P2'):1,(1,3,'unSc','P2'):1,(1,4,'unSc','P2'):1,(2,0,'unSc','P2'):1,(2,1,'unSc','P2'):1,(2,2,'unSc','P2'):1,(2,3,'unSc','P2'):1,(2,4,'unSc','P2'):1,(3,0,'unSc','P2'):1,(3,1,'unSc','P2'):1,(3,2,'unSc','P2'):1,(3,3,'unSc','P2'):1,(3,4,'unSc','P2'):1,(4,0,'unSc','P2'):1,(4,1,'unSc','P2'):1,(4,2,'unSc','P2'):1,(4,3,'unSc','P2'):1,(4,4,'unSc','P2'):1,(1,-1,'unSc','P2'):1,(2,-1,'unSc','P2'):1,(3,-1,'unSc','P2'):1,(4,-1,'unSc','P2'):1,(1,0,'sc','P1'):1,(1,1,'sc','P1'):1,(1,2,'sc','P1'):1,(1,3,'sc','P1'):1,(1,4,'sc','P1'):1,(2,0,'sc','P1'):1,(2,1,'sc','P1'):1,(2,2,'sc','P1'):1,(2,3,'sc','P1'):1,(2,4,'sc','P1'):1,(3,0,'sc','P1'):1,(3,1,'sc','P1'):1,(3,2,'sc','P1'):1,(3,3,'sc','P1'):1,(3,4,'sc','P1'):1,(4,0,'sc','P1'):1,(4,1,'sc','P1'):1,(4,2,'sc','P1'):1,(4,3,'sc','P1'):1,(4,4,'sc','P1'):1,(1,-1,'sc','P1'):1,(2,-1,'sc','P1'):1,(3,-1,'sc','P1'):1,(4,-1,'sc','P1'):1,(1,0,'sc','P2'):1.84,(1,1,'sc','P2'):1.84,(1,2,'sc','P2'):1.84,(1,3,'sc','P2'):1.84,(1,4,'sc','P2'):1.84,(2,0,'sc','P2'):2.96,(2,1,'sc','P2'):2.96,(2,2,'sc','P2'):2.96,(2,3,'sc','P2'):2.96,(2,4,'sc','P2'):2.96,(3,0,'sc','P2'):5.52,(3,1,'sc','P2'):5.52,(3,2,'sc','P2'):5.52,(3,3,'sc','P2'):5.52,(3,4,'sc','P2'):5.52,(4,0,'sc','P2'):15.28,(4,1,'sc','P2'):15.28,(4,2,'sc','P2'):15.28,(4,3,'sc','P2'):15.28,(4,4,'sc','P2'):15.28,(1,-1,'sc','P2'):1,(2,-1,'sc','P2'):1,(3,-1,'sc','P2'):1,(4,-1,'sc','P2'):1}
phiBConvHist=copy.deepcopy(phiBConv)
#phiBScaleOld={1:16*1.7370158,2:16*2.6109661,3:16*4.4111160,4:16*11.660448}
#for depth in depthList:
  #for eta in etaList:
    #phiBConvHist[depth,eta,'unSc','P2']*=phiBScaleOld[depth]
    #phiBConvHist[depth,eta,'sc','P2']*=phiBScaleOld[depth]

def fetchStubs(event,tag):
  phiSeg2=Handle('std::vector<L1MuCorrelatorHit>')
  event.getByLabel(tag,phiSeg2)

  return phiSeg2.product()

def fetchGEN(event,etaMax=3.0):
  genH=Handle('vector<reco::GenParticle>')
  event.getByLabel('genParticles',genH)
  genMuons=filter(lambda x: abs(x.pdgId())==13 and x.status()==1 and abs(x.eta())<etaMax,genH.product())

  return genMuons

def fetchGEANT(event):
  geantH=Handle('vector<PSimHit>')
  event.getByLabel('g4SimHits:MuonDTHits',geantH)
  geant=filter(lambda x: x.pabs()>0.5 and abs(x.particleType())==13,geantH.product())

  return geant

def getTrueBarrelChambers(muon,geant):
  thisMuonGEANT=filter(lambda x: (muon.charge()>0 and x.particleType()==-13) or ((muon.charge()<0) and x.particleType()==13),geant)
  chambers=[]
  for p in thisMuonGEANT:
    detid=ROOT.DTChamberId(p.detUnitId())
    info={'wheel':detid.wheel(),'sector':detid.sector()-1,'station':detid.station()}
    isThereAlready=False
    for c in chambers:
      if info['wheel']==c['wheel'] and info['sector']==c['sector'] and info['station']==c['station']:
        isThereAlready=True
        break
    if not isThereAlready:
      chambers.append(info)

  return chambers

def getMatchedBarrelStubs(muon,geant,stubs):
  matched=[]
  chambers=getTrueBarrelChambers(muon,geant)
  for s in stubs:
    for c in chambers:
      if s.stNum()==c['station'] and s.whNum()==c['wheel'] and s.scNum()==c['sector']:
        matched.append(s)
        break

  return matched

def deltaPhi(phi1,phi2):
  pi=int(3.14159/PHILSB)
  delta=phi1-phi2
  if delta>pi:
    return delta-2*pi
  if delta<-pi:
    return delta+2*pi

  return delta

def deltaR(*args):
  return math.sqrt(deltaR2(*args))

def deltaR2(e1,p1,e2,p2):
  de=e1-e2
  dp=deltaPhi(p1,p2)

  return de*de+dp*dp

def runStubs(stubs,phase,histoData,g):
  genPhi=int((g.phi()/PHILSB))
  genEta=int(g.eta()/ETALSB)
  genK=int(g.charge()/g.pt()/CURVLSB)

  for stub in stubs:
    if stub.type() not in typeList:
      continue
    eta=-1
    for etaInd in xrange(0,5):
      if abs(genEta)>=etaIndices[stub.depthRegion(),etaInd][0] and abs(genEta)<=etaIndices[stub.depthRegion(),etaInd][1]:
        eta=etaInd
        break

    if abs(deltaPhi(genPhi,stub.phi()))>math.pi/2./PHILSB or eta==-1:
      continue
    histoData[stub.type()][stub.depthRegion(),eta,phase]['phi'].Fill(genK,deltaPhi(stub.phi()-phiOffset[stub.depthRegion(),phase],genPhi))
    if (stub.type()==0):
      histoData[stub.type()][stub.depthRegion(),eta,phase]['phiBUnSc'].Fill(genK,phiBConv[stub.depthRegion(),eta,'unSc',phase]*stub.phiB())
      histoData[stub.type()][stub.depthRegion(),eta,phase]['phiBSc'].Fill(genK,phiBConv[stub.depthRegion(),eta,'sc',phase]*stub.phiB())

events=Events([tag+'.root'])

histoData={}

for t in typeList:
  histoData[t]={}
  for depth in depthList:
    for eta in etaList:
      for phase in phases:
        histoData[t][depth,eta,phase]={}
        histoData[t][depth,eta,phase]['phi']=ROOT.TH2F("propPhi_"+phase+"_type_"+str(t)+"_depth_"+str(depth)+"_eta_"+str(eta),"propPhi_"+phase+"_type_"+str(t)+"_depth_"+str(depth)+"_eta_"+str(eta),binsPhiMeanK[t],-4160,4160,binsPhiMean[t],-4000,4000)
        if t==0:
          histoData[t][depth,eta,phase]['phiBUnSc']=ROOT.TH2F("propPhiB_"+phase+"_type_"+str(t)+"_depth_"+str(depth)+"_eta_"+str(eta)+"_unSc","propPhiB_"+phase+"_type_"+str(t)+"_depth_"+str(depth)+"_eta_"+str(eta)+"_unSc",binsPhiBMeanK,-4160,4160,binsPhiBMean,-phiBConvHist[depth,eta,'unSc',phase]*4000,phiBConvHist[depth,eta,'unSc',phase]*4000)
          histoData[t][depth,eta,phase]['phiBSc']=ROOT.TH2F("propPhiB_"+phase+"_type_"+str(t)+"_depth_"+str(depth)+"_eta_"+str(eta)+"_sc","propPhiB_"+phase+"_type_"+str(t)+"_depth_"+str(depth)+"_eta_"+str(eta)+"_sc",binsPhiBMeanK,-4160,4160,binsPhiBMean,-phiBConvHist[depth,eta,'sc',phase]*4000,phiBConvHist[depth,eta,'sc',phase]*4000)

counter=-1
for event in events:
  counter=counter+1
  gen=fetchGEN(event)

  stubsList={}
  for phase,stubsName in phases.iteritems():
    stubsList[phase]=fetchStubs(event,stubsName)

  for g in gen:
    for phase,stubs in stubsList.iteritems():
      runStubs(stubs,phase,histoData,g)

f=ROOT.TFile("Rootfiles/pythonOut/mu0New.root","RECREATE")
f.cd()
for t,dictio in histoData.iteritems():
  for key,dictio2 in dictio.iteritems():
    if t==0:
      dictio2['phiBUnSc'].Write()
      dictio2['phiBSc'].Write()
    dictio2['phi'].Write()

f.Close()
