MENUS = {
    'NAV_MENU_LEFT': [

     

        # {
        #     "name": "View Patients",
        #     "url": "#",
        #     "icon_class": 'mdi mdi-file-cabinet',
        #     # "validators": [
        #     #             ('mainmenu.menu_validators.has_group' ,'doctor'),
        #     #         ],
                    
        # },

               # another section
        {
            "name": "Metrological Data",
            "url": "#",
            "icon_class": 'mdi mdi-google-analytics',
            "submenu": [
                {
                    "name": "Data Sources",
                    "url": "dashboard:libraries",
                    
                    
                    
                },
                {
                    "name": "Add Data",
                    "url": "dashboard:index",     
                    
                },
                
                {
                    "name": "Process Data",
                    "url": "dashboard:process_data",     
                    
                },
                {
                    "name": "Map Data",
                    "url": "dashboard:map_data",     
                },
               
              
               
          
          
          
            
            ],
        },

    ]
}

