{
    'name':"Real-Estate Management",
    'version':'1.0',
    'depends':['base'],
    'author':"qasim",
    'category':'Category',
    'description':"""This is a test module of Real-Estate Management""",
    'data': [
    'data/estate_property_data.xml',
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_property_type_views.xml',
    'views/users_inherit_views.xml',
    'views/estate_property_tag_views.xml',
    'views/estate_menus.xml',
],

    'installable': True,
    'auto_install': False,
    'application':  True,
}