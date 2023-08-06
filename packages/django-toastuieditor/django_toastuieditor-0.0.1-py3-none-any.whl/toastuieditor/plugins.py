# PLUGINS = {
#     'uml': {
#         'cdn': "https://uicdn.toast.com/editor-plugin-uml/latest/toastui-editor-plugin-uml.min.js",
#         'local': "toastuieditor/plugins/uml/toastui-editor-plugin-uml.min.js"
#     },
#     'chart': {
#         'cdn': [
#                 'https://uicdn.toast.com/chart/latest/toastui-chart.min.js', 
#                 'https://uicdn.toast.com/editor-plugin-chart/latest/toastui-editor-plugin-chart.min.js',
#                 'https://uicdn.toast.com/chart/latest/toastui-chart.min.css'
#             ], 
#         'local':[
#                 'toastuieditor/plugins/chart/uicdn.toast.com_chart_latest_toastui-chart.min.css',
#                 "toastuieditor/plugins/chart/uicdn.toast.com_chart_latest_toastui-chart.min.js", 
#                 "toastuieditor/plugins/chart/toastui-editor-plugin-chart.min.js",
#             ],
#     },
#     'code-syntax-highlight': {
#         'cdn': [
#                 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/themes/prism.min.css', 
#                 'https://uicdn.toast.com/editor-plugin-code-syntax-highlight/latest/toastui-editor-plugin-code-syntax-highlight.min.css',
#                 'https://uicdn.toast.com/editor-plugin-code-syntax-highlight/latest/toastui-editor-plugin-code-syntax-highlight-all.min.js',
#             ],
#         'local':  [
#                 'toastuieditor/plugins/code-syntax-highlight/toastui-editor-plugin-code-syntax-highlight-all.js',
#                 'toastuieditor/plugins/code-syntax-highlight/prism.min.css', 
#                 'toastuieditor/plugins/code-syntax-highlight/toastui-editor-plugin-code-syntax-highlight.css'
#             ]
#     },
#     'color-syntax': {
#         'cdn': {
#             'js': (
#                 'https://uicdn.toast.com/tui-color-picker/latest/tui-color-picker.min.js',
#                 'https://uicdn.toast.com/editor-plugin-color-syntax/latest/toastui-editor-plugin-color-syntax.min.js'
#             ),
#             'css': (
#                 'https://uicdn.toast.com/tui-color-picker/latest/tui-color-picker.min.css', 
#                 'https://uicdn.toast.com/editor-plugin-color-syntax/latest/toastui-editor-plugin-color-syntax.min.css'
#             )
#         },
#         'local': {
#             'js': [
#                 'toastuieditor/plugins/color-syntax/tui-color-picker.min.js',
#                 'toastuieditor/plugins/color-syntax/toastui-editor-plugin-color-syntax.js'
#             ],
#             'css': [
#                 'toastuieditor/plugins/color-syntax/tui-color-picker.min.css',
#                 'toastuieditor/plugins/color-syntax/toastui-editor-plugin-color-syntax.css'
#             ]
#         }
#     },
#     'table-merged-cell': {
#         'cdn': {
#             'js': 'https://uicdn.toast.com/editor-plugin-table-merged-cell/latest/toastui-editor-plugin-table-merged-cell.min.js',
#             'css': 'https://uicdn.toast.com/editor-plugin-table-merged-cell/latest/toastui-editor-plugin-table-merged-cell.min.css'
#         },
#         'local': {
#             'js': 'toastuieditor/plugins/table-merged-cell/toastui-editor-plugin-table-merged-cell.js',
#             'css': 'toastuieditor/plugins/table-merged-cell/toastui-editor-plugin-table-merged-cell.css'
#         }
#     }
# }

PLUGINS_CDN = {
    'uml': ['https://uicdn.toast.com/editor-plugin-uml/latest/toastui-editor-plugin-uml.min.js',],
}

PLUGINS_LOCAL = {
    'uml': ['toastuieditor/plugins/uml/toastui-editor-plugin-uml.min.js']
}

class Plugin:
    
    def __init__(self, name:str, has_cdn=True) -> None:
        self.name = name
        self.has_cdn = has_cdn
        self.plugins_cdn = PLUGINS_CDN
    
    def get_css_js(self):
        if self.has_cdn:
            medias = self.plugins_cdn.get(self.name.lower())
            if isinstance(medias, (list, tuple)):
                return 
            