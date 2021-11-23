import numpy

class Model:
    def __init__(self, filename):
        self.vertices = []
        self.vn_vertices = []#法线
        self.uv_vertices = []#贴图
        self.uv_indices = []
        self.indices = []#对应哪三个顶点构成一个面，从1开始
        self.is_poly=False


        with open(filename,encoding='utf-8') as f:
            for line in f:
                if line.startswith("v "):
                    x, y, z = [float(d) for d in line.strip("v").strip().split(" ")]
                    self.vertices.append(numpy.array([x, y, z, 1.]))
                    
                elif line.startswith("vt "):
                    u, v = [float(d) for d in line.strip("vt").strip().split(" ")]
                    self.uv_vertices.append([u, v])
                    
                elif line.startswith("vn "):
                    x, y, z = [float(d) for d in line.strip("vn").strip().split(" ")]
                    self.vn_vertices.append([x, y, z])

                elif line.startswith("f "):
                    facet = [d.split("/") for d in line.strip("f").strip().split(" ")]
                    if len(facet)==3:
                        self.indices.append([int(d[0]) for d in facet])
                        self.uv_indices.append([int(d[1]) for d in facet])                    
                    elif len(facet)==4: 
                        self.is_poly=True
                        self.indices.append([int(d[0]) for d in facet[:3]])
                        self.indices.append([int(d[0]) for d in [facet[0],facet[2],facet[3]]])
                        self.uv_indices.append([int(d[1]) for d in facet[:3]])
                        self.uv_indices.append([int(d[1]) for d in [facet[0],facet[2],facet[3]]])
                        
            if self.is_poly:
                z=[]
                for i in self.vn_vertices:
                    z.append(i)
                    z.append(i)
                self.vn_vertices=z#等待换写法
                
                    
                    

if __name__=="__main__":
    m=Model("model/box.obj")
    
    print("indices:")
    for i,j in enumerate(m.indices):
        print(i,j)
        if i>=20:   break
        
    print("vertices:")
    for i,j in enumerate(m.vertices):
        print(i,j)
        if i>=20:   break
        
    print("uv_indices:")
    for i,j in enumerate(m.uv_indices):
        print(i,j)
        if i>=20:   break
        
    print("uv_vertices:")
    for i,j in enumerate(m.uv_vertices):
        print(i,j)
        if i>=20:   break
    
    print("vn_vertices:")
    for i,j in enumerate(m.vn_vertices):
        print(i,j)
        if i>=20:   break
        
    
