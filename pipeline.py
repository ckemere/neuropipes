"""
Skeleton neural-data-analysis functions
"""

import numpy as np

class _PipelineElement:
    def __init__(self, label=None, output_label=None, output_name=None, vis_cluster=None,
                output_type=None, output_dim=None):
        self.num_inputs = 0
        self.named_inputs = []
        self.input_types = []

        if output_type is not None:
            self.output_type = output_type
        else:
            self.output_type = 'other'

        self.output_name = None

        self.input_nodes = []

        # for visualization
        self.label = None
        self.output_label = None
        self.vis_cluster = None
        self.sublabel = None
        if output_dim is not None:
            self.output_dim = output_dim
        else:
            self.output_dim = 'single'

        if label is not None:
            self.label = label

        if output_label is not None:
            self.output_label = output_label

        if output_name is not None:
            self.output_name = output_name

        if vis_cluster is not None:
            self.vis_cluster = vis_cluster


    def add_parent(self, node):
        self.input_nodes.append(node)
        self.input_types.append(node.output_type)


class Analysis:
    def __init__(self, DataDir=None, CacheDataDir=None, Subjects=None, ShowRawData=True):
        if ShowRawData:
            self.metadata = _PipelineElement('Metadata',output_name='metadata', vis_cluster="Raw Data")
            self.metadata.output_type = 'metadata'
            self.metadata.output_dim = 'single'
            self.lfp = _PipelineElement('LFP',output_name='lfp', vis_cluster="Raw Data")
            self.lfp.output_type = 'tsdata'
            self.lfp.output_dim = 'multi'
            self.spikes = _PipelineElement('Spikes',output_name='spikes', vis_cluster="Raw Data")
            self.spikes.output_type = 'ts'
            self.spikes.output_dim = 'multi'
            self.pos = _PipelineElement('Pos',output_name='pos', vis_cluster="Raw Data")
            self.pos.output_type = 'tsdata'
            self.pos.output_dim = 'single'
            self.PipelineNodes = [self.metadata, self.lfp, self.spikes, self.pos]
        else:
            self.PipelineNodes = []

        if Subjects is None:
            Subjects = []
        self.Subjects = Subjects
        self.CacheDataDir=CacheDataDir
        self.DataDir = DataDir

    def make_pipeline(self,steps):
        for idx, node in enumerate(steps):
            # Make sure each element of the pipeline is a tuple
            if not isinstance(node,tuple):
                steps[idx] = (node,)
            # Append previous pipeline element to tuple
            if (idx > 0):
                steps[idx] = steps[idx] + (steps[idx-1][0],)

        # Each element in pipeline is a tuple (_PipelineElement, parent1, parent2, ...)
        # The parent elements are either _PipelineElements which were already
        #  added to the Analysis pipeline or strings which match the name of
        #  a _PipelineElement in the pipeline.
        for idx,elem in enumerate(steps):
            node = elem[0]
            if node not in self.PipelineNodes:
                for p in elem[1:] :
                    if isinstance(p,str):
                        node.named_inputs.append(p)
                    elif isinstance(p,_PipelineElement):
                        node.add_parent(p)
                    else:
                        printf('Error - should be either a Pipeline element or string')
                for name in node.named_inputs:
                    for n in self.PipelineNodes:
                        if (n.output_name == name):
                            node.add_parent(n)
                            break
                self.PipelineNodes.append(node)

                # Adjust the output_type if it depends on the pipeline
                if isinstance(node.output_type, tuple):
                    print(node.output_type)
                    for n in node.input_nodes:
                        print(n)
                        if (n.output_type in node.output_type):
                            print(n.output_type)
                            steps[idx][0].output_type = n.output_type
                            break

        return steps[-1][0]
