"""
Useful pipeline elements which might be used for constructing Analysis Pipelines
"""
from neuropipes.pipeline import _PipelineElement

class DummyNode(_PipelineElement):
    def __init__(self, method=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = ""
        self.output_type = 'other'
        self.output_dim = 'match_input'



class ExtractEvents(_PipelineElement):
    def __init__(self, func=None, method=None, threshold=None, fields=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "ExtractEvents"
        self.output_type = 'iv'
        if func is not None:
            if fields is not None:
                self.label = self.label + "()"
                # self.label = self.label + "(func=f(), fields=[...])"
                # self.sublabel = '<font face="Times-Italic">find intervals where f({})</font>'.format(fields[0])
                self.input_types = ['other']
            else:
                self.label = self.label + "()"
                # self.label = self.label + "(func=f())"
                # self.sublabel = '<font face="Times-Italic">find intervals where f()</font>'
                self.input_types = ['tsdata']
        elif (method=='above') & (threshold is not None) :
            self.input_types = ['tsdata']
            if fields is not None:
                self.label = self.label + '()'
                # self.label = self.label + "(fields={}, method='above',<br/>    threshold={})".format(fields[0],threshold)
                #self.sublabel = '<font face="Times-Italic">periods when input.{} &gt; {}</font>'.format(fields[0],threshold)
            else:
                self.label = self.label + '(>{})'.format(threshold)
                #self.label = self.label + "(method='above',<br/>    threshold={})".format(threshold)
                #self.sublabel = '<font face="Times-Italic">periods when input &gt; {}</font>'.format(threshold)
        elif (method=='between') & (fields is not None):
            self.input_types = ['metadata']
            self.label = self.label + "()"
            #self.label = self.label + "(method='between',<br/>    fields={})".format(fields)
            #self.sublabel = '<font face="Times-Italic">periods between {} and {}</font>'.format(fields[0],fields[1])
            self.named_inputs.append('metadata')

        self.output_dim = 'single'

class MergeEvents(_PipelineElement):
    def __init__(self, method=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "MergeEvents"
        self.input_types = ['iv','iv']
        self.output_type = 'iv'
        self.output_dim = 'single'
        if (method=='intersect'):
            self.label = self.label + '()'
            # self.label = self.label + '("method=intersect")'


class RestrictByIntervals(_PipelineElement):
    def __init__(self, intervals=None, data=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "RestrictByIntervals()"
        self.output_type = ('ts','tsdata')
        self.input_types = [('ts','tsdata'),'iv']
        if data:
            self.named_inputs.append(data)
        self.output_dim = 'match_input'


class FilterSWR(_PipelineElement):
    def __init__(self, params=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = 'RippleFilter(params=...)'
        self.output_type = 'tsdata'
        self.input_types = ['tsdata']
        self.named_inputs = ["lfp"]
        self.output_dim = 'match_input'


class DetectSWREvents(_PipelineElement):
    def __init__(self, detect_thresh=4.0,boundary_thresh=0.0,
                 multiple_tetrodes='average',**kwargs):
        super().__init__(self, **kwargs)
        self.label = "DetectSWREvents(params=...)"
        self.output_type = 'iv'
        self.input_types = ['tsdata']

class CalcFiringRate(_PipelineElement):
    def __init__(self, method=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "CalcFiringRate()"
        self.input_types = ['ts']
        self.output_type = 'other'
        self.output_dim = 'match_input'

class SmoothSpikes(_PipelineElement):
    def __init__(self, kernel_width=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "SmoothSpikes()"
        self.input_types = ['ts']
        self.output_type = 'tsdata'
        self.named_inputs = ["spikes"]
        self.output_dim = 'multi'

class LinearizePosition(_PipelineElement):
    def __init__(self, method=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "LinearizePosition()"
        self.input_types = ['tsdata']
        self.output_type = 'tsdata'
        self.named_inputs = ["pos"]

class EstimatePlaceFields(_PipelineElement):
    def __init__(self, option=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "EstimatePlaceFields()"
        self.input_types = ['tsdata','tsdata']
        self.output_type = 'tuningcurve'

class Decode(_PipelineElement):
    def __init__(self, option=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "Decode()"
        self.input_types = ['tuningcurve','tsdata']
        self.output_type = 'tsdata'

class ScoreReplay(_PipelineElement):
    def __init__(self, option=None, **kwargs):
        super().__init__(self, **kwargs)
        self.label = "ScoreReplay()"
        self.input_types = ['tsdata']
        self.output_type = 'other'
