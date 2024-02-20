{
    "name": "Propietats immobiliaries",
    "version": "16.0.0",
    "application": True,
    "depends": ["base"],
    "data": [ 
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        'views/estate_menus.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
