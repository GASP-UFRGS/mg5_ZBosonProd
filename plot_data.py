from __future__ import division
from subprocess import call
from math import *
from ROOT import *

#####################################################################
# GGS (CERN-CMS/UFRGS) ---
# the muons are collected considering the ID codes in the event
# sample produced with SuperCHICv2 in LHE format.
#####################################################################

#####################################################################
# USER INPUT:

# CROSS SECTION(S) (pb):
#xsec    = [ 1.7587434e-04 , 8.2134120e+03 , 0.74053598E+09 , 1.7856140e+01 , 2.2379938e-01 ]; #FIXME
#xsec    = [5728, 1.251e+09 , 17.86 , 0.2238]; #FIXME
xsec    = [27.09,6805,36.93]; #FIXME
# PDF "_"+LABEL FOR OUTPUT FILES:
JOB     = "histos";
#PDF     = ['ppazbb' , 'ppbb' , 'pphbb' , 'ppzz' ]; #FIXME
PDF     = ['ppee','ppee_NLO_QCD','ppzee']; #FIXME
scale   = False;
scale_yield = False;
cuts    = False;
setLog  = False;
filled  = False;
stacked = False;
data    = False;

# KINEMATICAL CUTS: #FIXME
INVMCUTUPPER = 150.0; # (NO CUT 9999.0 )
INVMCUTLOWER = 0.0; # (NO CUT 0.0)

PTPAIRCUTUPPER = 9999.0; # (NO CUT 0.0 )
PTPAIRCUTLOWER = 0.0; # (NO CUT 0.0)

ETAPAIRCUT = 999.0; # (NO CUT 100.)
INNER = False; # (TRUE: -x < y < +x ; FALSE: y < -x AND y > +x)

PTCUTUPPER = 9999.0; # (NO CUT 9999.0 )
PTCUTLOWER = 0.0; # (NO CUT 0.0)

LUMINOSITY = 10E35/10E24#barn;
# INPUT FILES:
#FILES   = [
#"/home/public/aahbb.lhe",
#"/home/public/ppazbb.lhe",
#"/home/public/ppbb.lhe",
#"/home/public/pphbb.lhe",
#"/home/public/ppzz.lhe"
#]; #FIXME

FILES = [
"/home/deros/plotsZ/ppee.lhe",
"/home/deros/plotsZ/ppee_NLO_QCD.lhe",
"/home/deros/plotsZ/ppzee.lhe"
];

# EVENT SAMPLE INPUT:
Nevt     = 100000; #FIXED
EVTINPUT = str(int(Nevt/1000))+"k";

#####################################################################

# LABELS:
STRING	= "";
for m in range(len(PDF)):
	if (PDF[m]==PDF[-1]):
		STRING+=PDF[m]+"_";
	else:
		STRING+=PDF[m]+"-";

LABEL = "FULL_inner.final.madgraph";
if cuts: LABEL+=".cuts";
if scale: LABEL+=".scaled";
if scale_yield: LABEL+=".scale_yield";
if setLog: LABEL+=".log";
if filled: LABEL+=".filled";
if stacked: LABEL+=".stacked";
if data: LABEL+=".data";

# IMAGE FORMATS TO BE CREATED:
FILE_TYPES = [LABEL+".png"];
print("Os arquivos gravados em %s" % (FILE_TYPES[0]));
# SAVING HISTOS INTO ROOT FILE:
FILEROOT = TFile("histos"+LABEL+".root","RECREATE");

# CREATE INDIVIDUAL DIRS FOR IMAGE TYPES:
for l in range(len(FILE_TYPES)):
	call(["mkdir","-p",FILE_TYPES[l]]);

#####################################################################

# ARRAYS FOR EACH TYPE OF DISTRIBUTIONS:
#
# 1D:
invm_decay	= [];
pt_decay	= [];
ptsum_decay	= [];
eta_decay	= [];
phi_decay	= [];
E_decay		= [];
dpt_decay       = [];
acop            = [];
acop_zoom       = [];
dataonly        = [];
dphi            = [];
dphi_zoom       = [];

# SORTING THE DISTRIBUTIONS WITHIN THE SETS:
# THE ARRAYS STORE THE LABELS FOR AXIS AND UNITS:
histoslog        = [invm_decay,pt_decay,ptsum_decay,eta_decay,phi_decay,E_decay,dpt_decay,acop,acop_zoom,dphi,dphi_zoom];
histoslog_label  = ["invm_decay","pt_decay","ptsum_decay","eta_decay","phi_decay","E_decay","dpt_decay","acop","acop_zoom","dphi","dphi_zoom"];
histoslog_axis   = ["M(e^{+}e^{-})","p_{T}(x^{#pm})","p_{T}(e^{+}e^{-})","#eta(e^{+}e^{-})","#phi(x^{+},x^{-})","E(x^{+},x^{-})","#Delta p_{T}(e^{+}e^{-})","1-|#Delta#phi(e^{+}e^{-})/#pi|","1-|#Delta#phi(e^{+}e^{-})/#pi|","|#Delta#phi(e^{+}e^{-})|","|#Delta#phi(e^{+}e^{-})|"];
histoslog_varx   = ["GeV","GeV","GeV","","","GeV","GeV","","","deg","deg"];

# STARTING THE LOOP OVER FILES:
for i in range(len(FILES)):
        f = open(FILES[i],'r');
        print("Opening file %i: %s" % (i,FILES[i]));

	# SORTING THE DISTRIBUTIONS IN THE ARRAYS FOR EACH FILE:
	# EACH ARRAYS IS FORMATTED LIKE: array[] = [plots_file1, plots_file2, plots_file3, ...
        invm_decay.append(TH1D("1D_invm_decay"+"_"+PDF[i],"", 50,  20., 150.));
        pt_decay.append(TH1D("1D_pt_decay"+"_"+PDF[i]	, "", 50,  0., 200.));
        ptsum_decay.append(TH1D("1D_ptsum_decay"+"_"+PDF[i], "", 50,  0., 360.));
        eta_decay.append(TH1D("1D_eta_decay"+"_"+PDF[i]	, "", 50,-10.,  10.));
        phi_decay.append(TH1D("1D_phi_decay"+"_"+PDF[i]	, "", 10, -4.,   4.));
        E_decay.append(TH1D("1D_E_decay"+"_"+PDF[i]	, "", 50,  0., 250.));
        dpt_decay.append(TH1D("1D_dpt_decay"+"_"+PDF[i] , "", 50,  0.,   0.1));
        acop.append(TH1D("1D_acop"+"_"+PDF[i]           , "", 50,  0.,  10.));
        acop_zoom.append(TH1D("1D_acopz"+"_"+PDF[i]     , "", 50,  -.01,   1.));
        dphi.append(TH1D("1D_dphi"+"_"+PDF[i]           , "", 50,  0., 181.));
        dphi_zoom.append(TH1D("1D_dphiz"+"_"+PDF[i]     , "", 50,175., 180.1));

	# LOOP OVER LINES IN LHE SAMPLE:

	# RESET EVENT COUNTING:
        event  = 0;
        evPASS = 0;
        nskip = 0; # NEW
        # START LOOP:
        for line in f:
            nskip += 1;
            line = line.strip();
            if line == "</init>":
                print("Skipping first %i lines." % nskip)
                break;
        for line in f:
		# SKIP BLANK LINES:
                line = line.strip();
                if not line: continue;
                # STORE LINES INTO ARRAY:
                coll = line.split();
                #print(coll[0])
                # READ EVENT CONTENT:
                if coll[0] == "<event>":
                        event += 1;
                        # SET A SCREEN OUTPUT FOR CONTROL:
                        if Nevt < 10000: evtsplit = 1000;
                        else: evtsplit = 10000;
                        perct = event / Nevt * 100.;
                        if event%evtsplit==0: print("Event %i [%.2f%%]" % (event,perct));
                        elif event>Nevt: break;
                # 4-VECTORS FOR DECAY PRODUCTS:
                elif (coll[0] == '11') and coll[1] == '1':
                        dp = TLorentzVector();
                        px = float(coll[6]);
                        py = float(coll[7]);
                        pz = float(coll[8]);
                        en = float(coll[9]);
                        dp.SetPxPyPzE(px,py,pz,en);
                elif coll[0] == '-11':
                        dm = TLorentzVector();
                        px = float(coll[6]);
                        py = float(coll[7]);
                        pz = float(coll[8]);
                        en = float(coll[9]);
                        dm.SetPxPyPzE(px,py,pz,en);
                # CLOSE EVENT AND FILL HISTOGRAMS:
                elif coll[0] == "</event>":
			# KINEMATICS OF DECAY PRODUCTS:
                        if ( cuts and INNER
 			    and (dp+dm).M() >= INVMCUTLOWER
			    and (dp+dm).M() <= INVMCUTUPPER
                            and (dp+dm).Pt() >= PTPAIRCUTLOWER
			    and (dp+dm).Pt() <= PTPAIRCUTUPPER
                            and abs((dp+dm).Eta()) <= ETAPAIRCUT
                            and dp.Pt() >= PTCUTLOWER
                            and dm.Pt() >= PTCUTLOWER
                            and dp.Pt() <= PTCUTUPPER
                            and dm.Pt() <= PTCUTUPPER
			):
				# 1D:
                                invm_decay[i].Fill((dp+dm).M());
                                pt_decay[i].Fill(dp.Pt());
                                pt_decay[i].Fill(dm.Pt());
                                ptsum_decay[i].Fill((dp+dm).Pt());
                                eta_decay[i].Fill((dp).Eta());
                                eta_decay[i].Fill((dm).Eta());
                                phi_decay[i].Fill(dp.Phi());
                                phi_decay[i].Fill(dm.Phi());
                                E_decay[i].Fill(dp.E());
                                E_decay[i].Fill(dm.E());
                                dpt_decay[i].Fill(abs(dp.Pt()-dm.Pt()));
                                dphi[i].Fill(abs(dp.DeltaPhi(dm))*180./3.141592);
                                dphi_zoom[i].Fill(abs(dp.DeltaPhi(dm))*180./3.141592);
                                acop_zoom[i].Fill((1. - abs(dp.DeltaPhi(dm))/3.141592));
                                acop[i].Fill((1. - abs(dp.DeltaPhi(dm))/3.141592));
                                evPASS += 1;
                        elif ( cuts and not INNER
                            and (dp+dm).M() >= INVMCUTLOWER
                            and (dp+dm).M() <= INVMCUTUPPER
                            and (dp+dm).Pt() >= PTPAIRCUTLOWER
                            and (dp+dm).Pt() <= PTPAIRCUTUPPER
                            and abs((dp+dm).Eta()) >= ETAPAIRCUT
                            and dp.Pt() >= PTCUTLOWER
                            and dm.Pt() >= PTCUTLOWER
                            and dp.Pt() <= PTCUTUPPER
                            and dm.Pt() <= PTCUTUPPER
                        ):
                                # 1D:
                                invm_decay[i].Fill((dp+dm).M());
                                pt_decay[i].Fill(dp.Pt());
                                pt_decay[i].Fill(dm.Pt());
                                ptsum_decay[i].Fill((dp+dm).Pt());
                                eta_decay[i].Fill((dp).Eta());
                                eta_decay[i].Fill((dm).Eta());
                                phi_decay[i].Fill(dp.Phi());
                                phi_decay[i].Fill(dm.Phi());
                                E_decay[i].Fill(dp.E());
                                E_decay[i].Fill(dm.E());
                                dpt_decay[i].Fill(abs(dp.Pt()-dm.Pt()));
                                dphi[i].Fill(abs(dp.DeltaPhi(dm))*180./3.141592);
                                dphi_zoom[i].Fill(abs(dp.DeltaPhi(dm))*180./3.141592);
                                acop_zoom[i].Fill((1. - abs(dp.DeltaPhi(dm))/3.141592));
                                acop[i].Fill((1. - abs(dp.DeltaPhi(dm))/3.141592));
                                evPASS += 1;
                        elif not cuts:
				# 1D:
                                invm_decay[i].Fill((dp+dm).M());
                                pt_decay[i].Fill(dp.Pt());
                                pt_decay[i].Fill(dm.Pt());
                                ptsum_decay[i].Fill((dp+dm).Pt());
                                eta_decay[i].Fill((dp).Eta());
                                eta_decay[i].Fill((dm).Eta());
                                phi_decay[i].Fill(dp.Phi());
                                phi_decay[i].Fill(dm.Phi());
                                E_decay[i].Fill(dp.E());
                                E_decay[i].Fill(dm.E());
                                dpt_decay[i].Fill(abs(dp.Pt()-dm.Pt()));
                                dphi[i].Fill(abs(dp.DeltaPhi(dm))*180./3.141592);
                                dphi_zoom[i].Fill(abs(dp.DeltaPhi(dm))*180./3.141592);
                                acop_zoom[i].Fill((1. - abs(dp.DeltaPhi(dm))/3.141592));
                                acop[i].Fill((1. - abs(dp.DeltaPhi(dm))/3.141592));
	# End of loop over lines
        if cuts: print("Events passing acceptance: %i/%i" % (evPASS,event));
# End of loop over files

# Starting Drawing step:

# Defining the top label in the plots:
plotlabel = TPaveText(0.50,0.91,0.84,0.95,"NDC");
plotlabel.SetTextAlign(33);
plotlabel.SetTextColor(1);
plotlabel.SetFillColor(0);
plotlabel.SetBorderSize(0);
plotlabel.SetTextSize(0.035);
plotlabel.SetTextFont(42);
plotlabel.AddText("MadGraphv5 #bullet #sqrt{s}=540 GeV #bullet "+EVTINPUT+" evt");

# Legend:
leg = TLegend(0.55,0.72,0.75,0.87);
leg.SetTextSize(0.035);
leg.SetFillColor(0);
leg.SetBorderSize(0);

# Setting pads:
gStyle.SetOptStat(0);
gStyle.SetPadTickY(1);
gStyle.SetPadTickX(1);
gStyle.SetOptTitle(0);
gStyle.SetLegendBorderSize(0);

# Canvas
canvas = TCanvas("plots","Plots",0,0,1000,1000);

for i in range(len(histoslog)):
	globals()["hs_histoslog"+str(i)] = THStack("hs","");

# Starting loop over histograms in the arrays for each set:

# 1: 1D log-scaled plots:
canvas.SetLeftMargin(0.2);
canvas.SetBottomMargin(0.11);
canvas.SetRightMargin(0.18);
if setLog: gPad.SetLogy(1);
else: gPad.SetLogy(0);
legs=0;
for l in range(len(histoslog)):
        for m in range(len(FILES)):
                if scale:
                        histoslog[l][m].Scale(xsec[m]/Nevt*histoslog[l][m].GetBinWidth(1));
                if scale_yield:
                        histoslog[l][m].Scale(xsec[m]*LUMINOSITY/Nevt*histoslog[l][m].GetBinWidth(1));
                histoslog[l][m].SetLineColor(m+1);
                if (m == 4): histoslog[l][m].SetLineColor(m+2);
                if filled:
                        histoslog[l][m].SetFillColor(m+1);
                        if (m == 4): histoslog[l][m].SetFillColor(m+2);
                histoslog[l][m].SetLineWidth(3);
                histoslog[l][m].SetLineStyle(1);
                globals()["hs_histoslog"+str(l)].Add(histoslog[l][m]);
                leg.AddEntry(histoslog[l][m]," "+PDF[m],"f");
                if data:
                        if m == 0:
                                datapoints = histoslog[l][m].Clone();
                                dataonly = histoslog[l][m].Clone();
                        else:
                                datapoints.Add(histoslog[l][m]);
                                dataonly.Add(histoslog[l][m]);
                                datapoints.SetFillStyle(0);
                                datapoints.SetLineWidth(0);
                                datapoints.SetLineStyle(0);
                                datapoints.SetMarkerStyle(20);
        if stacked:
                globals()["hs_histoslog"+str(l)].Draw("hist");
        else:
                globals()["hs_histoslog"+str(l)].Draw("nostack hist");
        if scale:
                if histoslog_varx[l] == "":
                    globals()["hs_histoslog"+str(l)].GetYaxis().SetTitle("d#sigma/d"+str(histoslog_axis[l])+" (pb)");
                else:
                    globals()["hs_histoslog"+str(l)].GetYaxis().SetTitle("d#sigma/d"+str(histoslog_axis[l])+" (pb/"+str(histoslog_varx[l])+")");
                

        else:
                 
                globals()["hs_histoslog"+str(l)].GetYaxis().SetTitle("Events");
        if scale_yield:
                globals()["hs_histoslog"+str(l)].GetYaxis().SetTitle("Yield");
        else:
                globals()["hs_histoslog"+str(l)].GetYaxis().SetTitle("Events");

        if histoslog_varx[l] == "":
            globals()["hs_histoslog"+str(l)].GetXaxis().SetTitle(str(histoslog_axis[l]));
        else:
            globals()["hs_histoslog"+str(l)].GetXaxis().SetTitle(str(histoslog_axis[l])+" ("+str(histoslog_varx[l])+")");
        globals()["hs_histoslog"+str(l)].GetXaxis().SetTitleFont(42);
        globals()["hs_histoslog"+str(l)].GetYaxis().SetTitleFont(42);
        globals()["hs_histoslog"+str(l)].GetXaxis().SetTitleSize(0.05);
        globals()["hs_histoslog"+str(l)].GetYaxis().SetTitleSize(0.05);
        globals()["hs_histoslog"+str(l)].GetXaxis().SetLabelFont(42);
        globals()["hs_histoslog"+str(l)].GetYaxis().SetLabelFont(42);
        globals()["hs_histoslog"+str(l)].GetXaxis().SetTitleOffset(1.);
        globals()["hs_histoslog"+str(l)].GetYaxis().SetTitleOffset(1.6);
        globals()["hs_histoslog"+str(l)].GetXaxis().SetLabelSize(0.04);
        globals()["hs_histoslog"+str(l)].GetYaxis().SetLabelSize(0.04);
        globals()["hs_histoslog"+str(l)].GetXaxis().SetDecimals(True);
        if data:
                datapoints.Draw("E2,SAME");
                leg.AddEntry(datapoints,"data","p");
        leg.Draw("SAME");
        plotlabel.Draw("SAME");
        for k in range(len(FILE_TYPES)):
                canvas.Print(FILE_TYPES[k]+"/"+JOB+"_"+EVTINPUT+"evt_"+histoslog_label[l]+"."+FILE_TYPES[k]);
        leg.Clear();
        if data:
            dataonly.SetLineStyle(2);
            dataonly.SetFillColor(0);
            dataonly.SaveAs(FILE_TYPES[k]+"/"+JOB+"_"+EVTINPUT+"evt_"+histoslog_label[l]+".root");
# END loop over plots in log scale

FILEROOT.Write();

#####################################################################
#
# C'ESTI FINI
#
#####################################################################
