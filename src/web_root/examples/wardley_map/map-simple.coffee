class Maps extends window.Api_VisJs

  create_map: ()->
    @.add_component('Business' , 3, 1)
    @.add_component('User'     , 3, 5)
    @.add_component('Test'     , 1, 3)

    @.add_connection('Business', 'Test')
    @.add_connection('Business', 'User')

maps = new Maps()
maps.rows = ['A', 'B','C', 'D']
#maps.hide_anchor_edges = false
maps.setup()

maps.connection_arrows = 'to'
#maps.draw_static_elements = ()=>

maps.add_component(maps.hide_anchor_edges, 3,3)
maps.create_map()