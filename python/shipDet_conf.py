#!/usr/bin/env python
# -*- coding: latin-1 -*-
import ROOT,os
import shipunit as u
detectorList = []

def posHcal(z,hfile): 
 HcalZSize = 0
 sz = hfile+"z"+str(z)+".geo"
 floc = os.environ["FAIRSHIP"]+"/geometry"
 f_hcal  = floc+"/"+hfile
 f_hcalz = floc+"/"+sz
 f = open(f_hcal) 
 rewrite = True
 if sz in os.listdir(floc):
  test = os.popen("diff "+ f_hcal+ " "+ f_hcalz).read()
  if str.count(test,'---')==1 and not test.find('Position')<0: rewrite = False # only different is z position
 if rewrite: fn = open(f_hcalz,'w')
 for l in f.readlines():
   if rewrite:
    if not l.find("ZPos")<0:
      l ="ZPos="+str(z)+ "	#Position of Hcal  center	[cm]\n"
    fn.write(l)
   if not l.find("HcalZSize")<0:
     HcalZSize = float(l[len('HcalZSize')+1:].split('#')[0]) 
 f.close()
 if rewrite: fn.close()  
 hcal = ROOT.hcal("Hcal", ROOT.kTRUE, sz)
 return hcal,HcalZSize
def posEcal(z,efile):
 EcalZSize = 0
 sz = efile+"z"+str(z)+".geo"
 floc = os.environ["FAIRSHIP"]+"/geometry"
 f_ecal  = floc+"/"+efile
 f_ecalz = floc+"/"+sz
 f = open(f_ecal) 
 rewrite = True
 if sz in os.listdir(floc):
  test = os.popen("diff "+ f_ecal+ " "+ f_ecalz).read()
  if str.count(test,'---')==1 and not test.find('Position')<0: rewrite = False # only different is z position
 if rewrite: fn = open(f_ecalz,'w')
 for l in f.readlines():
   if rewrite:
    if not l.find("ZPos")<0:
      l ="ZPos="+str(z)+ "	#Position of Ecal start		[cm]\n"
    fn.write(l)
   if not l.find("EcalZSize")<0:
     EcalZSize = float(l[len('EcalZSize')+1:].split('#')[0]) 
 f.close()
 if rewrite: fn.close()  
 ecal = ROOT.ecal("Ecal", ROOT.kTRUE, sz)
 return ecal,EcalZSize

def configure(run,ship_geo):
# ---- for backward compatibility ----
 if not hasattr(ship_geo,"tankDesign"): ship_geo.tankDesign = 4
 if not hasattr(ship_geo.hcal,"File"): ship_geo.hcal.File = "hcal.geo"


# -----Create media-------------------------------------------------
 run.SetMaterials("media.geo")  # Materials
# ------------------------------------------------------------------------
  
# -----Create geometry----------------------------------------------
 cave= ROOT.ShipCave("CAVE")
 cave.SetGeometryFileName("cave.geo")
 detectorList.append(cave)

 if ship_geo.muShieldDesign==6: # magnetized hadron absorber
  TargetStation = ROOT.ShipTargetStation("TargetStation",ship_geo.target.length,0,
                                                        ship_geo.target.z,0.,ship_geo.targetOpt,ship_geo.target.sl)
 else:
  TargetStation = ROOT.ShipTargetStation("TargetStation",ship_geo.target.length,ship_geo.hadronAbsorber.length,
                                                        ship_geo.target.z,ship_geo.hadronAbsorber.z,ship_geo.targetOpt,ship_geo.target.sl)
   
 if ship_geo.targetOpt>10:
  TargetStation.SetLayerPosMat(ship_geo.target.xy,ship_geo.target.L1,ship_geo.target.M1,ship_geo.target.L2,ship_geo.target.M2,\
  ship_geo.target.L3,ship_geo.target.M3,ship_geo.target.L4,ship_geo.target.M4,ship_geo.target.L5,ship_geo.target.M5,\
  ship_geo.target.L6,ship_geo.target.M6,ship_geo.target.L7,ship_geo.target.M7,ship_geo.target.L8,ship_geo.target.M8,\
  ship_geo.target.L9,ship_geo.target.M9,ship_geo.target.L10,ship_geo.target.M10,ship_geo.target.L11,ship_geo.target.M11,\
  ship_geo.target.L12,ship_geo.target.M12,ship_geo.target.L13,ship_geo.target.M13,ship_geo.target.L14,ship_geo.target.M14,\
  ship_geo.target.L15,ship_geo.target.M15,ship_geo.target.L16,ship_geo.target.M16,ship_geo.target.L17,ship_geo.target.M17)
 detectorList.append(TargetStation)

 if ship_geo.muShieldDesign==1:
  MuonShield = ROOT.ShipMuonShield("MuonShield",ship_geo.muShieldDesign,"ShipMuonShield",ship_geo.muShield.z,ship_geo.muShield.dZ0,ship_geo.muShield.length,\
                                   ship_geo.muShield.LE) 
 elif ship_geo.muShieldDesign==2:
  MuonShield = ROOT.ShipMuonShield("MuonShield",ship_geo.muShieldDesign,"ShipMuonShield",ship_geo.muShield.z,ship_geo.muShield.dZ0,ship_geo.muShield.dZ1,\
               ship_geo.muShield.dZ2,ship_geo.muShield.dZ3,ship_geo.muShield.dZ4,ship_geo.muShield.dZ5,ship_geo.muShield.dZ6,ship_geo.muShield.LE) 
 elif ship_geo.muShieldDesign==3 or ship_geo.muShieldDesign==4 or ship_geo.muShieldDesign==5 or ship_geo.muShieldDesign==6 :
  MuonShield = ROOT.ShipMuonShield("MuonShield",ship_geo.muShieldDesign,"ShipMuonShield",ship_geo.muShield.z,ship_geo.muShield.dZ0,ship_geo.muShield.dZ1,\
               ship_geo.muShield.dZ2,ship_geo.muShield.dZ3,ship_geo.muShield.dZ4,ship_geo.muShield.dZ5,ship_geo.muShield.dZ6,\
               ship_geo.muShield.dZ7,ship_geo.muShield.dZ8,ship_geo.muShield.dXgap,ship_geo.muShield.LE,ship_geo.Yheight*4./10.) 

 detectorList.append(MuonShield)


 magnet_design = 2
 if ship_geo.tankDesign == 5: magnet_design = 3
 if ship_geo.strawDesign > 1 : magnet = ROOT.ShipMagnet("Magnet","SHiP Magnet",ship_geo.Bfield.z, magnet_design, ship_geo.Bfield.y)
 else: magnet = ROOT.ShipMagnet("Magnet","SHiP Magnet",ship_geo.Bfield.z)
 detectorList.append(magnet)
  
 Veto = ROOT.veto("Veto", ROOT.kTRUE)   # vacuum tank, liquid scintillator, simplistic tracking stations
 Veto.SetZpositions(ship_geo.vetoStation.z, ship_geo.TrackStation1.z, ship_geo.TrackStation2.z, \
                    ship_geo.TrackStation3.z, ship_geo.TrackStation4.z,ship_geo.tankDesign)
 Veto.SetTubZpositions(ship_geo.Chamber1.z,ship_geo.Chamber2.z,ship_geo.Chamber3.z,ship_geo.Chamber4.z,ship_geo.Chamber5.z,ship_geo.Chamber6.z);
 Veto.SetTublengths(ship_geo.chambers.Tub1length,ship_geo.chambers.Tub2length,ship_geo.chambers.Tub3length, \
                    ship_geo.chambers.Tub4length,ship_geo.chambers.Tub5length,ship_geo.chambers.Tub6length);
 Veto.SetB(ship_geo.Yheight/2.)
 if ship_geo.tankDesign == 5: 
    dz =  ship_geo.zFocus+ship_geo.target.z0    
    x1 = ship_geo.xMax/(ship_geo.Chamber1.z -ship_geo.chambers.Tub1length-dz)*(ship_geo.TrackStation4.z-dz)
    Veto.SetXstart(x1,dz)

 detectorList.append(Veto)

 if ship_geo.muShieldDesign not in [2,3,4]:
  taumagneticspectrometer = ROOT.MagneticSpectrometer("MagneticSpectrometer", ship_geo.tauMS.zMSC, ship_geo.tauMS.zSize, ship_geo.tauMS.FeSlab, \
  ship_geo.tauMS.RpcW,ship_geo.tauMS.ArmW, ship_geo.tauMS.GapV, ship_geo.tauMS.MGap, ship_geo.tauMS.Mfield, ship_geo.tauMS.RetYokeH, ROOT.kTRUE)
  taumagneticspectrometer.SetCoilParameters(ship_geo.tauMS.CoilH, ship_geo.tauMS.CoilW, ship_geo.tauMS.N, ship_geo.tauMS.CoilG);
  detectorList.append(taumagneticspectrometer)

  tauHpt = ROOT.Hpt("HighPrecisionTrackers",ship_geo.tauHPT.DX, ship_geo.tauHPT.DY, ship_geo.tauHPT.DZ, ROOT.kTRUE)
  tauHpt.SetZsize(ship_geo.tauMS.zSize)
  detectorList.append(tauHpt)

  NuTauTarget = ROOT.Target("NuTauTarget",ship_geo.NuTauTarget.zC, ship_geo.NuTauTarget.GapTS, ship_geo.NuTauTarget.Ydist,ROOT.kTRUE)
 
  NuTauTarget.SetDetectorDesign(ship_geo.NuTauTarget.nuTargetDesign)
  NuTauTarget.SetGoliathSizes(ship_geo.NuTauTarget.H, ship_geo.NuTauTarget.TS, ship_geo.NuTauTarget.LS, ship_geo.NuTauTarget.BasisH);
  NuTauTarget.SetCoilParameters(ship_geo.NuTauTarget.CoilR, ship_geo.NuTauTarget.UpCoilH, ship_geo.NuTauTarget.LowCoilH, ship_geo.NuTauTarget.CoilD);
 
  NuTauTarget.SetDetectorDimension(ship_geo.NuTauTarget.xdim, ship_geo.NuTauTarget.ydim, ship_geo.NuTauTarget.zdim);
  NuTauTarget.SetEmulsionParam(ship_geo.NuTauTarget.EmTh, ship_geo.NuTauTarget.EmX, ship_geo.NuTauTarget.EmY, ship_geo.NuTauTarget.PBTh,ship_geo.NuTauTarget.EPlW, ship_geo.NuTauTarget.LeadTh, ship_geo.NuTauTarget.AllPW);
 
  NuTauTarget.SetBrickParam(ship_geo.NuTauTarget.BrX, ship_geo.NuTauTarget.BrY, ship_geo.NuTauTarget.BrZ, ship_geo.NuTauTarget.BrPackX, ship_geo.NuTauTarget.BrPackY, ship_geo.NuTauTarget.BrPackZ);
  NuTauTarget.SetCESParam(ship_geo.NuTauTarget.RohG, ship_geo.NuTauTarget.LayerCESW, ship_geo.NuTauTarget.CESW, ship_geo.NuTauTarget.CESPack);
  NuTauTarget.SetCellParam(ship_geo.NuTauTarget.CellW);
  
  NuTauTT = ROOT.TargetTracker("TargetTrackers",ROOT.kTRUE)
  NuTauTT.SetTargetTrackerParam(ship_geo.NuTauTT.TTX, ship_geo.NuTauTT.TTY, ship_geo.NuTauTT.TTZ)
  NuTauTT.SetBrickParam(ship_geo.NuTauTarget.CellW);
  NuTauTT.SetTotZDimension(ship_geo.NuTauTarget.zdim);

  #method of nutau target that must be called after TT parameter definition
  NuTauTarget.SetTTzdimension(ship_geo.NuTauTT.TTZ)
 
  detectorList.append(NuTauTarget)
  detectorList.append(NuTauTT)


 if ship_geo.strawDesign > 1 :
  Strawtubes = ROOT.strawtubes("Strawtubes", ROOT.kTRUE)    
  Strawtubes.SetZpositions(ship_geo.vetoStation.z, ship_geo.TrackStation1.z, ship_geo.TrackStation2.z, ship_geo.TrackStation3.z, ship_geo.TrackStation4.z)
  Strawtubes.SetDeltazView(ship_geo.strawtubes.DeltazView)
  Strawtubes.SetInnerStrawDiameter(ship_geo.strawtubes.InnerStrawDiameter)
  Strawtubes.SetOuterStrawDiameter(ship_geo.strawtubes.OuterStrawDiameter)
  Strawtubes.SetStrawPitch(ship_geo.strawtubes.StrawPitch)
  Strawtubes.SetDeltazLayer(ship_geo.strawtubes.DeltazLayer)
  Strawtubes.SetDeltazPlane(ship_geo.strawtubes.DeltazPlane)
  Strawtubes.SetStrawsPerLayer(ship_geo.strawtubes.StrawsPerLayer)
  Strawtubes.SetStereoAngle(ship_geo.strawtubes.ViewAngle)
  Strawtubes.SetWireThickness(ship_geo.strawtubes.WireThickness)
  Strawtubes.SetVacBox_x(ship_geo.strawtubes.VacBox_x)
  Strawtubes.SetVacBox_y(ship_geo.strawtubes.VacBox_y)
  Strawtubes.SetStrawLength(ship_geo.strawtubes.StrawLength)
  if hasattr(ship_geo.strawtubes,"StrawLengthVeto"):
   Strawtubes.SetStrawLengthVeto(ship_geo.strawtubes.StrawLengthVeto) 
   Strawtubes.SetStrawLength12(ship_geo.strawtubes.StrawLength12) 
  else:
   Strawtubes.SetStrawLengthVeto(ship_geo.strawtubes.StrawLength) 
   Strawtubes.SetStrawLength12(ship_geo.strawtubes.StrawLength) 
   
  detectorList.append(Strawtubes) 

 if ship_geo.preshowerOption > 0:
  Preshower = ROOT.preshower("Preshower", ROOT.kTRUE)
  Preshower.SetZStationPosition2(ship_geo.PreshowerStation0.z,ship_geo.PreshowerStation1.z)
  Preshower.SetZFilterPosition2(ship_geo.PreshowerFilter0.z,ship_geo.PreshowerFilter1.z)
  Preshower.SetXMax(ship_geo.Preshower.XMax)
  Preshower.SetYMax(ship_geo.Preshower.YMax)
  Preshower.SetActiveThickness(ship_geo.Preshower.ActiveThickness)
  Preshower.SetFilterThickness2(ship_geo.Preshower.FilterThickness0,ship_geo.Preshower.FilterThickness1)
  detectorList.append(Preshower)

 ecal,EcalZSize = posEcal(ship_geo.ecal.z,ship_geo.ecal.File)
 detectorList.append(ecal)

 if not ship_geo.HcalOption < 0:
  hcal,HcalZSize = posHcal(ship_geo.hcal.z,ship_geo.hcal.File)
  if abs(ship_geo.hcal.hcalSpace -  HcalZSize) > 10*u.cm:
    print 'mismatch between hcalsize in geo file and python configuration'
    print ship_geo.hcal.hcalSpace -  HcalZSize, ship_geo.hcal.hcalSpace , HcalZSize
  detectorList.append(hcal)
 Muon = ROOT.muon("Muon", ROOT.kTRUE)
 Muon.SetZStationPositions(ship_geo.MuonStation0.z, ship_geo.MuonStation1.z,ship_geo.MuonStation2.z,ship_geo.MuonStation3.z)
 Muon.SetZFilterPositions(ship_geo.MuonFilter0.z, ship_geo.MuonFilter1.z,ship_geo.MuonFilter2.z)
 Muon.SetXMax(ship_geo.Muon.XMax)
 Muon.SetYMax(ship_geo.Muon.YMax)
 Muon.SetActiveThickness(ship_geo.Muon.ActiveThickness)
 Muon.SetFilterThickness(ship_geo.Muon.FilterThickness)
 detectorList.append(Muon)

#-----   Magnetic field   -------------------------------------------
 if ship_geo.strawDesign == 4: fMagField = ROOT.ShipBellField("wilfried", ship_geo.Bfield.max ,ship_geo.Bfield.z,2,ship_geo.Yheight/2.*u.m )  
 else :                        fMagField = ROOT.ShipBellField("wilfried", ship_geo.Bfield.max ,ship_geo.Bfield.z,1,ship_geo.Yheight/2.*u.m )  
 if ship_geo.muShieldDesign==6: fMagField.IncludeTarget(ship_geo.target.xy, ship_geo.target.z0, ship_geo.target.length)
 run.SetField(fMagField)
#
 exclusionList = []
 #exclusionList = ["Muon","Ecal","Hcal","Strawtubes","TargetTrackers","NuTauTarget","HighPrecisionTrackers",\
 #                 "Veto","Magnet","MuonShield","TargetStation","MagneticSpectrometer"]
 for x in detectorList:
   if x.GetName() in exclusionList: continue
   run.AddModule(x)
# return list of detector elements
 detElements = {}
 for x in run.GetListOfModules(): detElements[x.GetName()]=x
 return detElements
