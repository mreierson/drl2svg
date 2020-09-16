#!/usr/bin/python

import os
import re
import svgwrite
import sys

tools = {}
tool_size = re.compile('(T\d)C(.+)')
hole_coords = re.compile('.*X(.+)Y(.+)')

current_tool = ''
current_tool_size = 0.00

dwg = svgwrite.Drawing('drill.svg')

hole_group = dwg.g(id='drills')
    
if len(sys.argv) > 1:
    drill_fd = open(sys.argv[1], 'r')
    for line in drill_fd.readlines():
        sline = line.strip()

        tool_match = tool_size.match(sline)
        if tool_match:
            tools[tool_match.group(1)] = tool_match.group(2)
        else:
            if sline[0] == 'T':
                if (sline in tools):
                    current_tool = sline
                    current_tool_size = tools[sline]
            else:
                hole_match = hole_coords.match(sline)
                if (hole_match):
                    holex = hole_match.group(1)
                    holey = hole_match.group(2)
                    hole_group.add(dwg.circle(center=(float(holex)* svgwrite.mm, float(holey) * svgwrite.mm), r=current_tool_size, fill='none', stroke='black', stroke_width=0.1))
                

if len(sys.argv) > 2:
    edge_fd = open(sys.argv[2], 'r')
    for line in edge_fd.readlines():
        sline = line.strip()
        if (sline == '</svg>'):
            print hole_group.tostring()
            print sline
        else:
            print sline
else:
    dwg.add(hole_group)
    print dwg.tostring()
        
