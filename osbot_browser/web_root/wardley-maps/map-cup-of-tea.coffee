

class Maps extends window.Api_VisJs

  create_map_for_tea_original: ()->

    @.add_component('BUSINESS'   , 3, 1)
    @.add_component('PUBLIC'     , 3, 1)
    @.add_component('CUP OF TEA' , 3, 2)
    @.add_component('CUP'        , 4, 3)
    @.add_component('TEA'        , 4, 4)
    @.add_component('HOT WATER'  , 4, 5)
    @.add_component('WATER'      , 4, 6)
    @.add_component('KETTLE'     , 1, 6)
    @.add_component('POWER'      , 4, 7)

    @.add_connection('BUSINESS'   , 'CUP OF TEA')
    @.add_connection('PUBLIC'     , 'CUP OF TEA')
    @.add_connection('CUP OF TEA' , 'CUP'       )
    @.add_connection('CUP OF TEA' , 'TEA'       )
    @.add_connection('CUP OF TEA' , 'HOT WATER' )
    @.add_connection('HOT WATER'  , 'WATER'     )
    @.add_connection('HOT WATER'  , 'KETTLE'    )
    @.add_connection('KETTLE'     , 'POWER'     )

    # adjust text locations

    @.set_node_value('CUP OF TEA', 'font',{ vadjust : -30 })
    @.set_node_value('CUP OF TEA', 'label','CUP OF TEA                             ')
    @.set_node_value('HOT WATER' , 'font',{ vadjust : -30 })
    @.set_node_value('HOT WATER' , 'label','                            HOT WATER')
    @.set_node_value('WATER'     , 'font',{ vadjust : -30 })
    @.set_node_value('WATER'     , 'label','WATER                  ')
    @.set_node_value('POWER'     , 'font',{ vadjust : -30 })
    @.set_node_value('POWER'     , 'label','                       POWER')
    @.set_node_value('KETTLE'    , 'label','KETTLE                  ')

    # add red box and anchor reference
    @.node_fixed_x_y('BUSINESS', 450,55)
    @.node_fixed_x_y('PUBLIC'  , 540,55)

    @.on_AfterDrawing = ()=>
      @.draw().color("darkred").box(370,15,250,70,20)
      @.draw().font(35).text("ANCHOR", 350,55)

      #@.draw().font(35).text("Created in Lambda!!!!", 450,255)
    return @

  create_map_test_nodes: ()->
    @.add_component('A (1,1)' , 1 ,1)
    @.add_component('B (1,2)' , 4, 8)
    @.add_component('C (2,3)' )
    @.add_component('D (2,4)' )
    @.add_component('E (3,5)' )
    @.add_component('F (3,6)' )
    @.add_component('G (4,7)' )
    @.add_component('H (4,8)' )

    @.add_connection('A (1,1)', 'B (1,2)')
    @.add_connection('A (1,1)', 'C (2,3)')
    @.add_connection('A (1,1)', 'D (2,4)')
    @.add_connection('A (1,1)', 'E (3,5)')
    @.add_connection('A (1,1)', 'F (3,6)')
    @.add_connection('A (1,1)', 'G (4,7)')
    @.add_connection('A (1,1)', 'H (4,8)')
    @.node_fixed_x_y('A (1,1)', 300,50)

#    @.add_connection('A (1,1)', 'B (1,2)')
#    @.add_connection('B (1,2)', 'C (2,3)')
#    @.add_connection('C (2,3)', 'D (2,4)')
#    @.add_connection('D (2,4)', 'E (3,5)')
#    @.add_connection('E (3,5)', 'F (3,6)')
#    @.add_connection('F (3,6)', 'G (4,7)')
#    @.add_connection('G (4,7)', 'H (4,8)')
#    @.node_fixed_x_y('A (1,1)', 300,20)
#    @.node_fixed_x_y('H (4,8)', 540,670)






#new Maps().setup()
          #.physics_off()
          #.create_map_test_nodes()
          #.create_map_for_tea_original()

#new Maps().setup().create_map_test_nodes()
new Maps().setup().create_map_for_tea_original()
