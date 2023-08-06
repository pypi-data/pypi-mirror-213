from typing import Dict, Union, List, Optional, Tuple
import uuid

import numpy as np

from quickstats import semistaticmethod
from quickstats.interface.cppyy.vectorize import as_np_array, as_vector, np_type_str_maps
from .TH1 import TH1
from .TArrayData import TArrayData

class RooAbsPdf:
    
    @staticmethod
    def extract_sum_pdfs_by_category(pdf:"ROOT.RooAbsPdf", poi:Optional["ROOT.RooRealVar"]=None):
        pdf_class = pdf.ClassName()
        if pdf_class != "RooSimultaneous":
            raise RuntimeError(f"input pdf must be a RooSimultaneous instance (`{pdf_class}` received)")
        cat = pdf.indexCat()
        n_cat = cat.size()
        result = {}
        for i in range(n_cat):
            cat.setBin(i)
            cat_name = cat.getLabel()
            cat_pdf = pdf.getPdf(cat_name)
            cat_pdf_class = cat_pdf.ClassName()
            if cat_pdf_class != "RooProdPdf":
                raise RuntimeError(f"category pdf must be a RooProdPdf instance (`{cat_pdf_class}` received)")
            target_pdf = [i for i in cat_pdf.pdfList() if i.ClassName() == "RooRealSumPdf" and i != cat_pdf]
            if not target_pdf:
                raise RuntimeError(f"category pdf does not contain a RooRealSumPdf component")
            if len(target_pdf) > 1:
                raise RuntimeError(f"expect only one RooRealSumPdf component from category pdf but {len(target_pdf)} found")
            target_pdf = target_pdf[0]
            if poi is None:
                result[cat_name] = [i for i in pdf.getComponents()]
            else:
                result[cat_name] = [i for i in pdf.getComponents() if i.dependsOn(poi)]
        return result
    
    @semistaticmethod
    def get_values(self, pdf:"RooAbsPdf",
                   observables:"ROOT.RooArgSet",
                   bin_centers:np.ndarray):
        import ROOT
        vec_bin_centers = as_vector(bin_centers)
        type_str = np_type_str_maps.get(bin_centers.dtype, None)
        if type_str is None:
            bin_centers = bin_centers.astype(float)
            type_str = 'double'
        vec_values = ROOT.RFUtils.GetPdfValues[type_str](pdf, observables, vec_bin_centers)
        values = TArrayData.vec_to_array(vec_values)
        return values
    
    @semistaticmethod
    def get_histogram(self, pdf:"RooAbsPdf",
                      observables:"ROOT.RooArgSet",
                      histname:str='hist',
                      histtitle:Optional[str]=None,
                      nbins:Optional[int]=None,
                      bin_range:Optional[Tuple[float]]=None,
                      weight_scale:Optional[float]=None):
        distribution = self.get_distribution(pdf, observables,
                                             nbins=nbins,
                                             bin_range=bin_range,
                                             weight_scale=weight_scale)
        from quickstats.interface.root import TH1
        from quickstats.maths.statistics import bin_center_to_bin_edge
        bin_edges = bin_center_to_bin_edge(distribution['x'])
        hist = TH1.from_numpy_histogram(distribution['y'],
                                        bin_edges=bin_edges)
        roohist = hist.to_ROOT(histname, histtitle)
        return roohist
    
    @semistaticmethod
    def get_distribution(self, pdf:"RooAbsPdf",
                         observables:"ROOT.RooArgSet", 
                         nbins:Optional[int]=None,
                         bin_range:Optional[Tuple[float]]=None,
                         weight_scale:Optional[float]=None):
        # the observables are needed for normalization
        pdf_obs = pdf.getObservables(observables)
        target_obs = pdf_obs.first()
        if nbins is None:
            nbins = target_obs.numBins()
        if bin_range is None:
            obs_name = target_obs.GetName()
            histogram = pdf.createHistogram(obs_name, nbins)
            py_histogram = TH1(histogram)
            binning_class = target_obs.getBinning().ClassName()
            if binning_class == "RooUniformBinning":
                bin_widths = py_histogram.bin_width
            else:
                bin_widths = RooRealVar.get_bin_widths(target_obs)
            x = py_histogram.bin_center
            y = py_histogram.bin_content * bin_widths
            # free memory to avoid memory leak
            histogram.Delete()
        else:
            assert len(bin_range) == 2
            from quickstats.maths.statistics import get_bin_centers_from_range
            x = get_bin_centers_from_range(bin_range[0], bin_range[1], nbins)
            y = self.get_values(pdf, observables, x)
            normalization = pdf.expectedEvents(pdf_obs)
            bin_width = round((bin_range[1] -  bin_range[0]) / nbins, 8)
            y = y * normalization * bin_width
        if weight_scale is not None:
            y *= weight_scale
        result = {
            'x': x,
            'y': y
        }
        return result
    
    @semistaticmethod
    def get_expected_events_over_range(self, pdf:"RooAbsPdf",
                                       observables:"ROOT.RooArgSet",
                                       range_lo:float,
                                       range_li:float,
                                       normalize:bool=False):
        import ROOT
        expected_events = ROOT.RFUtils.GetPdfExpectedEventsOverRange(pdf, observables,
                                                                     range_lo, range_li,
                                                                     normalize)
        return expected_events
    
    @semistaticmethod
    def get_expected_events_and_error_band_over_range(self, pdf:"RooAbsPdf",
                                                      observables:"ROOT.RooArgSet",
                                                      range_lo:float,
                                                      range_hi:float,
                                                      parameters:"ROOT.RooArgSet",
                                                      fit_result,
                                                      Z:int=1,
                                                      n_samples:Optional[int]=None,
                                                      seed:int=0):
        import ROOT
        central_curve = ROOT.RooCurve()
        nominal_yield = self.get_expected_events_over_range(pdf, observables, range_lo, range_hi)
        central_curve.addPoint(0, nominal_yield)
        clone_func = pdf.cloneTree()
        clone_params = clone_func.getObservables(fit_result.floatParsFinal())
        error_params = clone_params.selectCommon(parameters)
        param_pdf = fit_result.createHessePdf(error_params)
        ROOT.gRandom.SetSeed(seed)
        if n_samples is None:
            n_samples = int(100 / ROOT.TMath.Erfc(Z / ROOT.TMath.Sqrt2())) * 100
        if (n_samples < 100):
            n_samples = 100
        dataset = param_pdf.generate(error_params, n_samples)
        toy_yields = ROOT.RFUtils.GetPdfExpectedEventsOverRangeAcrossDataset(clone_func, dataset,
                                                                             observables,
                                                                             range_lo, range_hi)
        errorband_curve = ROOT.RFUtils.createErrorBandFromArrayData(central_curve, toy_yields, Z)
        # only one point, no need to loop over points
        result = {
            'central': central_curve.GetPointY(0),
            'errorlo': central_curve.GetPointY(0) - errorband_curve.GetPointY(0),
            'errorhi': errorband_curve.GetPointY(1) - central_curve.GetPointY(0)
        }
        return result
    
    @staticmethod
    def get_pdf_map(pdf_dict:Dict):
        import ROOT
        pdf_map = ROOT.std.map('string, RooAbsPdf*')()
        pdf_map.keepalive = list()
        for c, d in pdf_dict.items():
            pdf_map.keepalive.append(d)
            pdf_map.insert(pdf_map.begin(), ROOT.std.pair("const string, RooAbsPdf*")(c, d))
        return pdf_map
    
    @semistaticmethod
    def build_simultaneous_pdf(self, pdfs:Union["RooAbsPdf", List["RooAbsPdf"]],
                               pdf_name:str="simPdf",
                               cat_name:str="indexCat"):
        import ROOT
        category = ROOT.RooCategory(cat_name, cat_name)
        sim_pdf = ROOT.RooSimultaneous(pdf_name, pdf_name, category)
        if not isinstance(pdfs, list):
            pdfs = [pdfs]
        for pdf in pdfs:
            category_name = pdf.GetName()
            category.defineType(category_name)
            sim_pdf.addPdf(pdf, category_name)
        ROOT.SetOwnership(category, False)
        return sim_pdf

    @semistaticmethod
    def remove_disconnected_components(self, pdf:"ROOT.RooProdPdf",
                                       data:"ROOT.RooDataSet",
                                       pdf_name:Optional[str]=None,
                                       pdf_title:Optional[str]=None):
        assert pdf.ClassName() == "RooProdPdf"
        pdf_parameters = pdf.getParameters(data)
        data_parameters = data.get()
        constraints = pdf.getAllConstraints(data_parameters, pdf_parameters, True)
        disconnected_constraints = pdf.getAllConstraints(data_parameters, pdf_parameters, False)
        disconnected_constraints.remove(constraints)
        import ROOT
        base_components = ROOT.RooArgSet()
        ROOT.RFUtils.GetProdPdfBaseComponents(pdf, base_components)
        # remove disconnected pdfs
        base_components.remove(disconnected_constraints)
        if pdf_name is None:
            pdf_name = pdf.GetName()
        if pdf_title is None:
            pdf_title = pdf.GetTitle()
        new_pdf = ROOT.RooProdPdf(pdf_name, pdf_title, base_components)
        return new_pdf