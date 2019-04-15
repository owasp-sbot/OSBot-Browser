from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc


class Node_Format:

    @staticmethod
    def issue_type_color(node, issue, set_label=True):
        if issue:
            colors = ['darkred', 'red', 'orange', 'darkgreen', 'green']
            issue_type = issue.get('Issue Type')
            if set_label:
                node['label'] = issue_type
            color = '#9EC2F7'
            font_color = 'black'
            if issue_type == 'Risk Theme'   : color = colors[0]; node['mass'] = 10; font_color = 'White'
            if issue_type == 'Risk'         : color = colors[1]; node['mass'] = 4 ; font_color = 'White'
            if issue_type == 'Vulnerability': color = colors[2]; node['mass'] = 2
            if issue_type == 'Fact'         : color = colors[3];
            if issue_type == 'GS-Project'   : color = 'black'  ; node['mass'] = 10; font_color = 'White'
            if issue_type == 'Programme'    : color = 'gray'   ; node['mass'] = 10; font_color = 'White'
            #if issue_type == 'Low': color = colors[4]; font_color = 'white'
            node['color'] = color
            node['font'] = {'color': font_color}
        return Node_Format

    @staticmethod
    def rating_color(node, issue, set_label=True):
        if issue:
            colors = ['darkred', 'red', 'orange', 'darkgreen', 'green']
            rating = issue.get('Rating')
            if set_label:
                node['label'] = rating
            color      = '#9EC2F7'
            font_color = 'Black'
            if rating == 'TBD'   : color = 'black'   ; font_color='white'
            if rating == 'High'  : color = colors[0] ; font_color='white'
            if rating == 'Medium': color = colors[2]
            if rating == 'Low'   : color = colors[4] ; font_color='white'
            node['color'] = color
            node['font' ] = {'color' : font_color}
        return Node_Format

    @staticmethod
    def status_color(node, issue, set_label=True):
        if issue:
            colors = ['darkred', 'red', 'orange', 'darkgreen', 'green']
            rating = issue.get('Status')
            if set_label:
                node['label'] = rating
            color      = '#9EC2F7'
            font_color = 'Black'
            if rating == 'False Positive / Not issue'                       : color = 'black'   ; font_color='white'
            if rating == 'Awaiting Acceptance'                              : color = colors[0] ; font_color='white'
            if rating in ['To VULN Assess' ,'To Risk Assess','To Validate'] : color = colors[2]
            if rating == 'Allocated for Fix'                                : color = colors[2]
            if rating == 'Fixed'                                            : color = colors[4] ; font_color='white'
            if rating in ['To Do','Open']                                   : color = 'Gray'    ; font_color='white'
            node['color'] = color
            node['font' ] = {'color' : font_color}
        return Node_Format

    @staticmethod
    def size_by_r123(node, issue, set_label=True):
        if issue:
            labels = issue.get('Labels')
            size  = None
            label = None
            node['mass'] = 1
            if 'R0' in labels: size = 40 ; label = 'R0' ; node['mass'] = 10
            if 'R1' in labels: size = 30 ; label = 'R1' ; node['mass'] = 2
            if 'R2' in labels: size = 20 ; label = 'R2' ;
            if 'R3' in labels: size = 15 ; label = 'R3'
            if size:
                if node['font']:
                    node['font']['size'] = size
                else:
                    node['font'] = {'color': size}
            if label and set_label:
                node['label'] = "{0}\n({1})".format(label,node['label'])
        return Node_Format


    # @staticmethod
    # def set_r1_positions(node):
    #     r1s = {
    #             'RISK-1495': {'x': 0     , 'y': -300 }, # 3
    #             'RISK-1494': {'x': 1000  , 'y': -300 }, # 4
    #             'RISK-1534': {'x': 0     , 'y': 300 }, # 5
    #             'RISK-1592': {'x': 1000  , 'y': 300 }} # 6
    #     issue_id = node.get('id')
    #     if issue_id in list(set(r1s)):
    #         node['fixed'] = True
    #         node['x'    ] = r1s[issue_id]['x']
    #         node['y'    ] = r1s[issue_id]['y']
    #         del node['mass']
    #         Dev.pprint(node)
    #     else:
    #         node['label'] = ''
    #     return Node_Format

    @staticmethod
    def add_key_to_label(node):
        if node['label'] != '':
            node['label'] += '\n({0})'.format(node.get('id'))
        else:
            node['label'] = node.get('id')
            node['font' ] = {'size' : 8 }
        return Node_Format

    @staticmethod
    def add_issue_type_to_label(node, issue):
        if issue:
            node['label'] += '\n({0})'.format(issue.get('Issue Type'))
        return Node_Format

    @staticmethod
    def add_status_to_label(node, issue):
        if issue:
            node['label'] += '\n({0})'.format(issue.get('Status'))
        return Node_Format

    @staticmethod
    def only_highs(node,issue):
        if issue:
            if issue['Rating'] != 'High':
                node['label'] = ''
        return Node_Format

    @staticmethod
    def no_label(node):
        node['label'] = ''
        return Node_Format

    @staticmethod
    def no_label_for_issue_type(node, issue, issue_type):
        if issue and issue.get('Issue Type') == issue_type:
            node['label'] = ''
        return Node_Format

    @staticmethod
    def set_label(node, issue, key):
        if issue:
            node['label'] = Misc.word_wrap(issue.get(key), 20)
        return Node_Format


    # Nodes issues
    @staticmethod
    def remove_fixed_and_fp(nodes, issues):
        for node in list(nodes):
            issue = issues.get(node.get('id'))
            if issue:
                status = issue.get('Status')
                if status in ['Fixed','False Positive / Not issue']:
                    nodes.remove(node)

        return Node_Format