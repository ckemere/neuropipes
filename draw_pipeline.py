"""
Function to draw Analysis Pipelines using Graphviz
"""

import graphviz as gv

def draw_pipeline(final_nodes, filename='graph', graph_format='png',
    text_font='Arial',monospace_font='Courier',suppress_arrowheads=False,
    final_view=True,
    show_legend=True,
    legend_order=['ts','tsdata','iv','metadata','tuningcurve','other'],
    legend_colors={'ts':'orchid2', 'tsdata':'chartreuse', 'iv':'deepskyblue1',
                  'metadata': 'pink1', 'tuningcurve':'darksalmon', 'other':'black'}):
    gmain = gv.Digraph(format=graph_format)
    gmain.body.extend(['outputorder=edgesfirst','fontname = "{}"'.format(text_font),
        'overlap = false','nodesep=0.3','ranksep=0.1'])
    if (graph_format=='png') :
        gmain.body.extend(['resolution=300'])
    gmain.edge_attr.update(fontcolor='blue', fontname=text_font, fontsize='8', penwidth='1')
    if (suppress_arrowheads) :
        gmain.edge_attr.update(arrowhead='none')
    gmain.node_attr.update(shape='rectangle',fontsize='8',fontname=monospace_font,
        margin='0.05,0.05',style='plain-text',color='invis',fillcolor='invis')

    g1 = gv.Digraph('Main Graph')
    all_nodes = []
    counter = 0
    clusters = []

    def add_parents(node, node_list):
        for n in node.input_nodes:
            if n not in node_list:
                node_list.append(n)
                if n.label is None:
                    n.label = "N{}".format(len(node_list))
                node_list = add_parents(n, node_list)
        return node_list

    for leaf in final_nodes:
        all_nodes.append(leaf)
        if leaf.label is None:
            leaf.label = "N{}".format(len(all_nodes))
        all_nodes = add_parents(leaf, all_nodes)

    for n in all_nodes:
        label = '<<table cellborder="0" border="0" cellspacing="0"><tr>'+ \
        ''.join(['<td fixedsize="true" width="12" height="0.1" port="p{}"></td>'.format(i) for i in range(3)]) + '</tr>'

        if n.sublabel:
            label = label + \
                '<tr><td colspan="3" bgcolor="white" border="1" color="black" port="pp">{}<br/>{}</td></tr></table>>'.format(n.label,n.sublabel)
        else:
            label = label + \
                '<tr><td colspan="3" bgcolor="white" border="1" color="black" port="pp">{}</td></tr></table>>'.format(n.label)

        if (n.vis_cluster):
            cxl = [v[1] for i, v in enumerate(clusters) if v[0] == n.vis_cluster]
            if not cxl: # if n.vis_cluster not in clusters:
                newcluster = gv.Digraph('cluster_{}'.format(n.vis_cluster))
                clusters.append((n.vis_cluster,newcluster))
                cx = newcluster
            else:
                cx = cxl[0]
            cx.node(str(id(n)),label=label)
        else:
            g1.node(str(id(n)),label=label)

    for cxl in clusters:
        cxl[1].body.append('style=filled')
        cxl[1].body.extend(['color=lightgrey','rank="same"','fontsize=8', 'nodesep=0.1','ranksep=0.1',
            'margin="0.05,0.05"', 'label="{}"'.format(cxl[0])])
        g1.subgraph(cxl[1])

    for n in all_nodes:
        if len(n.input_nodes) == 0:
            continue
        elif len(n.input_nodes) == 1:
            input_ports = ['p1']
        elif len(n.input_nodes) == 2:
            input_ports = ['p0','p2']
        elif len(n.input_nodes) == 3:
            input_ports = ['p0','p1','p2']
        elif len(n.input_nodes) > 3:
            input_ports = ['p1']*len(n.input_nodes)

        for edge_idx, nparent in enumerate(n.input_nodes):
            multiedge = nparent.output_dim
            if (multiedge =='match_input'):
                for m in nparent.input_nodes:
                    if(m.output_type == nparent.output_type):
                        multiedge = m.output_dim
                        break

            if (multiedge == 'multi'):
                penwidth = '2'
            else:
                penwidth = '1'
#                for i in range(2):
#                    g1.edge(str(id(nparent)),str(id(n)),
#                        color=legend_colors[nparent.output_type])

            if nparent.output_label:
                g1.edge(str(id(nparent))+':pp:s',str(id(n))+':{}:s'.format(input_ports[edge_idx]),
                        xlabel=nparent.output_label,
                        color=legend_colors[nparent.output_type],
                        penwidth=penwidth)
            else:
                g1.edge(str(id(nparent))+':pp:s',str(id(n))+':{}:s'.format(input_ports[edge_idx]),
                       color=legend_colors[nparent.output_type],
                       penwidth=penwidth)



    if show_legend:
        leg= gv.Digraph('legend')
        leg.node_attr.update(fontsize='7',color='invis',fillcolor='invis')
        leg.body.extend(['rank=max'])
        leg.node('keyleft', label='<<table border="0" cellpadding="1" cellspacing="0" cellborder="0">' +
            ''.join(['<tr><td port="i{}">&nbsp;</td></tr>'.format(idx)
                 for idx in range(len(legend_order))]) + '</table>>')
        leg.node('keyright', label='<<table border="0" cellpadding="1" cellspacing="0" cellborder="0">' +
            ''.join(['<tr><td align="left" port="i{}">{}</td></tr>'.format(idx,item)
                 for (idx,item) in enumerate(legend_order)]) + '</table>>')
        for idx,key in enumerate(legend_order):
            leg.edge('keyleft:i{}:e'.format(idx),'keyright:i{}:w'.format(idx),
                color=legend_colors[key],arrowhead='none')


        cleg = gv.Digraph('cluster_legend_wrapper')
        cleg.body.extend(['fontsize=8','label="Data Types"','margin=0','pencolor=transparent'])
        cleg.subgraph(leg)

        # Get legend to be at bottom!
        dummy = gv.Digraph('force-bottom')
        dummy.body.extend(['rank=max'])
        dummy.node('dummy',label="",style='plain-text',color='invis',fillcolor='invis')
        gmain.subgraph(dummy) # make it left most

        gmain.subgraph(g1)
        gmain.subgraph(cleg)
        gmain.edge('dummy','keyleft',style='invis')
    else:
        gmain.subgraph(g1)


    gmain.render(filename)
    if (final_view):
        gmain.view(filename)
