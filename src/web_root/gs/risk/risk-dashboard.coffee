class R1_and_R2
  constructor: (params)->
    @.set_params(params)

  create_table: ()=>
    $('.risks_table thead tr').html('') # clear existing table
    $('.risks_table tbody').html('')
    for i in [1..@.cells]
      header = $("<th id='r#{i}' >")
      $('.risks_table thead tr').append(header)

    for i in [1..@.rows]
      row = $("<tr id='row_#{i}' >")
      for j in [1..@.cells]
        cell = $("<td id='r#{j}_#{i}' valign='top'>")
        #cell.text("r#{j}_#{i}")
        row.append(cell)
      $('.risks_table tbody').append(row)

    @

  set_params: (params)=>
    @.params   = params ? {}
    @.cells    = @.params.cells     ? 1
    @.rows     = @.params.rows      ? 1
    @.data_R1s = @.params.data_R1s  ? {}
    @.data_R2s = @.params.data_R2s  ? {}
    @.risks    = @.params.risks     ? {}


  #set_data_r1: (data_R1s)=> @.data_R1s = data_R1s
  #set_data_r2: (data_R2s)=> @.data_R2s = data_R2s

  show_data: =>
    for key,value of @.data_R1s
      jQuery('#' + key).html(value)

    for key,value of @.data_R2s
      jQuery('#' + key).html(value)
    @

  set_risks: ()=>
    @.colors =  { '2' : 'darkred' ,'1': 'darkorange' , '0': 'black'}
    for key,value of @.risks
      console.log(key,value)
      $("##{key}").css({'background-color': @.colors[value]})

  create_risk_table:(params)=>
    @.set_params(params)
    @.create_table()
    @.show_data()
#    @.set_risks()


#$('.risks_table').hide()
window.r1_and_r2 = new R1_and_R2()#.create_data_cells(6,6,'.')
                                  #.set_data()
#$('.risks_table').show()