class Canvas_Draw
  constructor: (context,options) ->
    @.ctx  = context
    @.default_font = options?.font || 'Arial'

  arrow: (x1, y1, x2, y2)=>
    @.ctx.beginPath();
    @.ctx.moveTo(x1, y1);
    @.ctx.lineTo(x2, y2);
    @.ctx.stroke();         # draw arrow line

    rot = -Math.atan2(x1 - x2, y1 - y2) +  Math.PI;
    @.ctx.save();             # draw arrow head
    @.ctx.translate(x2, y2);
    @.ctx.rotate(rot);
    @.ctx.beginPath();
    @.ctx.moveTo(0, 0);
    @.ctx.lineTo(-5, -12);
    @.ctx.lineTo(5, -12);
    @.ctx.closePath();
    @.ctx.fill();
    @.ctx.restore();

  box: (x, y, w, h, r)=>
    if (w < 2 * r)
      r = w / 2
    if (h < 2 * r)
      r = h / 2
    @.ctx.beginPath();
    @.ctx.lineWidth = "3";
    @.ctx.moveTo(x+r, y);
    @.ctx.arcTo(x+w, y,   x+w, y+h, r);
    @.ctx.arcTo(x+w, y+h, x,   y+h, r);
    @.ctx.arcTo(x,   y+h, x,   y,   r);
    @.ctx.arcTo(x,   y,   x+w, y,   r);
    @.ctx.closePath();
    @.ctx.stroke();
    @


  circle: (x, y, r)=>
    @.ctx.strokeStyle = '#294475';
    @.ctx.lineWidth   = 40;
    @.ctx.fillStyle   = '#A6D5F7';
    @.ctx.circle(x,y,r)
    @.ctx.fill();
    @.ctx.stroke();
    @

  color: (color)=>
    @.ctx.strokeStyle = color
    @.ctx.fillStyle   = color
    @

  font: (font_size, font_type)=>
    @.ctx.font   = "#{font_size || 14}px #{font_type || @.default_font }";
    @

  gradient: (x1, y1, x2, y2, color_from, color_to)=>
    grd= @.ctx.createLinearGradient(x1, y1, x2, y2);
    grd.addColorStop(0,color_from);
    grd.addColorStop(1,color_to );
    @.ctx.fillStyle=grd;
    @

  line: (x1, y1, x2, y2)=>
    @.ctx.beginPath();
    @.ctx.moveTo(x1, y1);
    @.ctx.lineTo(x2, y2);
    @.ctx.stroke();
    @

  line_dash: (length)=>
    @.ctx.setLineDash([length,length])
    @

  rectangle: (from_x, from_y, to_x, to_y )=>
    @.ctx.rect(from_x, from_y, to_x, to_y);
    @.ctx.stroke()
    @

  rectangle_fill: (x1, y1, x2, y2 )=>
    @.ctx.fillRect(x1, y1, x2, y2)
    @.ctx.stroke()
    @

  text: (value, x, y)=>
    @.ctx.fillText(value, x, y);
    @

  text_align: (value)=>
    @.ctx.textAlign = value
    @

  text_vertical: (value, x, y)=>
    @.ctx.save();
    @.ctx.translate(x, y);
    @.ctx.rotate(-Math.PI/2);
    #@.ctx.textAlign = "center";
    @.ctx.fillText(value, 0, -20);
    @.ctx.restore();
    @

window.Canvas_Draw = Canvas_Draw