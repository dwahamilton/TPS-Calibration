from __future__ import print_function
import ROOT,itertools,math
from array import array
from DataFormats.FWLite import Events, Handle
from ROOT import gStyle
import copy
import pdb
ROOT.FWLiteEnabler.enable()
ROOT.gROOT.SetBatch(True)

#verbose=False
#tag='singleMuonOfficial'
#isData=False
#tag='/scratch3/MTF/data/190401/singleMu0'
tag='root://cmseos.fnal.gov//store/user/bachtis/PhaseII_19_10_04/singleMu0'
#tag='root://cmseos.fnal.gov//store/user/bachtis/Mu_FlatPt2to100-pythia8-gun/PHASEII_SingleMu0/190930_194739/0000/test_3'

PHILSB=0.00019174760
ETALSB=0.00585938
CURVLSB=0.000122070

binsPhiRes={0:75,1:67,2:67,3:67}
binsPhiResK={0:75,1:67,2:67,3:67}
binsPhiBRes=75
binsPhiBResK=101

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
      if s.depthRegion()==c['station'] and s.etaRegion()==c['wheel'] and s.phiRegion()==c['sector']:
        matched.append(s)
        break

  return matched

def deltaPhi(phi1,phi2):
  pi=int(3.14159/PHILSB)
  delta=phi1-phi2
  while delta>pi:
    delta-=2*pi
  while delta<-pi:
    delta+=2*pi

  return delta

def phiProp(k,phi,slope):
  pi=int(3.14159/PHILSB)
  phiPropagate=int(slope*k+phi)
  while phiPropagate>pi:
    phiPropagate-=2*pi
  while phiPropagate<-pi:
    phiPropagate+=2*pi

  return phiPropagate

def pullPhi(k,delta,aRes,bRes):
  return delta/(aRes*abs(k)+bRes)

def fitPull(hist):
  fit=ROOT.TF1('gaus','gaus',-3,3)
  hist.Fit(fit,"R")
  gStyle.SetOptFit()

def runStubs(stubs,phase,hists,g,fillType):
  genPhi=int(g.phi()/PHILSB)
  genEta=int(g.eta()/ETALSB)
  genK=int(g.charge()/g.pt()/CURVLSB)
  if abs(genEta)>0:
    genEtaSign=genEta/abs(genEta)
  else:
    genEtaSign=1

  for s in stubs:
    stubType=s.type()
    stubDepth=s.depthRegion()
    stubWheel=s.etaRegion()

    eta=-1
    for etaInd in xrange(0,5):
       if abs(genEta)>=etaIndices[stubDepth,etaInd][0] and abs(genEta)<=etaIndices[stubDepth,etaInd][1]:
           eta=etaInd
           break

    stubPhi=s.phi()-phiOffset[stubDepth,phase]

    stubPhiBUnSc=int(phiBConv[stubDepth,eta,'unSc',phase]*s.phiB())
    stubPhiBSc=int(phiBConv[stubDepth,eta,'sc',phase]*s.phiB())

    if abs(deltaPhi(genPhi,stubPhi))>math.pi/2./PHILSB:
      continue
    for hist in hists.values():
      if hist.phase!=phase:
        continue
      type=hist.type
      depth=hist.depth
      eta=hist.eta
      etaLow=hist.etaIndices[0]
      etaHigh=hist.etaIndices[1]

      if eta==0:
        wh=0
      elif eta==1 or eta==2:
        wh=1*genEtaSign
      elif eta==3 or eta==4:
        wh=2*genEtaSign

      if stubType!=type or stubDepth!=depth or stubWheel!=wh or (abs(genEta)<etaLow or abs(genEta)>etaHigh):
        continue

      slope=hist.slope
      stubPhiProp=phiProp(genK,genPhi,slope)
      delta=deltaPhi(stubPhi,stubPhiProp)
      if type==0:
        slopeBUnSc=hist.slopeBUnSc
        stubPhiBPropUnSc=phiProp(genK,0,slopeBUnSc)
        deltaBUnSc=deltaPhi(stubPhiBUnSc,stubPhiBPropUnSc)

        slopeBSc=slope
        stubPhiBPropSc=phiProp(genK,0,slopeBSc)
        deltaBSc=deltaPhi(stubPhiBSc,stubPhiBPropSc)

        stubPhiBPropScPh=phiProp(genK,0,slope)
        deltaBScPh=deltaPhi(stubPhiBSc,stubPhiBPropScPh)

      if fillType=='res':
        hist.plots.phiPropRatio.Fill(stubPhi,stubPhiProp)
        if type==0:
          hist.plots.phiBPropRatioUnSc.Fill(stubPhiBUnSc,stubPhiBPropUnSc)
          hist.plots.phiBPropRatioSc.Fill(stubPhiBSc,stubPhiBPropSc)

        hist.plots.deltaPhi.Fill(delta)
        hist.plots.deltaPhiK.Fill(genK,delta)

        if type==0:
          hist.plots.deltaPhiBUnSc.Fill(deltaBUnSc)
          hist.plots.deltaPhiBKUnSc.Fill(genK,deltaBUnSc)

          hist.plots.deltaPhiBSc.Fill(deltaBSc)
          hist.plots.deltaPhiBKSc.Fill(genK,deltaBSc)

      elif fillType=='pull':
        aRes=hist.aRes
        bRes=hist.bRes
        pull=pullPhi(genK,delta,aRes,bRes)
        if (aRes!=0 or bRes!=0):
          hist.plots.pull.Fill(pull)
          hist.plots.pullK.Fill(abs(genK),pull)
        if type==0:
          aResBUnSc=hist.aResBUnSc
          bResBUnSc=hist.bResBUnSc
          pullBUnSc=pullPhi(genK,deltaBUnSc,aResBUnSc,bResBUnSc)
          if (aResBUnSc!=0 or bResBUnSc!=0):
            hist.plots.pullBUnSc.Fill(pullBUnSc)
            hist.plots.pullBKUnSc.Fill(abs(genK),pullBUnSc)

          aResBSc=hist.aResBSc
          bResBSc=hist.bResBSc
          pullBSc=pullPhi(genK,deltaBSc,aResBSc,bResBSc)
          if (aResBSc!=0 or bResBSc!=0):
            hist.plots.pullBSc.Fill(pullBSc)
            hist.plots.pullBKSc.Fill(abs(genK),pullBSc)

def runEvents(events,numEvents,hists,fillType):
  counter=-1
  for event in events:
    counter+=1
    if counter%10000==0:
      print('Event',counter)
    if counter==numEvents:
      break

    gen=fetchGEN(event)

    stubsList={}
    for phase,stubsName in phases.iteritems():
      stubsList[phase]=fetchStubs(event,stubsName)

    for g in gen:
      for phase,stubs in stubsList.iteritems():
        runStubs(stubs,phase,hists,g,fillType)

def writeLUT(filename,hists,N=3):
  # Get number of detectors
  numDetect=0
  for key in hists:
    if key[0]>numDetect:
      numDetect=key[0]
  numDetect+=1

  # Get LUTs
  slope={}
  slope_phiB={}
  aRes={}
  bRes={}
  aRes_phiB={}
  bRes_phiB={}
  hasPhiB={}
  for detector in xrange(0,numDetect):
    for i in xrange(0,512):
      slope[detector,i]=0
      slope_phiB[detector,i]=0
      aRes[detector,i]=0
      bRes[detector,i]=0
      aRes_phiB[detector,i]=0
      bRes_phiB[detector,i]=0
      hasPhiB[detector,i]=0

  for hist in hists.values():
    detector=hist.detector
    etaHigh=hist.etaIndices[1]+1
    etaLow=hist.etaIndices[0]
    type=hist.type
    for i in xrange(etaLow,etaHigh):
      slope[detector,i]=hist.slope
      aRes[detector,i]=hist.aRes
      bRes[detector,i]=hist.bRes
      if type==0:
        slope_phiB[detector,i]=hist.slope
        aRes_phiB[detector,i]=hist.aResBSc
        bRes_phiB[detector,i]=hist.bResBSc
        hasPhiB[detector,i]=1

  coeffs={0:[slope,'slope'],1:[slope_phiB,'slope_phiB'],2:[aRes,'resa'],3:[bRes,'resb'],4:[aRes_phiB,'resa_phiB'],5:[bRes_phiB,'resb_phiB'],6:[hasPhiB,'hasPhiB']}
  #coeffs={0:[slope,'slope'],1:[aRes,'resa'],2:[bRes,'resb'],3:[aRes_phiB,'resa_phiB'],4:[bRes_phiB,'resb_phiB'],5:[hasPhiB,'hasPhiB']}

  # Write LUTs to file
  fitParam=open(filename+'.py','w')
  fitParam.write('class bLUT:')
  for detector in xrange(0,numDetect):
    for coeff in xrange(0,7):
      coeffName=coeffs[coeff][1]
      fitParam.write('\n\n\t'+coeffName+'_'+str(detector)+'=[')
      for i in xrange(0,512):
        coeffValue=coeffs[coeff][0][detector,i]
        if i!=511:
          if coeffValue==0:
            fitParam.write('0,')
          else:
            if coeffName=='resa' or coeffName=='resb' or coeffName=='resa_phiB' or coeffName=='resb_phiB':
              fitParam.write('{0:.5e}'.format(N*coeffValue)+',')
            elif coeffName=='hasPhiB':
              fitParam.write(str(coeffValue)+',')
            else:
              fitParam.write('{0:.5e}'.format(coeffValue)+',')
        else:
          if coeffValue==0:
            fitParam.write('0]')
          else:
            if coeffName=='resa' or coeffName=='resb' or coeffName=='resa_phiB' or coeffName=='resb_phiB':
              fitParam.write('{0:.5e}'.format(N*coeffValue)+']')
            elif coeffName=='hasPhiB':
              fitParam.write(str(coeffValue)+']')
            else:
              fitParam.write('{0:.5e}'.format(coeffValue)+']')
  fitParam.close()

def printEvent(events,numEvents,hists):
  counter=-1
  for event in events:
    counter+=1
    if counter%10000==0:
      print('Event',counter)
    if counter==numEvents:
      break

    gen=fetchGEN(event)

    stubsList={}
    for phase,stubsName in phases.iteritems():
      stubsList[phase]=fetchStubs(event,stubsName)

    for g in gen:
      genPhi=int(g.phi()/PHILSB)
      genEta=int(g.eta()/ETALSB)
      genK=int(g.charge()/g.pt()/CURVLSB)
      if abs(genEta)>0:
        genEtaSign=genEta/abs(genEta)
      else:
        genEtaSign=1

      print('Event {COUNTER}'.format(COUNTER=counter))
      print('Gen Muon phi={PHI} k={K} eta={ETA}\n'.format(PHI=genPhi,K=genK,ETA=genEta))

      for hist in hists.values():
        detector=hist.detector
        type=hist.type
        depth=hist.depth
        eta=hist.eta
        etaLow=hist.etaIndices[0]
        etaHigh=hist.etaIndices[1]

        slope=hist.slope
        aRes=hist.aRes
        bRes=hist.bRes
        if type==0:
          aResB=hist.aResBSc
          bResB=hist.bResBSc

        if eta==0:
          wh=0
        elif eta==1 or eta==2:
          wh=1*genEtaSign
        elif eta==3 or eta==4:
          wh=2*genEtaSign

        # Get stubs for histogram
        histStubs={}
        for phase,stubs in stubsList.iteritems():
          histStubs[phase]=[]
          for stub in stubs:
            stubType=stub.type()
            stubDepth=stub.depthRegion()
            stubWheel=stub.etaRegion()

            eta=-1
            for etaInd in xrange(0,5):
               if abs(genEta)>=etaIndices[stubDepth,etaInd][0] and abs(genEta)<=etaIndices[stubDepth,etaInd][1]:
                   eta=etaInd
                   break

            stubPhi=stub.phi()-phiOffset[stubDepth,phase]

            if abs(deltaPhi(genPhi,stubPhi))>math.pi/2./PHILSB or stubType!=type or stubDepth!=depth or stubWheel!=wh or (abs(genEta)<etaLow or abs(genEta)>etaHigh):
              continue

            histStubs[phase].append(stub)

        numStubsList={}
        for phase,stubs in histStubs.iteritems():
          numStubsList[phase]=len(stubs)
        if max(numStubsList.values())>0:
          print('Detector {DETECTOR} etaIndex {ETAINDEX}'.format(DETECTOR=detector,ETAINDEX=eta))
          for phase,stubs in histStubs.iteritems():
            numStubs=len(stubs)
            if numStubs>0:
              print('{NUMSTUBS} {PHASE} stubs:'.format(NUMSTUBS=numStubs,PHASE=phase))
              for i,stub in enumerate(stubs):
                stubType=stub.type()
                stubDepth=stub.depthRegion()

                stubPhi=stub.phi()-phiOffset[stubDepth,phase]
                stubPhiProp=phiProp(genK,genPhi,slope)
                delta=deltaPhi(stubPhi,stubPhiProp)
                sigma=aRes*abs(genK)+bRes
                pull=pullPhi(genK,delta,aRes,bRes)

                print('\tStub {NUM} (type {STUBTYPE}): depth={STUBDEPTH} phi={STUBPHI} phiProp={STUBPHIPROP} delta={DELTA} sigma={SIGMA} pull={PULL}'.format(NUM=i,STUBTYPE=stubType,STUBDEPTH=stubDepth,STUBPHI=stubPhi,STUBPHIPROP=stubPhiProp,DELTA=delta,SIGMA=sigma,PULL=pull))

                if stubType==0:
                  stubPhiB=int(phiBConv[stubDepth,eta,'sc',phase]*stub.phiB())
                  stubPhiBProp=phiProp(genK,0,slope)
                  deltaB=deltaPhi(stubPhiB,stubPhiBProp)
                  sigmaB=aResB*abs(genK)+bResB
                  pullB=pullPhi(genK,deltaB,aResB,bResB)

                  print('\tphiB={STUBPHIB} phiBProp={STUBPHIBPROP} deltaB={DELTAB} sigmaB={SIGMAB} pullB={PULLB}'.format(STUBPHIB=stubPhiB,STUBPHIBPROP=stubPhiBProp,DELTAB=deltaB,SIGMAB=sigmaB,PULLB=pullB))

      pdb.set_trace()

class plots:
  def __init__(self,name,type,depth,eta,phase):
    self.hist2D=None
    self.histMean=None
    self.histRes=None
    self.deltaPhi=ROOT.TH1F(name+'_deltaPhi',name+'_deltaPhi;;Count',100,-200,200)
    self.deltaPhiK=ROOT.TH2F(name+'_deltaPhiK',name+'_deltaPhiK;|k|;;Count',binsPhiResK[type],-4160,4160,binsPhiRes[type],-1500,1500)
    self.pull=ROOT.TH1F(name+'_pull',name+'_pull;;Count',49,-5,5)
    self.pullK=ROOT.TH2F(name+'_pullK',name+'_pullK;|k|;;Count',33,0,4160,50,-5,5)
    self.phiPropRatio=ROOT.TH2F(name+'_phiPropRatio',name+'_phiPropRatio;#phi_{stub};#phi_{prop}',binsPhiResK[type],-4160,4160,binsPhiRes[type],-4160,4160)
    self.phiPropRatioMean=None
    if type==0:
      self.histB2DUnSc=None
      self.histBMeanUnSc=None
      self.histBResUnSc=None
      self.deltaPhiBUnSc=ROOT.TH1F(name+'_deltaPhiB_unSc',name+'_deltaPhiB_unSc;;Count',100,-phiBConvHist[depth,eta,'unSc',phase]*200,phiBConvHist[depth,eta,'unSc',phase]*200)
      self.deltaPhiBKUnSc=ROOT.TH2F(name+'_deltaPhiBK_unSc',name+'_deltaPhiBK_unSc;|k|;;Count',binsPhiBResK,-4160,4160,binsPhiBRes,-phiBConvHist[depth,eta,'unSc',phase]*1500,phiBConvHist[depth,eta,'unSc',phase]*1500)
      self.pullBUnSc=ROOT.TH1F(name+'_pullB_unSc',name+'_pullB_unSc;;Count',49,-5,5)
      self.pullBKUnSc=ROOT.TH2F(name+'_pullBK_unSc',name+'_pullBK_unSc;|k|;;Count',33,0,4160,50,-5,5)
      self.phiBPropRatioUnSc=ROOT.TH2F(name+'_phiBPropRatio_unSc',name+'_phiBPropRatio_unSc;#phi_{stub,b};#phi_{prop,b}',binsPhiBResK,-4160,4160,binsPhiBRes,-4160,-4160)
      self.phiBPropRatioMeanUnSc=None

      self.histB2DSc=None
      self.histBMeanSc=None
      self.histBResSc=None
      self.deltaPhiBSc=ROOT.TH1F(name+'_deltaPhiB_sc',name+'_deltaPhiB_sc;;Count',100,-phiBConvHist[depth,eta,'sc',phase]*200,phiBConvHist[depth,eta,'sc',phase]*200)
      self.deltaPhiBKSc=ROOT.TH2F(name+'_deltaPhiBK_sc',name+'_deltaPhiBK_sc;|k|;;Count',binsPhiBResK,-4160,4160,binsPhiBRes,-phiBConvHist[depth,eta,'sc',phase]*1500,phiBConvHist[depth,eta,'sc',phase]*1500)
      self.pullBSc=ROOT.TH1F(name+'_pullB_sc',name+'_pullB_sc;;Count',49,-5,5)
      self.pullBKSc=ROOT.TH2F(name+'_pullBK_sc',name+'_pullBK_sc;|k|;;Count',33,0,4160,50,-5,5)
      self.phiBPropRatioSc=ROOT.TH2F(name+'_phiBPropRatio_sc',name+'_phiBPropRatio_sc;#phi_{stub,b};#phi_{prop,b}',binsPhiBResK,-4160,4160,binsPhiBRes,-4160,-4160)
      self.phiBPropRatioMeanSc=None

    # Set titles
    self.deltaPhi.GetXaxis().SetTitle('#Delta#phi_{prop}')
    self.deltaPhiK.GetYaxis().SetTitle('#Delta#phi_{prop}')
    self.pull.GetXaxis().SetTitle('P_{#phi}')
    if type==0:
      self.deltaPhiBUnSc.GetXaxis().SetTitle('#Delta#phi_{b,prop}')
      self.deltaPhiBKUnSc.GetYaxis().SetTitle('#Delta#phi_{b,prop}')
      self.pullBUnSc.GetXaxis().SetTitle('P_{#phi_{b}}')

      self.deltaPhiBSc.GetXaxis().SetTitle('#Delta#phi_{b,prop}')
      self.deltaPhiBKSc.GetYaxis().SetTitle('#Delta#phi_{b,prop}')
      self.pullBSc.GetXaxis().SetTitle('P_{#phi_{b}}')

class histPlotter:
  def __init__(self,detector,key):
    self.detector=key[0]
    self.type=detector[0]
    self.eta=detector[1]
    self.depth=detector[2]
    self.etaIndices=detector[3]
    self.phase=detector[4]
    self.name='detector'+str(self.detector)+'_eta'+str(self.eta)+'_'+self.phase
    self.plots=plots(self.name,self.type,self.depth,self.eta,self.phase)
    self.slope=None
    self.aRes=None
    self.bRes=None
    if self.type=='0':
      self.slopeBUnSc=None
      self.aResBUnSc=None
      self.bResBUnSc=None

      self.slopeBSc=None
      self.aResBSc=None
      self.bResBSc=None

  def get2DHist(self,histFile,plotNames):
    # Get 2D histogram
    hist=histFile.Get(plotNames[0])
    hist.SetName(self.name+'_deltaPhi_2D')
    hist.GetXaxis().SetTitle('k')
    hist.GetYaxis().SetTitle('#phi')
    self.plots.hist2D=hist

    if self.type==0:
      histBUnSc=histFile.Get(plotNames[1]+'_unSc')
      histBUnSc.SetName(self.name+'_phiB_2D_unSc')
      histBUnSc.GetXaxis().SetTitle('k')
      histBUnSc.GetYaxis().SetTitle('#phi')
      self.plots.histB2DUnSc=histBUnSc

      histBSc=histFile.Get(plotNames[1]+'_sc')
      histBSc.SetName(self.name+'_phiB_2D_sc')
      histBSc.GetXaxis().SetTitle('k')
      histBSc.GetYaxis().SetTitle('#phi')
      self.plots.histB2DSc=histBSc

  def fit2DHistMean(self,fitFuncMean,fitRange,fitRangeB,numFit=1):
    self.plots.hist2D.FitSlicesY()
    histMean=ROOT.gDirectory.Get(self.plots.hist2D.GetName()+'_1')
    histMean.SetName(self.name+'_mean')

    if self.type==0:
      self.plots.histB2DUnSc.FitSlicesY()
      histBMeanUnSc=ROOT.gDirectory.Get(self.plots.histB2DUnSc.GetName()+'_1')
      histBMeanUnSc.SetName(self.name+'_Bmean_unSc')

      self.plots.histB2DSc.FitSlicesY()
      histBMeanSc=ROOT.gDirectory.Get(self.plots.histB2DSc.GetName()+'_1')
      histBMeanSc.SetName(self.name+'_Bmean_sc')

    # Set up fitting functions
    fitMean=ROOT.TF1(histMean.GetName(),fitFuncMean,fitRange[0],fitRange[1])

    if self.type==0:
      fitBMeanUnSc=ROOT.TF1(histBMeanUnSc.GetName(),fitFuncMean,fitRangeB[0],fitRangeB[1])
      fitBMeanSc=ROOT.TF1(histBMeanSc.GetName(),fitFuncMean,fitRangeB[0],fitRangeB[1])

    # Draw mean fit function
    canvMean=ROOT.TCanvas(histMean.GetName()+'_canv')
    canvMean.cd()
    canvMean.SetGrid()
    histMean.Draw()
    histMean.GetXaxis().SetRangeUser(-2000,2000)
    histMean.GetXaxis().SetTitle('k')
    histMean.GetYaxis().SetRangeUser(-5000,5000)
    histMean.GetYaxis().SetTitle('#phi')
    gStyle.SetOptFit()

    if self.type==0:
      canvBMeanUnSc=ROOT.TCanvas(histBMeanUnSc.GetName()+'_canv')
      canvBMeanUnSc.cd()
      canvBMeanUnSc.SetGrid()
      histBMeanUnSc.Draw()
      histBMeanUnSc.GetXaxis().SetRangeUser(-2000,2000)
      histBMeanUnSc.GetXaxis().SetTitle('k')
      histBMeanUnSc.GetYaxis().SetRangeUser(-phiBConvHist[self.depth,self.eta,'unSc',self.phase]*5000,phiBConvHist[self.depth,self.eta,'unSc',self.phase]*5000)
      histBMeanUnSc.GetYaxis().SetTitle('#phi_{b}')
      gStyle.SetOptFit()

      canvBMeanSc=ROOT.TCanvas(histBMeanSc.GetName()+'_canv')
      canvBMeanSc.cd()
      canvBMeanSc.SetGrid()
      histBMeanSc.Draw()
      histBMeanSc.GetXaxis().SetRangeUser(-2000,2000)
      histBMeanSc.GetXaxis().SetTitle('k')
      histBMeanSc.GetYaxis().SetRangeUser(-phiBConvHist[self.depth,self.eta,'sc','P2']*5000,phiBConvHist[self.depth,self.eta,'sc','P2']*5000)
      histBMeanSc.GetYaxis().SetTitle('#phi_{b}')
      gStyle.SetOptFit()

    for num in xrange(0,numFit):
      histMean.Fit(fitMean,'R')

      if self.type==0:
        histBMeanUnSc.Fit(fitBMeanUnSc,'R')
        histBMeanSc.Fit(fitBMeanSc,'R')

    self.plots.histMean=copy.deepcopy(histMean)

    if self.type==0:
      self.plots.histBMeanUnSc=copy.deepcopy(histBMeanUnSc)
      self.plots.histBMeanSc=copy.deepcopy(histBMeanSc)

    # Get fit coefficients
    self.slope=fitMean.GetParameter(0)
    if self.type==0:
      self.slopeBUnSc=fitBMeanUnSc.GetParameter(0)
      self.slopeBSc=fitBMeanSc.GetParameter(0)

  def fit2DHistRes(self,fitFuncRes,fitRange,numFit=1):
    self.plots.deltaPhiK.FitSlicesY()
    histRes=ROOT.gDirectory.Get(self.plots.deltaPhiK.GetName()+'_2')
    histRes.SetName(self.name+'_res')
    if self.type==0:
      self.plots.deltaPhiBKUnSc.FitSlicesY()
      histBResUnSc=ROOT.gDirectory.Get(self.plots.deltaPhiBKUnSc.GetName()+'_2')
      histBResUnSc.SetName(self.name+'_Bres_unSc')

      self.plots.deltaPhiBKSc.FitSlicesY()
      histBResSc=ROOT.gDirectory.Get(self.plots.deltaPhiBKSc.GetName()+'_2')
      histBResSc.SetName(self.name+'_Bres_sc')

    # Set up fitting functions
    fitRes=ROOT.TF1(histRes.GetName(),fitFuncRes,fitRange[0],fitRange[1])
    if self.type==0:
      fitBResUnSc=ROOT.TF1(histBResUnSc.GetName(),fitFuncRes,fitRange[0],fitRange[1])
      fitBResSc=ROOT.TF1(histBResSc.GetName(),fitFuncRes,fitRange[0],fitRange[1])

    # Set up fitting parameter limits
    #if self.type==0:
      #fitBResSc.SetParLimts(0,1e-10,1e10)
      #fitBResSc.SetParLimts(1,1e-10,1e10)

    # Draw res fit function
    canvRes=ROOT.TCanvas(histRes.GetName()+'_canv')
    canvRes.cd()
    canvRes.SetGrid()
    histRes.Draw()
    histRes.GetXaxis().SetRangeUser(-2000,2000)
    histRes.GetXaxis().SetTitle('k')
    histRes.GetYaxis().SetRangeUser(-100,1000)
    histRes.GetYaxis().SetTitle('#phi')
    gStyle.SetOptFit()
    if self.type==0:
      canvBResUnSc=ROOT.TCanvas(histBResUnSc.GetName()+'_canv')
      canvBResUnSc.cd()
      canvBResUnSc.SetGrid()
      histBResUnSc.Draw()
      histBResUnSc.GetXaxis().SetRangeUser(-2000,2000)
      histBResUnSc.GetXaxis().SetTitle('k')
      histBResUnSc.GetYaxis().SetRangeUser(-phiBConvHist[self.depth,self.eta,'unSc',self.phase]*100,phiBConvHist[self.depth,self.eta,'unSc',self.phase]*1000)
      histBResUnSc.GetYaxis().SetTitle('#phi_{b}')
      gStyle.SetOptFit()

      canvBResSc=ROOT.TCanvas(histBResSc.GetName()+'_canv')
      canvBResSc.cd()
      canvBResSc.SetGrid()
      histBResSc.Draw()
      histBResSc.GetXaxis().SetRangeUser(-2000,2000)
      histBResSc.GetXaxis().SetTitle('k')
      histBResSc.GetYaxis().SetRangeUser(-phiBConvHist[self.depth,self.eta,'sc',self.phase]*100,phiBConv[self.depth,self.eta,'sc',self.phase]*1000)
      histBResSc.GetYaxis().SetTitle('#phi_{b}')
      gStyle.SetOptFit()

    for num in xrange(0,numFit):
      histRes.Fit(fitRes,'R')
      if self.type==0:
        histBResUnSc.Fit(fitBResUnSc,'R')
        histBResSc.Fit(fitBResSc,'R')

    self.plots.histRes=copy.deepcopy(histRes)
    if self.type==0:
      self.plots.histBResUnSc=copy.deepcopy(histBResUnSc)
      self.plots.histBResSc=copy.deepcopy(histBResSc)

    # Get fit coefficients
    self.aRes=fitRes.GetParameter(0)
    self.bRes=fitRes.GetParameter(1)
    if self.type==0:
      self.aResBUnSc=fitBResUnSc.GetParameter(0)
      self.bResBUnSc=fitBResUnSc.GetParameter(1)

      self.aResBSc=fitBResSc.GetParameter(0)
      self.bResBSc=fitBResSc.GetParameter(1)

  def fitRatioSlope(self,fitFuncRatio,fitRange):
    self.plots.phiPropRatio.FitSlicesY()
    histRatio=ROOT.gDirectory.Get(self.plots.phiPropRatio.GetName()+'_1')
    histRatio.SetName(self.name+'_RatioMean')
    if self.type==0:
      self.plots.phiBPropRatioUnSc.FitSlicesY()
      histBRatioUnSc=ROOT.gDirectory.Get(self.plots.phiBPropRatioUnSc.GetName()+'_1')
      histBRatioUnSc.SetName(self.name+'_BRatioMean_unSc')

      self.plots.phiBPropRatioSc.FitSlicesY()
      histBRatioSc=ROOT.gDirectory.Get(self.plots.phiBPropRatioSc.GetName()+'_1')
      histBRatioSc.SetName(self.name+'_BRatioMean_sc')

    # Set up fitting functions
    fitRatio=ROOT.TF1(histRatio.GetName(),fitFuncRatio,fitRange[0],fitRange[1])
    if self.type==0:
      fitBRatioUnSc=ROOT.TF1(histBRatioUnSc.GetName(),fitFuncRatio,fitRange[0],fitRange[1])
      fitBRatioSc=ROOT.TF1(histBRatioSc.GetName(),fitFuncRatio,fitRange[0],fitRange[1])

    # Draw ratio fit function
    canvRatio=ROOT.TCanvas(histRatio.GetName()+'_canv')
    canvRatio.cd()
    canvRatio.SetGrid()
    histRatio.Draw()
    histRatio.GetXaxis().SetRangeUser(-1000,1000)
    histRatio.GetXaxis().SetTitle('#phi_{stub}')
    histRatio.GetYaxis().SetRangeUser(-1000,1000)
    histRatio.GetYaxis().SetTitle('#phi_{prop}')
    gStyle.SetOptFit()
    if self.type==0:
      canvBRatioUnSc=ROOT.TCanvas(histBRatioUnSc.GetName()+'_canv')
      canvBRatioUnSc.cd()
      canvBRatioUnSc.SetGrid()
      histBRatioUnSc.Draw()
      histBRatioUnSc.GetXaxis().SetRangeUser(-1000,1000)
      histBRatioUnSc.GetXaxis().SetTitle('#phi_{stub,b}')
      histBRatioUnSc.GetYaxis().SetRangeUser(-1000,1000)
      histBRatioUnSc.GetYaxis().SetTitle('#phi_{prop,b}')
      gStyle.SetOptFit()

      canvBRatioSc=ROOT.TCanvas(histBRatioSc.GetName()+'_canv')
      canvBRatioSc.cd()
      canvBRatioSc.SetGrid()
      histBRatioSc.Draw()
      histBRatioSc.GetXaxis().SetRangeUser(-1000,1000)
      histBRatioSc.GetXaxis().SetTitle('#phi_{stub,b}')
      histBRatioSc.GetYaxis().SetRangeUser(-1000,1000)
      histBRatioSc.GetYaxis().SetTitle('#phi_{prop,b}')
      gStyle.SetOptFit()

    histRatio.Fit(fitRatio,'R')
    if self.type==0:
      histBRatioUnSc.Fit(fitBRatioUnSc,'R')
      histBRatioSc.Fit(fitBRatioSc,'R')

    self.plots.PhiPropRatioMean=copy.deepcopy(histRatio)
    if self.type==0:
      self.plots.PhiBPropRatioMeanUnSc=copy.deepcopy(histBRatioUnSc)
      self.plots.PhiBPropRatioMeanSc=copy.deepcopy(histBRatioSc)

detectors={}
for eta in xrange(0,5):
  for phase in phases:
    detectors[0,eta,phase]=[1,eta,1,etaIndices[1,eta],phase]
    detectors[1,eta,phase]=[0,eta,1,etaIndices[1,eta],phase]
    detectors[3,eta,phase]=[1,eta,1,etaIndices[1,eta],phase]
    detectors[4,eta,phase]=[1,eta,2,etaIndices[2,eta],phase]
    detectors[5,eta,phase]=[0,eta,2,etaIndices[2,eta],phase]
    detectors[6,eta,phase]=[1,eta,3,etaIndices[3,eta],phase]
    detectors[7,eta,phase]=[1,eta,2,etaIndices[2,eta],phase]
    detectors[8,eta,phase]=[0,eta,3,etaIndices[3,eta],phase]
    detectors[9,eta,phase]=[1,eta,4,etaIndices[4,eta],phase]
    detectors[10,eta,phase]=[0,eta,4,etaIndices[4,eta],phase]

# Set fit ranges
meanFitRange={}
meanFitBRange={}
resFitRange={}
meanDefault=750
meanBDefault=500
resDefault=1000
for key in detectors:
  meanFitRange[key]=[-meanDefault,meanDefault]
  meanFitBRange[key]=[-meanBDefault,meanBDefault]
  resFitRange[key]=[-resDefault,resDefault]
meanFitRange[8,4,'P1']=[-500,750]
meanFitBRange[1,2,'P2']=[-150,500]
meanFitBRange[1,4,'P2']=[-500,100]
meanFitBRange[5,2,'P2']=[-55,750]
meanFitBRange[5,4,'P2']=[-350,500]
meanFitBRange[8,4,'P2']=[-750,250]
meanFitBRange[10,0,'P2']=[-500,50]
meanFitBRange[10,2,'P2']=[-610,55]
meanFitBRange[10,3,'P2']=[-380,-55]
meanFitBRange[10,4,'P2']=[-500,55]
resFitRange[10,3,'P1']=[-450,450]
resFitRange[10,4,'P1']=[-200,200]
resFitRange[1,0,'P2']=[-1000,500]

# Get histograms
histFile=ROOT.TFile("Rootfiles/pythonOut/mu0New.root","OPEN")
hists={}
for key,detector in detectors.items():
  type=detector[0]
  eta=detector[1]
  depth=detector[2]
  phase=detector[4]
  plotNamesP1=[]
  plotNamesP2=[]
  if type==0:
    plotNamesP1=['propPhi_P1_type_'+str(type)+'_depth_'+str(depth)+'_eta_'+str(eta),'propPhiB_P1_type_'+str(type)+'_depth_'+str(depth)+'_eta_'+str(eta)]
    plotNamesP2=['propPhi_P2_type_'+str(type)+'_depth_'+str(depth)+'_eta_'+str(eta),'propPhiB_P2_type_'+str(type)+'_depth_'+str(depth)+'_eta_'+str(eta)]
  elif type==1:
    plotNamesP1=['propPhi_P1_type_'+str(type)+'_depth_'+str(depth)+'_eta_'+str(eta)]
    plotNamesP2=['propPhi_P2_type_'+str(type)+'_depth_'+str(depth)+'_eta_'+str(eta)]

  hists[key]=histPlotter(detector,key)
  if phase=='P1':
    hists[key].get2DHist(histFile,plotNamesP1)
  elif phase=='P2':
    hists[key].get2DHist(histFile,plotNamesP2)
  hists[key].fit2DHistMean('[0]*x',meanFitRange[key],meanFitBRange[key],1)

# Fetch events
numEvents=-1
events=Events([tag+'.root'])

# Get histogram resolution plots
runEvents(events,numEvents,hists,'res')
for key,hist in hists.items():
  hist.fit2DHistRes('[0]*abs(x)+[1]',resFitRange[key],1)
  hist.fitRatioSlope('[0]*x',[-500,500])

#events=Events([tag+'.root'])
#printEvent(events,numEvents,hists)

# Get pull distributions
events=Events([tag+'.root'])
runEvents(events,numEvents,hists,'pull')
for hist in hists.values():
  fitPull(hist.plots.pull)
  if hist.type==0:
    fitPull(hist.plots.pullBUnSc)
    fitPull(hist.plots.pullBSc)

# Write plots to file
f=ROOT.TFile("Rootfiles/pythonOut/TPSPlotsFermi.root","RECREATE")

for hist in hists.values():
  dirName='detector'+str(hist.detector)+'/eta'+str(hist.eta)+'/'+hist.phase
  f.mkdir(dirName)
  f.cd(dirName)
  for plot in hist.plots.__dict__.values():
    if hasattr(plot,'Write')==True:
      plot.Write()

f.Close()

# Write values to LUT
#writeLUT('L1Phase2TPSLUTsBarrel',hists,N=3)
#writeLUT('L1TPSLUTsBarrel',hists,N=3)
