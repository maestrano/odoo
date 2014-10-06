{
    'name': 'Maestrano',
    'version': '1.0',
    'category': 'Tools',
    'description': """
Allow users to login through Maestrano.
====================================
""",
    'author': 'Maestrano Pty Ltd',
    'maintainer': 'Maestrano Pty Ltd',
    'website': 'https://maestrano.com',
    'depends': ['base', 'web'],
    'qweb' : ["static/src/xml/*.xml"],
    'external_dependencies': {},
    'installable': True,
    'auto_install': True,
    'js' : ["//cdn.maestrano.com/apps/mno_libs/mno-loader.js","static/src/js/mno-init.js"],
}
