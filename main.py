import screen_Draw as draw

v = ((15,50),(700,35),(700,170),(600,200),(400,431),(65,400))
e = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,0))

line_color = (255,0,0)

draw.edges(v,e)

#draw.fill_triangle(v[0],v[1],v[2],line_color)

draw.img.show()