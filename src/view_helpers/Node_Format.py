from utils.Misc import Misc


class Node_Format:

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
    def size_by_r123(node, issue, set_label=True):
        if issue:
            labels = issue.get('Labels')
            size  = None
            label = None
            node['mass'] = 1
            if 'R0' in labels: size = 40 ; label = 'R0' ; node['mass'] = 10
            if 'R1' in labels: size = 30 ; label = 'R1' ; node['mass'] = 2
            if 'R2' in labels: size = 20 ; label = 'R2'
            if 'R3' in labels: size = 15 ; label = 'R3'
            if size:
                if node['font']:
                    node['font']['size'] = size
                else:
                    node['font'] = {'color': size}
            if label and set_label:
                node['label'] = "{0}\n({1})".format(label,node['label'])
        return Node_Format

    @staticmethod
    def set_Label(node, issue, key):
        if issue:
            node['label'] = Misc.word_wrap(issue.get(key),20)
        return Node_Format

    @staticmethod
    def add_Key_to_Label(node):
        node['label'] += '\n({0})'.format(node.get('id'))
        return Node_Format

    @staticmethod
    def only_highs(node,issue):
        if issue:
            if issue['Rating'] != 'High':
                node['label'] = ''
        return Node_Format
