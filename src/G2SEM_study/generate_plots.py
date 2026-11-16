#!/usr/bin/env python3
import os
from array import array
import ROOT

# Run ROOT in batch mode (equivalent to root -b)
ROOT.gROOT.SetBatch(True)


def load_ratio_graphs(ds_list, denom_branch, color_map, marker_style=20):
    """Reads data_<ds>.root for each dataset in ds_list and returns a dict of TGraphs."""
    graphs = {}

    for ds in ds_list:
        fname = f"data_{ds}.root"
        if not os.path.exists(fname):
            print(f"Warning: {fname} not found, skipping.")
            continue

        tfile = ROOT.TFile.Open(fname, "READ")
        if not tfile or tfile.IsZombie():
            print(f"Warning: Could not open {fname}, skipping.")
            continue

        tree = tfile.Get("tree")
        if not tree:
            print(f"Warning: 'tree' not found in {fname}, skipping.")
            tfile.Close()
            continue

        # Prepare branch buffers matching the C++ types in draw.cc
        spill_id = array("I", [0])
        e906bm = array("f", [0.0])
        denom = array("f", [0.0])

        tree.SetBranchAddress("spill_id", spill_id)
        tree.SetBranchAddress("e906bm", e906bm)
        tree.SetBranchAddress(denom_branch, denom)

        gr = ROOT.TGraph()
        # Let Python manage the primary TGraph; we will add clones to TMultiGraph
        ROOT.SetOwnership(gr, True)
        gr.SetName(f"gr_e906bm_{denom_branch}_rs{ds}")
        gr.SetMarkerColor(color_map.get(ds, ROOT.kBlack))
        gr.SetLineColor(color_map.get(ds, ROOT.kBlack))
        gr.SetMarkerStyle(marker_style)
        gr.SetMarkerSize(0.6)

        pt_idx = 0
        n_ent = tree.GetEntries()
        for i in range(n_ent):
            tree.GetEntry(i)
            if denom[0] > 0 and e906bm[0] > 0:
                gr.SetPoint(pt_idx, float(spill_id[0]), float(e906bm[0]) / float(denom[0]))
                pt_idx += 1

        tfile.Close()

        if gr.GetN() > 0:
            graphs[ds] = gr

    return graphs


def build_multigraph(graphs_dict, title, y_min, y_max):
    """Creates a TMultiGraph containing cloned TGraphs so C++ ownership never conflicts."""
    mg = ROOT.TMultiGraph()
    mg.SetTitle(title)
    for ds, gr in graphs_dict.items():
        gr_clone = gr.Clone(f"{gr.GetName()}_mg")
        ROOT.SetOwnership(gr_clone, False)  # TMultiGraph owns the clone
        mg.Add(gr_clone, "P")
    mg.SetMinimum(y_min)
    mg.SetMaximum(y_max)
    return mg


def plot_group(ds_list, denom1, denom2, y_min=2e-8, y_max=1.5e-7):
    os.makedirs("result", exist_ok=True)
    ds_tag = "_".join(ds_list)
    ds_title = ", ".join(ds_list)

    color_map = {
        "57": ROOT.kRed,
        "59": ROOT.kBlue,
        "62": ROOT.kRed,
        "67": ROOT.kBlue,
        "70": ROOT.kGreen + 2,
    }

    graphs1 = load_ratio_graphs(ds_list, denom1, color_map, marker_style=20)
    graphs2 = load_ratio_graphs(ds_list, denom2, color_map, marker_style=24)

    c1 = ROOT.TCanvas(f"c1_{ds_tag}", "", 900, 600)
    c1.SetGrid()

    # 1. Single-canvas plot for e906bm / denom1
    mg1 = None
    leg1 = None
    if graphs1:
        mg1 = build_multigraph(
            graphs1,
            f"RS {ds_title};Spill ID;E906BM / {denom1.upper()}",
            4e-8,
            9e-8,
        )
        mg1.Draw("AP")
        c1.Update()

        leg1 = ROOT.TLegend(0.75, 0.75, 0.98, 0.95)
        for ds, gr in graphs1.items():
            leg1.AddEntry(gr, f"RS {ds} (E906BM/{denom1.upper()})", "p")
        leg1.Draw()

        c1.Update()
        c1.SaveAs(f"result/gr_e906bm_{denom1}_rs{ds_tag}.pdf")

    # 2. Single-canvas plot for e906bm / denom2
    mg2 = None
    leg2 = None
    if graphs2:
        c1.Clear()
        c1.SetGrid()
        mg2 = build_multigraph(
            graphs2,
            f"RS {ds_title};Spill ID;E906BM / {denom2.upper()}",
            y_min,
            y_max,
        )
        mg2.Draw("AP")
        c1.Update()

        leg2 = ROOT.TLegend(0.75, 0.75, 0.98, 0.95)
        for ds, gr in graphs2.items():
            leg2.AddEntry(gr, f"RS {ds} (E906BM/{denom2.upper()})", "p")
        leg2.Draw()

        c1.Update()
        c1.SaveAs(f"result/gr_e906bm_{denom2}_rs{ds_tag}.pdf")

    # 3. Combined plots with both ratios on the same TCanvas
    if graphs1 or graphs2:
        # 3a. Overlaid on a single canvas
        c1.Clear()
        c1.SetGrid()
        mg_both = ROOT.TMultiGraph()
        mg_both.SetTitle(
            f"RS {ds_title};Spill ID;E906BM / ({denom1.upper()}, {denom2.upper()})"
        )
        for gr in graphs1.values():
            gr_c = gr.Clone(f"{gr.GetName()}_both1")
            ROOT.SetOwnership(gr_c, False)
            mg_both.Add(gr_c, "P")
        for gr in graphs2.values():
            gr_c = gr.Clone(f"{gr.GetName()}_both2")
            ROOT.SetOwnership(gr_c, False)
            mg_both.Add(gr_c, "P")

        mg_both.SetMinimum(y_min)
        mg_both.SetMaximum(y_max)
        mg_both.Draw("AP")
        c1.Update()

        leg_both = ROOT.TLegend(0.70, 0.68, 0.98, 0.95)
        for ds, gr in graphs1.items():
            leg_both.AddEntry(gr, f"RS {ds}: E906BM / {denom1.upper()}", "p")
        for ds, gr in graphs2.items():
            leg_both.AddEntry(gr, f"RS {ds}: E906BM / {denom2.upper()}", "p")
        leg_both.Draw()

        c1.Update()
        c1.SaveAs(f"result/gr_e906bm_{denom1}_and_{denom2}_overlaid_rs{ds_tag}.pdf")

        # 3b. Two vertical pads on the same TCanvas
        c2 = ROOT.TCanvas(f"c2_{ds_tag}", "", 900, 900)
        c2.Divide(1, 2)

        if mg1 and leg1:
            pad1 = c2.cd(1)
            pad1.SetGrid()
            mg1.Draw("AP")
            leg1.Draw()

        if mg2 and leg2:
            pad2 = c2.cd(2)
            pad2.SetGrid()
            mg2.Draw("AP")
            leg2.Draw()

        c2.Update()
        c2.SaveAs(f"result/gr_e906bm_{denom1}_and_{denom2}_2pads_rs{ds_tag}.pdf")


def main():
    # Group 1: data_62.root, data_67.root, data_70.root -> e906bm/g2sem & e906bm/nm3sem
    plot_group(
        ds_list=["62", "67", "70"],
        denom1="g2sem",
        denom2="nm3sem",
        y_min=2e-8,
        y_max=1.5e-7,
    )

    # Group 2: data_57.root, data_59.root -> e906bm/g2sem & e906bm/nm3ion
    plot_group(
        ds_list=["57", "59"],
        denom1="g2sem",
        denom2="nm3ion",
        y_min=2e-8,
        y_max=1.5e-7,
    )


if __name__ == "__main__":
    main()